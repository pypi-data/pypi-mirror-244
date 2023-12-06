"""Module providing abstract classes for classification models."""
import functools
import json
import os
import platform
import time
from typing import Any, Dict, Iterator, List, Optional, Tuple, Type, Union

import numpy as np
import pandas as pd
from cache_decorator import Cache
from ensmallen import Graph, express_measures
from environments_utils import must_be_in_slurm_node
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    hamming_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from tqdm.auto import tqdm, trange
from userinput.utils import must_be_in_set
from embiggen.__version__ import __version__ as __embiggen_version__

from embiggen.utils.abstract_edge_feature import AbstractEdgeFeature
from embiggen.utils.abstract_models.abstract_embedding_model import (
    AbstractEmbeddingModel,
    EmbeddingResult,
)
from embiggen.utils.abstract_models.abstract_feature_preprocessor import (
    AbstractFeaturePreprocessor,
)
from embiggen.utils.abstract_models.abstract_model import AbstractModel, abstract_class
from embiggen.utils.abstract_models.list_formatting import format_list


@abstract_class
class AbstractClassifierModel(AbstractModel):
    """Class defining properties of an abstract classifier model."""

    def __init__(self, random_state: Optional[int] = None):
        """Create new instance of model.

        Parameters
        ---------------
        random_state: Optional[int] = None
            The random state to use if the model is stocastic.
        """
        super().__init__(random_state=random_state)
        self._fitting_was_executed = False
        self._is_using_node_type_features = False
        self._is_using_edge_type_features = False

        # The following three lists will imprint on the provided features and
        # will help in the case of potential mis-alignments between the provided
        # training features and those later provided for the predictions. The
        # idea is that, while commonly the models concretely implementing this class
        # will most commonly test that the dimensionality of the provided features
        # is a given amount, it cannot execute a per-feature check, as the features
        # will be concatenated at that point and it is no longer possible to verify
        # whether two features have been swapped.

        # Furthermore, some features are rasterized at different points in time.
        # When a feature has not yet been turned into a numpy array, we will put
        # 'None' as its shape, and skip that particular feature when checking
        # for the feature shapes. We will still check, of course, that the
        # number of features is the same.
        self._node_feature_shapes: Optional[List[Optional[Tuple[int]]]] = None
        self._node_type_feature_shapes: Optional[List[Optional[Tuple[int]]]] = None
        self._edge_type_feature_shapes: Optional[List[Optional[Tuple[int]]]] = None

        # We additionally imprint the model on the training graph density. In this manner,
        # if the model is later used on a different graph, we can check whether the density
        # of the graph changes significantly and, if so, we can warn the user that the
        # model may not be applicable to the new graph and a different support graph may
        # be required.
        self._training_graph_density: Optional[float] = None

    def _check_feature_shapes(
        self,
        expected_feature_shapes: Optional[List[Optional[Tuple[int]]]],
        provided_features: Optional[List[Union[np.ndarray, Any]]],
        feature_name: str,
    ) -> List[Optional[Tuple[int]]]:
        """Check that the provided features have the expected shapes."""
        if provided_features is None and expected_feature_shapes is None:
            return None

        if provided_features is None and expected_feature_shapes is not None:
            raise ValueError(
                f"The provided {feature_name} features are None, "
                f"while the expected features are {format_list(expected_feature_shapes)}. "
                "Maybe these features refer to another "
                "version of the graph or another graph "
                "entirely?"
            )

        # If the expected feature shapes was not yet learned, we imprint
        # it on the provided features.
        if expected_feature_shapes is None:
            return [
                provided_feature.shape
                if isinstance(provided_feature, np.ndarray)
                else None
                for provided_feature in provided_features
            ]
        if len(expected_feature_shapes) != len(provided_features):
            raise ValueError(
                f"The provided {feature_name} features have {len(provided_features)} features, "
                f"while the expected features have {len(expected_feature_shapes)} features. "
                "Maybe these features refer to another "
                "version of the graph or another graph "
                "entirely?"
            )
        for i, provided_feature in enumerate(provided_features):
            if expected_feature_shapes[i] is None:
                expected_feature_shapes[i] = (
                    provided_feature.shape
                    if isinstance(provided_feature, np.ndarray)
                    else None
                )
            if expected_feature_shapes[i] is not None:
                if not isinstance(provided_feature, np.ndarray):
                    raise ValueError(
                        f"The provided {feature_name} features are of type `{type(provided_feature)}`, "
                        "while we only currently support numpy arrays. "
                        "What behaviour were you expecting with this feature? "
                        "Please do open an issue on Embiggen and let us know!"
                    )
                # We check that the provided feature has the expected shape, except
                # for the first colum which is the number of elements in the graph and
                # the user may want to run the models on graphs with different number
                # of nodes.
                if provided_feature.shape[1:] != expected_feature_shapes[i][1:]:
                    raise ValueError(
                        f"The provided {feature_name} features have shape {provided_feature.shape}, "
                        f"while the expected features have shape {expected_feature_shapes[i]}. "
                        "Maybe these features refer to another "
                        "version of the graph or another graph "
                        "entirely?"
                    )
        return expected_feature_shapes

    def _check_node_features_shapes(
        self,
        provided_node_features: Optional[List[Union[np.ndarray, Any]]],
    ):
        """Check that the provided node features have the expected shapes."""
        self._node_feature_shapes = self._check_feature_shapes(
            expected_feature_shapes=self._node_feature_shapes,
            provided_features=provided_node_features,
            feature_name="node",
        )

    def _check_node_type_features_shapes(
        self,
        provided_node_type_features: Optional[List[Union[np.ndarray, Any]]],
    ):
        """Check that the provided node type features have the expected shapes."""
        self._node_type_feature_shapes = self._check_feature_shapes(
            expected_feature_shapes=self._node_type_feature_shapes,
            provided_features=provided_node_type_features,
            feature_name="node type",
        )

    def _check_edge_type_features_shapes(
        self,
        provided_edge_type_features: Optional[List[Union[np.ndarray, Any]]],
    ):
        """Check that the provided edge type features have the expected shapes."""
        self._edge_type_feature_shapes = self._check_feature_shapes(
            expected_feature_shapes=self._edge_type_feature_shapes,
            provided_features=provided_edge_type_features,
            feature_name="edge type",
        )

    def _check_nan(
        self,
        features: List[np.ndarray],
        feature_kind: str
    ):
        """Check that the provided features do not contain NaNs."""
        for feature in features:
            nan_mask = np.isnan(feature)
            number_of_nans = nan_mask.sum()
            if number_of_nans > 0:
                number_of_rows_with_nans = nan_mask.any(axis=1).sum()
                number_of_columns_with_nans = nan_mask.any(axis=0).sum()
                raise ValueError(
                    f"The provided {feature_kind} features contain {number_of_nans} NaNs "
                    f"out or {feature.size} elements. "
                    f"Furthermore, {number_of_rows_with_nans} out of {number_of_rows_with_nans.shape[0]} "
                    f"rows and {number_of_columns_with_nans} out of {number_of_rows_with_nans.shape[1]} columns "
                    f"contain at least one NaN. "
                    "Please remove them before fitting the model, "
                    "either by dropping the rows or by imputing them."
                )

    @classmethod
    def _handle_potentially_misparametrized_edge_features(
        cls, features: List[Any], expected_parameter_name: str
    ):
        """Raises an exception if an edge feature-like type was provided instead than the expected feature type.

        Parameters
        ---------------------
        features: List[Any]
            The features to check.
        expected_feature_name: str
            The name of the expected feature type.
        """
        for feature in features:
            if issubclass(type(feature), AbstractEdgeFeature):
                raise ValueError(
                    f"The provided {expected_parameter_name} features are of type `{type(feature)}`, "
                    f"which is an edge feature, called {feature.get_feature_name()}. Edge features are not supported "
                    f"as {expected_parameter_name}, most likely you meant to provide them as edge features. "
                    f"Instead of providing them for the parameter `{expected_parameter_name}`, "
                    "please provide them for the `edge_features` parameter."
                )

    @classmethod
    def _handle_potentially_misparametrized_features(
        cls,
        features: List[Union[pd.DataFrame, np.ndarray]],
        expected_parameter_name: str,
        expected_number_of_elements: int,
        expected_getter_from_index,
        expected_has_index_name,
        graph: Graph,
    ):
        """Raises an exception if a feature was provided instead of expected feature type.

        Parameters
        ---------------------
        features: List[Union[pd.DataFrame, np.ndarray]]
            The features to check.
        expected_parameter_name: str
            The name of the expected parameter.
        expected_number_of_elements: int
            The expected number of elements in the feature.
        expected_getter_from_index
            The expected getter from index.
        expected_has_index_name
            Checks whether a provided index name exists in the current graph.
        graph: Graph
            The graph to check for.
        """

        if graph.get_name().lower() != "graph":
            graph_name_message = (
                f"You are using a graph with name `{graph.get_name()}`. "
            )
        else:
            graph_name_message = ""

        for feature in features:
            # If the feature is neither a numpy array nor a pandas dataframe, we raise an exception.
            if not isinstance(feature, (np.ndarray, pd.DataFrame)):
                raise ValueError(
                    f"The provided {expected_parameter_name} features are of type `{type(feature)}`, "
                    "while we only currently support numpy arrays and pandas DataFrames. "
                    f"{graph_name_message}"
                    "What behaviour were you expecting with this feature? "
                    "Please do open an issue on Embiggen and let us know!"
                )

            # We check whether the provided feature has the expected number of elements.
            if feature.shape[0] == expected_number_of_elements:
                # If the feature is a numpy array, we cannot execute any more checks
                # other than the number of elements and therefore we skip the rest.
                if isinstance(feature, np.ndarray):
                    continue

                # If the feature is a pandas dataframe, we check that the index is the same as the one
                # of the expected feature.
                if isinstance(feature, pd.DataFrame):
                    index_full_match = True
                    for index, index_value in enumerate(feature.index):
                        # We convert the index value from the dataframe to string
                        # in the case that pandas has converted it to a number.
                        if expected_getter_from_index(index) != str(index_value):
                            index_full_match = False
                            break
                    if index_full_match:
                        continue
            # We don't give up yet - if the provided feature is a DataFrame, and the number of rows
            # in the dataframe is higher or equal to the expected number of elements, we check that
            # all of the index of the expected feature are contained in the provided dataframe.
            if (
                isinstance(feature, pd.DataFrame)
                and feature.shape[0] >= expected_number_of_elements
            ):
                if feature.index.has_duplicates:
                    raise ValueError(
                        f"The feature provided as {expected_parameter_name} has {feature.shape[0]} rows, "
                        f"while the expected number of elements is {expected_number_of_elements}. "
                        "Furthermore, the provided feature has duplicate rows, which is not supported. "
                        f"{graph_name_message}"
                    )
                matched_index_name_counter = 0
                for index_value in feature.index:
                    if expected_has_index_name(index_value):
                        matched_index_name_counter += 1
                if matched_index_name_counter == expected_number_of_elements:
                    continue

            for (
                candidate_feature_parameter,
                candidate_number_of_elements,
                getter_from_index,
                candidate_has_index_name,
            ) in (
                (
                    "node_features",
                    graph.get_number_of_nodes(),
                    graph.get_node_name_from_node_id,
                    graph.has_node_name,
                ),
                (
                    "node_type_features",
                    graph.get_number_of_node_types() if graph.has_node_types() else 0,
                    graph.get_node_type_name_from_node_type_id,
                    graph.has_node_type_name,
                ),
                (
                    "edge_type_features",
                    graph.get_number_of_edge_types() if graph.has_edge_types() else 0,
                    graph.get_edge_type_name_from_edge_type_id,
                    graph.has_edge_type_name,
                ),
            ):
                # If the number of elements of the candidate feature is not equal to the number of elements
                # of the provided feature, surely the provided feature is not of the type of the candidate feature.
                if candidate_number_of_elements != feature.shape[0]:
                    continue
                # If the current candidate feature parameter is equal to the expected parameter name,
                # we skip it, as we are checking for the other features.
                if expected_parameter_name == candidate_feature_parameter:
                    continue
                # If the number of elements of the candidate feature is equal to the number of elements
                # of the provided feature, we check that the provided feature is not of the type of the candidate feature.
                if candidate_number_of_elements == feature.shape[0]:
                    # If the provided feature is a dataframe, we check that the index is the same as the one
                    # of the candidate feature. If so, it is extremely likely that the user provided the feature
                    # as the wrong parameter.
                    if isinstance(feature, pd.DataFrame):
                        index_match_completely = True
                        for index, index_value in enumerate(feature.index):
                            # We convert the index value from the dataframe to string
                            # in the case that pandas has converted it to a number.
                            if getter_from_index(index) != str(index_value):
                                index_match_completely = False
                                break
                        if index_match_completely:
                            raise ValueError(
                                f"The provided {expected_parameter_name} features have shape {feature.shape[0]} "
                                f"which matches the shape of the {candidate_feature_parameter} features. "
                                "Furthermore, the index of the provided features matches the index of the "
                                f"{candidate_feature_parameter} features. "
                                f"{graph_name_message}"
                                f"Instead of providing them for the parameter `{expected_parameter_name}`, "
                                f"most likely you meant to provide them as {candidate_feature_parameter}."
                            )

                        # We don't give up yet - if the provided feature is a DataFrame, and the number of rows
                        # in the dataframe is higher or equal to the candidate number of elements, we check that
                        # all of the index of the candidate feature are contained in the provided dataframe.
                        if (
                            isinstance(feature, pd.DataFrame)
                            and feature.shape[0] >= candidate_number_of_elements
                        ):
                            if feature.index.has_duplicates:
                                raise ValueError(
                                    f"The feature provided as {candidate_feature_parameter} has {feature.shape[0]} rows, "
                                    f"while the candidate number of elements is {candidate_number_of_elements}. "
                                    f"{graph_name_message}"
                                    "Furthermore, the provided feature has duplicate rows, which is not supported."
                                )
                            matched_index_name_counter = 0
                            for index_value in feature.index:
                                if candidate_has_index_name(index_value):
                                    matched_index_name_counter += 1
                            if (
                                matched_index_name_counter
                                == candidate_number_of_elements
                            ):
                                continue

                        # If not even that works, the current feature is surely not of the candidate
                        # feature type and we can continue to the next candidate.
                        continue

                    raise ValueError(
                        f"The provided {expected_parameter_name} features have shape {feature.shape[0]} "
                        f"which matches the shape of the {candidate_feature_parameter} features "
                        f"and does not match the expepected number of elements {expected_number_of_elements}."
                        f"{graph_name_message}"
                        f"Instead of providing them for the parameter `{expected_parameter_name}`, "
                        f"most likely you meant to provide them as {candidate_feature_parameter}."
                    )

            # If we got this far down, it means that the current feature is not compatible with
            # the expected feature and NONE of the candidate features. Therefore, we raise an exception.
            raise ValueError(
                f"The provided {expected_parameter_name} features have shape {feature.shape[0]} "
                f"and do not match the expected number of elements {expected_number_of_elements}. "
                f"{graph_name_message}"
                "We checked this feature against node features, node type features and edge type features "
                "and none of them seem to match - it is unclear what you expected this feature to be."
            )

    def _fit(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[
            Union[Type[AbstractEdgeFeature], List[np.ndarray]]
        ] = None,
    ):
        """Run fitting on the provided graph.

        Parameters
        --------------------
        graph: Graph
            The graph to run predictions on.
        support: Optional[Graph] = None
            The graph describiding the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological classifiers
            such as Graph Convolutional Networks.
        node_features: Optional[List[np.ndarray]] = None
            The node features to use.
        node_type_features: Optional[List[np.ndarray]] = None
            The node type features to use.
        edge_type_features: Optional[List[np.ndarray]] = None
            The edge type features to use.
        edge_features: Optional[Union[Type[AbstractEdgeFeature], List[np.ndarray]]] = None
            The edge features to use.
        """
        raise NotImplementedError(
            (
                "The `_fit` method must be implemented "
                "in the child classes of abstract model. "
                f"The {self.model_name()} from library {self.library_name()} "
                f"needs to implement this method for the task {self.task_name()}."
            )
        )

    def _predict(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[
            Union[Type[AbstractEdgeFeature], List[np.ndarray]]
        ] = None,
    ) -> np.ndarray:
        """Run prediction on the provided graph.

        Parameters
        --------------------
        graph: Graph
            The graph to run predictions on.
        support: Optional[Graph] = None
            The graph describiding the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological classifiers
            such as Graph Convolutional Networks.
        node_features: Optional[List[np.ndarray]] = None
            The node features to use.
        node_type_features: Optional[List[np.ndarray]] = None
            The node type features to use.
        edge_type_features: Optional[List[np.ndarray]] = None
            The edge type features to use.
        edge_features: Optional[Union[Type[AbstractEdgeFeature], List[np.ndarray]]] = None
            The edge features to use.
        """
        raise NotImplementedError(
            (
                "The `_predict` method must be implemented "
                "in the child classes of abstract model. "
                f"The {self.model_name()} from library {self.library_name()} "
                f"needs to implement this method for the task {self.task_name()}."
            )
        )

    def _predict_proba(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[
            Union[Type[AbstractEdgeFeature], List[np.ndarray]]
        ] = None,
    ) -> Union[np.ndarray, Iterator[np.ndarray]]:
        """Run prediction on the provided graph.

        Parameters
        --------------------
        graph: Graph
            The graph to run predictions on.
        support: Optional[Graph] = None
            The graph describiding the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological classifiers
            such as Graph Convolutional Networks.
        node_features: Optional[List[np.ndarray]] = None
            The node features to use.
        node_type_features: Optional[List[np.ndarray]] = None
            The node type features to use.
        edge_type_features: Optional[List[np.ndarray]] = None
            The edge type features to use.
        edge_features: Optional[Union[Type[AbstractEdgeFeature], List[np.ndarray]]] = None
            The edge features to use.
        """
        raise NotImplementedError(
            (
                "The `_predict_proba` method must be implemented "
                "in the child classes of abstract model. "
                f"The {self.model_name()} from library {self.library_name()} "
                f"needs to implement this method for the task {self.task_name()}."
            )
        )

    def is_binary_prediction_task(self) -> bool:
        """Returns whether the model was fit on a binary prediction task."""
        raise NotImplementedError(
            (
                "The `is_binary_prediction_task` method should be implemented "
                "in the child classes of abstract model. "
                f"The {self.model_name()} from library {self.library_name()} "
                f"needs to implement this method for the task {self.task_name()}."
            )
        )

    def is_multilabel_prediction_task(self) -> bool:
        """Returns whether the model was fit on a multilabel prediction task."""
        raise NotImplementedError(
            (
                "The `is_multilabel_prediction_task` method should be implemented "
                "in the child classes of abstract model. "
                f"The {self.model_name()} from library {self.library_name()} "
                f"needs to implement this method for the task {self.task_name()}."
            )
        )

    @classmethod
    def supports_multilabel_prediction(cls) -> bool:
        """Returns whether the model supports multilabel prediction."""
        raise NotImplementedError(
            (
                "The `supports_multilabel_prediction` method should be implemented "
                "in the child classes of abstract model. "
                f"The {cls.model_name()} from library {cls.library_name()} "
                f"needs to implement this method for the task {cls.task_name()}."
            )
        )

    @classmethod
    def get_available_evaluation_schemas(cls) -> List[str]:
        """Returns available evaluation schemas for this task."""
        raise NotImplementedError(
            (
                "The `get_available_evaluation_schemas` method must be implemented "
                "in the child classes of abstract model. "
                f"The {cls.model_name()} from library {cls.library_name()} "
                f"needs to implement this method for the task {cls.task_name()}."
            )
        )

    @classmethod
    def load(cls, path: str):
        """Load a saved version of the model from the provided path.

        Parameters
        -------------------
        path: str
            Path from where to load the model.
        """
        raise NotImplementedError(
            (
                f"The `load` was not implemented for the {cls.model_name()} "
                f"for the {cls.task_name()} task as made available from the "
                f"{cls.library_name()} library."
            )
        )

    def dump(self, path: str):
        """Dump the current model at the provided path.

        Parameters
        -------------------
        path: str
            Path from where to dump the model.
        """
        raise NotImplementedError(
            (
                f"The `dump` was not implemented for the {self.model_name()} "
                f"for the {self.task_name()} task as made available from the "
                f"{self.library_name()} library."
            )
        )

    @classmethod
    def normalize_node_feature(
        cls,
        graph: Graph,
        support: Graph,
        random_state: int,
        node_feature: Union[
            str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]
        ],
        node_features_preprocessing_steps: Optional[
            Union[
                Type[AbstractFeaturePreprocessor],
                List[Type[AbstractFeaturePreprocessor]],
            ]
        ] = None,
        allow_automatic_feature: bool = True,
        skip_evaluation_biased_feature: bool = False,
        smoke_test: bool = False,
        precompute_constant_stocastic_features: bool = False,
    ) -> List[np.ndarray]:
        """Normalizes the provided node features and validates them.

        Parameters
        ------------------
        graph: Graph
            The graph to check for.
        support: Graph
            The graph describing the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological features.
        random_state: int
            The random state to use for the stochastic automatic features.
        node_feature: Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]],
            The node feature to normalize.
        node_features_preprocessing_steps: Optional[Union[Type[AbstractFeaturePreprocessor], List[Type[AbstractFeaturePreprocessor]]]] = None
            The preprocessing steps to apply to the node features.
        allow_automatic_feature: bool = True
            Whether to allow feature names creation based on the
            provided feature name, using the default settings,
            or based on a provided abstract embedding model that
            will be called on the provided graph.
        skip_evaluation_biased_feature: bool = False
            Whether to skip feature names that are known to be biased
            when running an holdout. These features should be computed
            exclusively on the training graph and not the entire graph.
        smoke_test: bool = False
            Whether this run should be considered a smoke test
            and therefore use the smoke test configurations for
            the provided model names and feature names.
        precompute_constant_stocastic_features: bool = False
            Whether to precompute once the constant automatic stocastic
            features before starting the embedding loop. This means that,
            when left set to false, while the features will be computed
            using the same input data, the random state between runs will
            be different and therefore the experiment performance will
            capture more of the variance derived from the stocastic aspect
            of the considered method. When set to true, they are only computed
            once and therefore the experiment will be overall faster.
        """
        if isinstance(node_feature, str):
            if not allow_automatic_feature:
                raise ValueError(
                    f"The node feature `{node_feature}` was requested, but "
                    "the `allow_automatic_feature` has been set to False. "
                    "This may be because this is an evaluation execution or "
                    "a prediction, and the string feature should be obtained "
                    "from either the training graph, the test graph or the "
                    "complete graph and it is not clear which one was provided. "
                    "Consider calling the `normalize_node_features` method "
                    "yourselves to completely define your intentions."
                )

            node_feature = AbstractEmbeddingModel.get_model_from_library(
                model_name=node_feature, task_name="Node Embedding"
            )()

        # If this object is an implementation of an abstract
        # embedding model, we compute the embedding.
        if issubclass(type(node_feature), AbstractEmbeddingModel):
            if skip_evaluation_biased_feature and (
                cls.task_involves_edge_types()
                and node_feature.can_use_edge_types()
                and node_feature.is_using_edge_types()
                or cls.task_involves_node_types()
                and node_feature.can_use_node_types()
                and node_feature.is_using_node_types()
                or cls.task_involves_edge_weights()
                and node_feature.can_use_edge_weights()
                and node_feature.is_using_edge_weights()
                or cls.task_involves_topology()
                and node_feature.is_topological()
                or not precompute_constant_stocastic_features
                and node_feature.is_stocastic()
            ):
                yield node_feature
                return None

            if node_feature.is_stocastic():
                node_feature.set_random_state(random_state)

            if smoke_test:
                node_feature = node_feature.into_smoke_test()

            node_feature = node_feature.fit_transform(
                graph=support, return_dataframe=False
            )

        if isinstance(node_feature, EmbeddingResult):
            node_feature = node_feature.get_all_node_embedding()

        if not isinstance(node_feature, list):
            node_feature = [node_feature]

        if node_features_preprocessing_steps is None:
            node_features_preprocessing_steps = []

        if not isinstance(node_features_preprocessing_steps, list):
            node_features_preprocessing_steps = [node_features_preprocessing_steps]

        for preprocessing_step in node_features_preprocessing_steps:
            node_feature = preprocessing_step.transform(
                support=support, node_features=node_feature
            )

        if isinstance(node_feature, EmbeddingResult):
            node_feature = node_feature.get_all_node_embedding()

        cls._handle_potentially_misparametrized_features(
            features=node_feature,
            expected_parameter_name="node_features",
            expected_number_of_elements=graph.get_number_of_nodes(),
            expected_getter_from_index=graph.get_node_name_from_node_id,
            expected_has_index_name=graph.has_node_name,
            graph=graph,
        )

        for nf in node_feature:
            # If it is a dataframe we align it
            if isinstance(nf, pd.DataFrame):
                yield nf.loc[graph.get_node_names()].to_numpy()
            else:
                # And if it is a numpy array we must believe that the user knows what
                # they are doing, as we cannot ensure alignment.
                yield nf

    @classmethod
    def normalize_node_features(
        cls,
        graph: Graph,
        support: Graph,
        random_state: int,
        node_features: Optional[
            Union[
                str,
                pd.DataFrame,
                np.ndarray,
                Type[AbstractEmbeddingModel],
                List[
                    Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]
                ],
            ]
        ] = None,
        node_features_preprocessing_steps: Optional[
            Union[
                Type[AbstractFeaturePreprocessor],
                List[Type[AbstractFeaturePreprocessor]],
            ]
        ] = None,
        allow_automatic_feature: bool = True,
        skip_evaluation_biased_feature: bool = False,
        smoke_test: bool = False,
        precompute_constant_stocastic_features: bool = False,
    ) -> List[np.ndarray]:
        """Normalizes the provided node features and validates them.

        Parameters
        ------------------
        graph: Graph
            The graph to check for.
        support: Graph
            The graph describing the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological features.
        random_state: int
            The random state to use for the stochastic automatic features.
        node_features: Optional[Union[str, pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]]]] = None
            The node features to normalize.
        node_features_preprocessing_steps: Optional[Union[Type[AbstractFeaturePreprocessor], List[Type[AbstractFeaturePreprocessor]]]] = None
            The preprocessing steps to apply to the node features.
        allow_automatic_feature: bool = True
            Whether to allow feature names creation based on the
            provided feature name, using the default settings,
            or based on a provided abstract embedding model that
            will be called on the provided graph.
        skip_evaluation_biased_feature: bool = False
            Whether to skip feature names that are known to be biased
            when running an holdout. These features should be computed
            exclusively on the training graph and not the entire graph.
        smoke_test: bool = False
            Whether this run should be considered a smoke test
            and therefore use the smoke test configurations for
            the provided model names and feature names.
        precompute_constant_stocastic_features: bool = False
            Whether to precompute once the constant automatic stocastic
            features before starting the embedding loop. This means that,
            when left set to false, while the features will be computed
            using the same input data, the random state between runs will
            be different and therefore the experiment performance will
            capture more of the variance derived from the stocastic aspect
            of the considered method. When set to true, they are only computed
            once and therefore the experiment will be overall faster.
        """
        if node_features is None:
            return []

        if not isinstance(node_features, (list, tuple)):
            node_features = [node_features]

        # If any node features are provided, we need to make sure that
        # the support and the graph have aligned vocabularies for what
        # entails the node names.
        if not support.has_compatible_node_vocabularies(graph):
            raise ValueError(
                "The provided graph and support graphs do not have compatible "
                "node vocabularies. Please make sure that the node names "
                "are the same for both graphs."
            )

        # We check that the provided features are not edge features,
        # and if they are we provide a meaningful error.
        cls._handle_potentially_misparametrized_edge_features(
            features=node_features,
            expected_parameter_name="node_features",
        )

        return [
            normalized_node_feature
            for node_feature in node_features
            for normalized_node_feature in cls.normalize_node_feature(
                graph=graph,
                support=support,
                random_state=random_state,
                node_feature=node_feature,
                node_features_preprocessing_steps=node_features_preprocessing_steps,
                allow_automatic_feature=allow_automatic_feature,
                skip_evaluation_biased_feature=skip_evaluation_biased_feature,
                smoke_test=smoke_test,
                precompute_constant_stocastic_features=precompute_constant_stocastic_features,
            )
        ]

    @classmethod
    def normalize_node_type_feature(
        cls,
        graph: Graph,
        support: Graph,
        random_state: int,
        node_type_feature: Union[
            str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]
        ],
        allow_automatic_feature: bool = True,
        skip_evaluation_biased_feature: bool = False,
        smoke_test: bool = False,
        precompute_constant_stocastic_features: bool = False,
    ) -> List[np.ndarray]:
        """Normalizes the provided node type features and validates them.

        Parameters
        ------------------
        graph: Graph
            The graph to check for.
        support: Graph
            The graph describing the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological features.
        random_state: int
            The random state to use for the stochastic automatic features.
        node_type_feature: Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]],
            The node type feature to normalize.
        allow_automatic_feature: bool = True
            Whether to allow feature names creation based on the
            provided feature name, using the default settings,
            or based on a provided abstract embedding model that
            will be called on the provided graph.
        skip_evaluation_biased_feature: bool = False
            Whether to skip feature names that are known to be biased
            when running an holdout. These features should be computed
            exclusively on the training graph and not the entire graph.
        smoke_test: bool = False
            Whether this run should be considered a smoke test
            and therefore use the smoke test configurations for
            the provided model names and feature names.
        precompute_constant_stocastic_features: bool = False
            Whether to precompute once the constant automatic stocastic
            features before starting the embedding loop. This means that,
            when left set to false, while the features will be computed
            using the same input data, the random state between runs will
            be different and therefore the experiment performance will
            capture more of the variance derived from the stocastic aspect
            of the considered method. When set to true, they are only computed
            once and therefore the experiment will be overall faster.
        """
        if isinstance(node_type_feature, str):
            if not allow_automatic_feature:
                raise ValueError(
                    f"The node type feature `{node_type_feature}` was requested, but "
                    "the `allow_automatic_feature` has been set to False. "
                    "This may be because this is an evaluation execution or "
                    "a prediction, and the string feature should be obtained "
                    "from either the training graph, the test graph or the "
                    "complete graph and it is not clear which one was provided. "
                    "Consider calling the `normalize_node_type_features` method "
                    "yourselves to completely define your intentions."
                )

            node_type_feature = AbstractEmbeddingModel.get_model_from_library(
                model_name=node_type_feature
            )()

        # If this object is an implementation of an abstract
        # embedding model, we compute the embedding.
        if issubclass(node_type_feature.__class__, AbstractEmbeddingModel):
            if skip_evaluation_biased_feature and (
                cls.task_involves_edge_types()
                and node_type_feature.is_using_edge_types()
                or cls.task_involves_node_types()
                and node_type_feature.is_using_node_types()
                or cls.task_involves_edge_weights()
                and node_type_feature.is_using_edge_weights()
                or cls.task_involves_topology()
                and node_type_feature.is_topological()
                or not precompute_constant_stocastic_features
                and node_type_feature.is_stocastic()
            ):
                yield node_type_feature
                return None

            if node_type_feature.is_stocastic():
                node_type_feature.set_random_state(random_state)

            if smoke_test:
                node_type_feature = node_type_feature.into_smoke_test()

            node_type_feature = node_type_feature.fit_transform(
                graph=support,
                return_dataframe=False,
            )

        if isinstance(node_type_feature, EmbeddingResult):
            node_type_feature = node_type_feature.get_all_node_type_embeddings()

        if not isinstance(node_type_feature, list):
            node_type_feature = [node_type_feature]

        cls._handle_potentially_misparametrized_features(
            features=node_type_feature,
            expected_parameter_name="node_type_features",
            expected_number_of_elements=graph.get_number_of_node_types(),
            expected_getter_from_index=graph.get_node_type_name_from_node_type_id,
            expected_has_index_name=graph.has_node_type_name,
            graph=graph,
        )

        for nf in node_type_feature:
            # If it is a dataframe we align it
            if isinstance(nf, pd.DataFrame):
                yield nf.loc[graph.get_unique_node_type_names()].to_numpy()
            else:
                # And if it is a numpy array we must believe that the user knows what
                # they are doing, as we cannot ensure alignment.
                yield nf

    @classmethod
    def normalize_node_type_features(
        cls,
        graph: Graph,
        support: Graph,
        random_state: int,
        node_type_features: Optional[
            Union[
                str,
                pd.DataFrame,
                np.ndarray,
                Type[AbstractEmbeddingModel],
                List[
                    Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]
                ],
            ]
        ] = None,
        allow_automatic_feature: bool = True,
        skip_evaluation_biased_feature: bool = False,
        smoke_test: bool = False,
        precompute_constant_stocastic_features: bool = False,
    ) -> List[np.ndarray]:
        """Normalizes the provided node type features and validates them.

        Parameters
        ------------------
        graph: Graph
            The graph to check for.
        support: Graph
            The graph describing the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological features.
        random_state: int
            The random state to use for the stochastic automatic features.
        node_type_features: Optional[Union[str, pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]]]] = None
            The node features to normalize.
        allow_automatic_feature: bool = True
            Whether to allow feature names creation based on the
            provided feature name, using the default settings,
            or based on a provided abstract embedding model that
            will be called on the provided graph.
        skip_evaluation_biased_feature: bool = False
            Whether to skip feature names that are known to be biased
            when running an holdout. These features should be computed
            exclusively on the training graph and not the entire graph.
        smoke_test: bool = False
            Whether this run should be considered a smoke test
            and therefore use the smoke test configurations for
            the provided model names and feature names.
        precompute_constant_stocastic_features: bool = False
            Whether to precompute once the constant automatic stocastic
            features before starting the embedding loop. This means that,
            when left set to false, while the features will be computed
            using the same input data, the random state between runs will
            be different and therefore the experiment performance will
            capture more of the variance derived from the stocastic aspect
            of the considered method. When set to true, they are only computed
            once and therefore the experiment will be overall faster.
        """
        if node_type_features is None:
            return []

        if not isinstance(node_type_features, (list, tuple)):
            node_type_features = [node_type_features]

        # If any node type features are provided, we need to make sure that
        # the support and the graph have aligned vocabularies for what
        # entails the node type names.
        if not support.has_compatible_node_types_vocabularies(graph):
            raise ValueError(
                "The provided graph and support graphs do not have compatible "
                "node type vocabularies. Please make sure that the node type names "
                "are the same for both graphs."
            )

        # We check that the provided features are not edge features,
        # and if they are we provide a meaningful error.
        cls._handle_potentially_misparametrized_edge_features(
            features=node_type_features,
            expected_parameter_name="node_type_features",
        )

        return [
            normalized_node_type_feature
            for node_type_feature in node_type_features
            for normalized_node_type_feature in cls.normalize_node_type_feature(
                graph=graph,
                support=support,
                random_state=random_state,
                node_type_feature=node_type_feature,
                allow_automatic_feature=allow_automatic_feature,
                skip_evaluation_biased_feature=skip_evaluation_biased_feature,
                smoke_test=smoke_test,
                precompute_constant_stocastic_features=precompute_constant_stocastic_features,
            )
        ]

    @classmethod
    def normalize_edge_type_feature(
        cls,
        graph: Graph,
        support: Graph,
        random_state: int,
        edge_type_feature: Union[
            str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]
        ],
        allow_automatic_feature: bool = True,
        skip_evaluation_biased_feature: bool = False,
        smoke_test: bool = False,
        precompute_constant_stocastic_features: bool = False,
    ) -> List[np.ndarray]:
        """Normalizes the provided edge type features and validates them.

        Parameters
        ------------------
        graph: Graph
            The graph to check for.
        support: Graph
            The graph describing the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological features.
        random_state: int
            The random state to use for the stochastic automatic features.
        edge_type_feature: Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]],
            The edge type feature to normalize.
        allow_automatic_feature: bool = True
            Whether to allow feature names creation based on the
            provided feature name, using the default settings,
            or based on a provided abstract embedding model that
            will be called on the provided graph.
        skip_evaluation_biased_feature: bool = False
            Whether to skip feature names that are known to be biased
            when running an holdout. These features should be computed
            exclusively on the training graph and not the entire graph.
        smoke_test: bool = False
            Whether this run should be considered a smoke test
            and therefore use the smoke test configurations for
            the provided model names and feature names.
        precompute_constant_stocastic_features: bool = False
            Whether to precompute once the constant automatic stocastic
            features before starting the embedding loop. This means that,
            when left set to false, while the features will be computed
            using the same input data, the random state between runs will
            be different and therefore the experiment performance will
            capture more of the variance derived from the stocastic aspect
            of the considered method. When set to true, they are only computed
            once and therefore the experiment will be overall faster.
        """
        if isinstance(edge_type_feature, str):
            if not allow_automatic_feature:
                raise ValueError(
                    f"The edge type feature `{edge_type_feature}` was requested, but "
                    "the `allow_automatic_feature` has been set to False. "
                    "This may be because this is an evaluation execution or "
                    "a prediction, and the string feature should be obtained "
                    "from either the training graph, the test graph or the "
                    "complete graph and it is not clear which one was provided. "
                    "Consider calling the `normalize_edge_type_features` method "
                    "yourselves to completely define your intentions."
                )

            edge_type_feature = AbstractEmbeddingModel.get_model_from_library(
                model_name=edge_type_feature
            )()

        # If this object is an implementation of an abstract
        # embedding model, we compute the embedding.
        if issubclass(edge_type_feature.__class__, AbstractEmbeddingModel):
            if skip_evaluation_biased_feature and (
                cls.task_involves_edge_types()
                and edge_type_feature.is_using_edge_types()
                or cls.task_involves_edge_types()
                and edge_type_feature.is_using_edge_types()
                or cls.task_involves_edge_weights()
                and edge_type_feature.is_using_edge_weights()
                or cls.task_involves_topology()
                and edge_type_feature.is_topological()
                or not precompute_constant_stocastic_features
                and edge_type_feature.is_stocastic()
            ):
                yield edge_type_feature
                return None

            if edge_type_feature.is_stocastic():
                edge_type_feature.set_random_state(random_state)

            if smoke_test:
                edge_type_feature = edge_type_feature.into_smoke_test()

            edge_type_feature = edge_type_feature.fit_transform(
                graph=support,
                return_dataframe=False,
            )

        if isinstance(edge_type_feature, EmbeddingResult):
            edge_type_feature = edge_type_feature.get_all_edge_type_embeddings()

        if not isinstance(edge_type_feature, list):
            edge_type_feature = [edge_type_feature]

        cls._handle_potentially_misparametrized_features(
            features=edge_type_feature,
            expected_parameter_name="edge_type_features",
            expected_number_of_elements=graph.get_number_of_edge_types(),
            expected_getter_from_index=graph.get_edge_type_name_from_edge_type_id,
            expected_has_index_name=graph.has_edge_type_name,
            graph=graph,
        )

        for edge_type_feature in edge_type_feature:
            # If it is a dataframe we align it
            if isinstance(edge_type_feature, pd.DataFrame):
                yield edge_type_feature.loc[
                    graph.get_unique_edge_type_names()
                ].to_numpy()
            else:
                # And if it is a numpy array we must believe that the user knows what
                # they are doing, as we cannot ensure alignment.
                yield edge_type_feature

    @classmethod
    def normalize_edge_type_features(
        cls,
        graph: Graph,
        support: Graph,
        random_state: int,
        edge_type_features: Optional[
            Union[
                str,
                pd.DataFrame,
                np.ndarray,
                Type[AbstractEmbeddingModel],
                List[
                    Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]
                ],
            ]
        ] = None,
        allow_automatic_feature: bool = True,
        skip_evaluation_biased_feature: bool = False,
        smoke_test: bool = False,
        precompute_constant_stocastic_features: bool = False,
    ) -> List[np.ndarray]:
        """Normalizes the provided edge type features and validates them.

        Parameters
        ------------------
        graph: Graph
            The graph to check for.
        support: Graph
            The graph describing the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological features.
        random_state: int
            The random state to use for the stochastic automatic features.
        edge_type_features: Optional[Union[str, pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]]]] = None
            The edge features to normalize.
        allow_automatic_feature: bool = True
            Whether to allow feature names creation based on the
            provided feature name, using the default settings,
            or based on a provided abstract embedding model that
            will be called on the provided graph.
        skip_evaluation_biased_feature: bool = False
            Whether to skip feature names that are known to be biased
            when running an holdout. These features should be computed
            exclusively on the training graph and not the entire graph.
        smoke_test: bool = False
            Whether this run should be considered a smoke test
            and therefore use the smoke test configurations for
            the provided model names and feature names.
        precompute_constant_stocastic_features: bool = False
            Whether to precompute once the constant automatic stocastic
            features before starting the embedding loop. This means that,
            when left set to false, while the features will be computed
            using the same input data, the random state between runs will
            be different and therefore the experiment performance will
            capture more of the variance derived from the stocastic aspect
            of the considered method. When set to true, they are only computed
            once and therefore the experiment will be overall faster.
        """
        if edge_type_features is None:
            return []

        if not isinstance(edge_type_features, (list, tuple)):
            edge_type_features = [edge_type_features]

        # If any edge type features are provided, we need to make sure that
        # the support and the graph have aligned vocabularies for what
        # entails the edge type names.
        if not support.has_compatible_edge_types_vocabularies(graph):
            raise ValueError(
                "The provided graph and support graphs do not have compatible "
                "edge type vocabularies. Please make sure that the edge type names "
                "are the same for both graphs."
            )

        # We check that the provided features are not edge features,
        # and if they are we provide a meaningful error.
        cls._handle_potentially_misparametrized_edge_features(
            features=edge_type_features,
            expected_parameter_name="edge_type_features",
        )

        return [
            normalized_edge_type_feature
            for edge_type_feature in edge_type_features
            for normalized_edge_type_feature in cls.normalize_edge_type_feature(
                graph=graph,
                support=support,
                random_state=random_state,
                edge_type_feature=edge_type_feature,
                allow_automatic_feature=allow_automatic_feature,
                skip_evaluation_biased_feature=skip_evaluation_biased_feature,
                smoke_test=smoke_test,
                precompute_constant_stocastic_features=precompute_constant_stocastic_features,
            )
        ]

    @classmethod
    def normalize_edge_feature(
        cls,
        graph: Graph,
        support: Graph,
        random_state: int,
        edge_feature: Optional[
            Union[
                str,
                pd.DataFrame,
                np.ndarray,
                EmbeddingResult,
                Type[AbstractEmbeddingModel],
            ]
        ] = None,
        allow_automatic_feature: bool = True,
        skip_evaluation_biased_feature: bool = False,
        smoke_test: bool = False,
        precompute_constant_stocastic_features: bool = False,
    ) -> List[np.ndarray]:
        """Normalizes the provided edge features and validates them.

        Parameters
        ------------------
        graph: Graph
            The graph to check for.
        support: Graph
            The graph describing the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological features.
        random_state: int
            The random state to use for the stochastic automatic features.
        edge_feature: Optional[Union[str, pd.DataFrame, np.ndarray]] = None
            The edge feature to normalize.
        allow_automatic_feature: bool = True
            Whether to allow feature names creation based on the
            provided feature name, using the default settings,
            or based on a provided abstract embedding model that
            will be called on the provided graph.
        skip_evaluation_biased_feature: bool = False
            Whether to skip feature names that are known to be biased
            when running an holdout. These features should be computed
            exclusively on the training graph and not the entire graph.
        smoke_test: bool = False
            Whether this run should be considered a smoke test
            and therefore use the smoke test configurations for
            the provided model names and feature names.
        precompute_constant_stocastic_features: bool = False
            Whether to precompute once the constant automatic stocastic
            features before starting the embedding loop. This means that,
            when left set to false, while the features will be computed
            using the same input data, the random state between runs will
            be different and therefore the experiment performance will
            capture more of the variance derived from the stocastic aspect
            of the considered method. When set to true, they are only computed
            once and therefore the experiment will be overall faster.
        """
        if isinstance(edge_feature, str):
            if not allow_automatic_feature:
                raise ValueError(
                    f"The edge feature `{edge_feature}` was requested, but "
                    "the `allow_automatic_feature` has been set to False. "
                    "This may be because this is an evaluation execution or "
                    "a prediction, and the string feature should be obtained "
                    "from either the training graph, the test graph or the "
                    "complete graph and it is not clear which one was provided. "
                    "Consider calling the `normalize_edge_features` method "
                    "yourselves to completely define your intentions."
                )

            edge_feature = AbstractEmbeddingModel.get_model_from_library(
                model_name=edge_feature, task_name="Edge Embedding"
            )()

        # If this object is an implementation of an abstract
        # embedding model, we compute the embedding.
        if issubclass(type(edge_feature), AbstractEmbeddingModel):
            if skip_evaluation_biased_feature and (
                cls.task_involves_edge_types()
                and edge_feature.is_using_edge_types()
                or cls.task_involves_node_types()
                and edge_feature.is_using_node_types()
                or cls.task_involves_edge_weights()
                and edge_feature.is_using_edge_weights()
                or cls.task_involves_topology()
                and edge_feature.is_topological()
                or not precompute_constant_stocastic_features
                and edge_feature.is_stocastic()
            ):
                yield edge_feature
                return None

            if edge_feature.is_stocastic():
                edge_feature.set_random_state(random_state)

            if smoke_test:
                edge_feature = edge_feature.into_smoke_test()

            if issubclass(type(edge_feature), AbstractEdgeFeature):
                if not edge_feature.is_fit():
                    edge_feature = edge_feature.clone()
                    edge_feature.fit(
                        graph=support,
                    )
            else:
                edge_feature = edge_feature.fit_transform(
                    graph=support,
                    return_dataframe=False,
                )

        if isinstance(edge_feature, EmbeddingResult):
            edge_feature = edge_feature.get_all_edge_embedding()

        if not isinstance(edge_feature, list):
            edge_feature = [edge_feature]

        for ef in edge_feature:
            if issubclass(type(ef), AbstractEdgeFeature):
                yield ef
                continue
            if not isinstance(ef, (np.ndarray, pd.DataFrame)):
                raise ValueError(
                    f"The provided edge features are of type `{type(ef)}`, "
                    "while we only currently support numpy arrays and pandas DataFrames. "
                    "What behaviour were you expecting with this feature? "
                    "Please do open an issue on Embiggen and let us know!"
                )

            if graph.get_number_of_edges() != ef.shape[0]:
                if graph.get_name().lower() == "graph":
                    graph_name = ""
                else:
                    graph_name = f" {graph.get_name()}"
                raise ValueError(
                    f"The provided edge features have {ef.shape[0]} rows "
                    f"but the provided graph{graph_name} has {graph.get_number_of_edges()} edges. "
                    "Maybe these features refer to another "
                    "version of the graph or another graph "
                    "entirely?"
                )

            # If it is a dataframe we align it
            if isinstance(ef, pd.DataFrame):
                yield ef.loc[graph.get_edge_names()].to_numpy()
            else:
                # And if it is a numpy array we must believe that the user knows what
                # they are doing, as we cannot ensure alignment.
                yield ef

    @classmethod
    def normalize_edge_features(
        cls,
        graph: Graph,
        support: Graph,
        random_state: int,
        edge_features: Optional[
            Union[
                str,
                pd.DataFrame,
                np.ndarray,
                Type[AbstractEmbeddingModel],
                List[
                    Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]
                ],
            ]
        ] = None,
        allow_automatic_feature: bool = True,
        skip_evaluation_biased_feature: bool = False,
        smoke_test: bool = False,
        precompute_constant_stocastic_features: bool = False,
    ) -> List[np.ndarray]:
        """Normalizes the provided edge features and validates them.

        Parameters
        ------------------
        graph: Graph
            The graph to check for.
        support: Graph
            The graph describing the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological features.
        random_state: int
            The random state to use for the stochastic automatic features.
        edge_features: Optional[Union[str, pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]] = None
            The edge features to normalize.
        allow_automatic_feature: bool = True
            Whether to allow feature names creation based on the
            provided feature name, using the default settings,
            or based on a provided abstract embedding model that
            will be called on the provided graph.
        skip_evaluation_biased_feature: bool = False
            Whether to skip feature names that are known to be biased
            when running an holdout. These features should be computed
            exclusively on the training graph and not the entire graph.
        smoke_test: bool = False
            Whether this run should be considered a smoke test
            and therefore use the smoke test configurations for
            the provided model names and feature names.
        precompute_constant_stocastic_features: bool = False
            Whether to precompute once the constant automatic stocastic
            features before starting the embedding loop. This means that,
            when left set to false, while the features will be computed
            using the same input data, the random state between runs will
            be different and therefore the experiment performance will
            capture more of the variance derived from the stocastic aspect
            of the considered method. When set to true, they are only computed
            once and therefore the experiment will be overall faster.
        """
        if edge_features is None:
            return []

        if not isinstance(edge_features, list):
            edge_features = [edge_features]

        return [
            normalized_edge_feature
            for edge_feature in edge_features
            for normalized_edge_feature in cls.normalize_edge_feature(
                graph=graph,
                support=support,
                random_state=random_state,
                edge_feature=edge_feature,
                allow_automatic_feature=allow_automatic_feature,
                skip_evaluation_biased_feature=skip_evaluation_biased_feature,
                smoke_test=smoke_test,
                precompute_constant_stocastic_features=precompute_constant_stocastic_features,
            )
        ]

    def fit(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]
        ] = None,
        node_type_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]
        ] = None,
        edge_type_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]
        ] = None,
        edge_features: Optional[
            Union[
                Type[AbstractEdgeFeature],
                pd.DataFrame,
                np.ndarray,
                List[Union[pd.DataFrame, np.ndarray]],
            ]
        ] = None,
    ):
        """Execute predictions on the provided graph.

        Parameters
        --------------------
        graph: Graph
            The graph to run predictions on.
        support: Optional[Graph] = None
            The graph describiding the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological classifiers
            such as Graph Convolutional Networks.
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node features to use.
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node type features to use.
        edge_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge type features to use.
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge features to use.
        """
        if not graph.has_nodes():
            raise ValueError("The provided graph is empty.")

        if (
            self.requires_node_types()
            or self.can_use_node_types()
            and self.is_using_node_types()
        ) and not graph.has_node_types():
            raise ValueError(
                f"The provided graph {graph.get_name()} does not have node types, but "
                f"the {self.model_name()} requires or is parametrized to use node types."
            )

        if (
            self.requires_edge_types()
            or self.can_use_edge_types()
            and self.is_using_edge_types()
        ) and not graph.has_edge_types():
            raise ValueError(
                f"The provided graph {graph.get_name()} does not have edge types, but "
                f"the {self.model_name()} requires edge types."
            )

        if (
            self.is_multilabel_prediction_task()
            and not self.supports_multilabel_prediction()
        ):
            raise ValueError(
                f"The provided model {self.model_name()} does not support multilabel prediction, "
                f"but the task {self.task_name()} requires it. There are other models available "
                "that support multilabel prediction, please do check them out."
            )

        if support is None:
            support = graph

        node_features = self.normalize_node_features(
            graph=graph,
            support=support,
            random_state=self._random_state,
            node_features=node_features,
            allow_automatic_feature=True,
        )
        self._check_node_features_shapes(node_features)
        self._check_nan(node_features, "node features")
        node_type_features = self.normalize_node_type_features(
            graph=graph,
            support=support,
            random_state=self._random_state,
            node_type_features=node_type_features,
            allow_automatic_feature=True,
        )
        self._check_node_type_features_shapes(node_type_features)
        self._check_nan(node_type_features, "node type features")
        edge_type_features = self.normalize_edge_type_features(
            graph=graph,
            support=support,
            random_state=self._random_state,
            edge_type_features=edge_type_features,
            allow_automatic_feature=True,
        )
        self._check_edge_type_features_shapes(edge_type_features)
        self._check_nan(edge_type_features, "edge type features")
        edge_features = self.normalize_edge_features(
            graph=graph,
            support=support,
            random_state=self._random_state,
            edge_features=edge_features,
            allow_automatic_feature=True,
        )

        for edge_feature in edge_features:
            if issubclass(type(edge_feature), AbstractEdgeFeature):
                assert edge_feature.is_fit()

        if len(node_type_features) > 0 and not graph.has_node_types():
            raise ValueError(
                "The node type features have been provided but the current "
                f"instance of graph {graph.get_name()} does not have node types. "
                "It is unclear how to proceed with this data."
            )
        
        if len(node_type_features) > 0 and graph.has_exclusively_homogeneous_node_types():
            raise ValueError(
                "The node type features have been provided but the current "
                f"instance of graph {graph.get_name()} has homogeneous node types. "
                "This means that all of the nodes in the graph have the same node type, "
                "and therefore all of the nodes in the graph will have the same node type "
                "features. It is unclear how to proceed with this data."
            )
        
        if len(node_type_features) > 0 and graph.has_exclusively_singleton_node_types():
            node_type_name_counts = json.dumps(graph.get_node_type_names_counts_hashmap(), indent=4)
            raise ValueError(
                "The node type features have been provided but the current "
                f"instance of graph {graph.get_name()} has exclusively singleton node types, "
                "meaning that all of the nodes in the graph have a unique node type. "
                f"Specifically, this means that the node type counts of your graph as as follows: {node_type_name_counts}"
                "This means that the node type features will effectively be the same as "
                "the node features. We recommend that you use such features directly as "
                "node features instead of node type features so as to avoid confusion."
            )

        if len(edge_type_features) > 0 and not graph.has_edge_types():
            raise ValueError(
                "The edge type features have been provided but the current "
                f"instance of graph {graph.get_name()} does not have edge types. "
                "It is unclear how to proceed with this data."
            )
        
        if len(edge_type_features) > 0 and graph.has_exclusively_homogeneous_edge_types():
            raise ValueError(
                "The edge type features have been provided but the current "
                f"instance of graph {graph.get_name()} has homogeneous edge types. "
                "This means that all of the edges in the graph have the same edge type, "
                "and therefore all of the edges in the graph will have the same edge type "
                "features. It is unclear how to proceed with this data."
            )
        
        if len(edge_type_features) > 0 and graph.has_exclusively_singleton_edge_types():
            raise ValueError(
                "The edge type features have been provided but the current "
                f"instance of graph {graph.get_name()} has exclusively singleton edge types, "
                "meaning that all of the edges in the graph have a unique edge type. "
                "This means that the edge type features will effectively be the same as "
                "the edge features. We recommend that you use such features directly as "
                "edge features instead of edge type features so as to avoid confusion."
            )

        self._is_using_node_type_features = len(node_type_features) > 0
        self._is_using_edge_type_features = len(edge_type_features) > 0

        if len(node_type_features) > 0 and not self.can_use_node_type_features():
            raise ValueError(
                f"The current model {self.model_name()} for task {self.task_name()} "
                f"from library {self.library_name()} "
                "does not support node type features, "
                f"but you provided {len(node_type_features)} node type features. "
            )

        if len(edge_type_features) > 0 and not self.can_use_edge_type_features():
            raise ValueError(
                f"The current model {self.model_name()} for task {self.task_name()} "
                f"from library {self.library_name()} "
                "does not support edge type features, "
                f"but you provided {len(edge_type_features)} edge type features. "
            )

        if len(edge_features) > 0 and not self.can_use_edge_features():
            raise ValueError(
                f"The current model {self.model_name()} for task {self.task_name()} "
                f"from library {self.library_name()} "
                "does not support edge features, "
                f"but you provided {len(edge_features)} edge features. "
            )
        
        self._training_graph_density = support.get_density()

        try:
            self._fit(
                graph=graph,
                support=support,
                node_features=node_features,
                node_type_features=node_type_features,
                edge_type_features=edge_type_features,
                edge_features=edge_features,
            )
        except Exception as exception:
            raise RuntimeError(
                f"An exception was raised while calling the `_fit` method of {self.model_name()} "
                f"implemented using the {self.library_name()} for the {self.task_name()} task. "
                f"Specifically, the class of the model is {self.__class__.__name__}."
            ) from exception

        self._fitting_was_executed = True

    def predict(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]
        ] = None,
        node_type_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]
        ] = None,
        edge_type_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]
        ] = None,
        edge_features: Optional[
            Union[
                Type[AbstractEdgeFeature],
                pd.DataFrame,
                np.ndarray,
                List[Union[pd.DataFrame, np.ndarray]],
            ]
        ] = None,
    ) -> np.ndarray:
        """Execute predictions on the provided graph.

        Parameters
        --------------------
        graph: Graph
            The graph to run predictions on.
        support: Optional[Graph] = None
            The graph describiding the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological classifiers
            such as Graph Convolutional Networks.
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node features to use.
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node type features to use.
        edge_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge type features to use.
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge features to use.
        """
        if not graph.has_nodes():
            raise ValueError("The provided graph is empty.")

        if not self._fitting_was_executed:
            raise ValueError(
                (
                    "The prediction cannot be executed without "
                    "having first executed the fitting of the model. "
                    "Do call the `.fit` method before the `.predict` "
                    "method."
                )
            )

        if support is None:
            support = graph

        node_features = self.normalize_node_features(
            graph=graph,
            support=support,
            random_state=self._random_state,
            node_features=node_features,
            allow_automatic_feature=False,
        )
        self._check_node_features_shapes(node_features)
        self._check_nan(node_features, "node features")
        node_type_features = self.normalize_node_type_features(
            graph=graph,
            support=support,
            random_state=self._random_state,
            node_type_features=node_type_features,
            allow_automatic_feature=False,
        )
        self._check_node_type_features_shapes(node_type_features)
        self._check_nan(node_type_features, "node type features")
        edge_type_features = self.normalize_edge_type_features(
            graph=graph,
            support=support,
            random_state=self._random_state,
            edge_type_features=edge_type_features,
            allow_automatic_feature=False,
        )
        self._check_edge_type_features_shapes(edge_type_features)
        self._check_nan(edge_type_features, "edge type features")
        edge_features = self.normalize_edge_features(
            graph=graph,
            support=support,
            random_state=self._random_state,
            edge_features=edge_features,
            allow_automatic_feature=False,
        )

        if self._training_graph_density > support.get_density() * 3.0 or self._training_graph_density < support.get_density() / 3.0:
            raise ValueError(
                f"The density of the support graph has changed too much from the training graph. "
                f"The density of the training graph was {self._training_graph_density} while the "
                f"density of the support graph is {support.get_density()}. This may be due to a "
                f"change in the graph structure or the provided support graph is not the one used "
                f"during training. If you are using the same graph, please do provide the same "
                f"support graph during prediction as you did during training."
            )

        try:
            predictions = self._predict(
                graph=graph,
                support=support,
                node_features=node_features,
                node_type_features=node_type_features,
                edge_type_features=edge_type_features,
                edge_features=edge_features,
            )
        except Exception as exception:
            raise RuntimeError(
                f"An exception was raised while calling the `._predict` method of {self.model_name()} "
                f"implemented using the {self.library_name()} for the {self.task_name()} task. "
                f"Specifically, the class of the model is {self.__class__.__name__}."
            ) from exception

        return predictions

    def predict_proba(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]
        ] = None,
        node_type_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]
        ] = None,
        edge_type_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]
        ] = None,
        edge_features: Optional[
            Union[
                Type[AbstractEdgeFeature],
                pd.DataFrame,
                np.ndarray,
                List[Union[pd.DataFrame, np.ndarray]],
            ]
        ] = None,
    ) -> Union[np.ndarray, Iterator[np.ndarray]]:
        """Execute predictions on the provided graph.

        Parameters
        --------------------
        graph: Graph
            The graph to run predictions on.
        support: Optional[Graph] = None
            The graph describiding the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological classifiers
            such as Graph Convolutional Networks.
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node features to use.
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node type features to use.
        edge_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge type features to use.
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge features to use.
        """
        if not graph.has_nodes():
            raise ValueError("The provided graph is empty.")

        if not self._fitting_was_executed:
            raise ValueError(
                (
                    "The prediction cannot be executed without "
                    "having first executed the fitting of the model. "
                    "Do call the `.fit` method before the `.predict_proba` "
                    "method."
                )
            )

        if support is None:
            support = graph

        node_features = self.normalize_node_features(
            graph=graph,
            support=support,
            random_state=self._random_state,
            node_features=node_features,
            allow_automatic_feature=False,
        )
        self._check_node_features_shapes(node_features)
        self._check_nan(node_features, "node features")
        node_type_features = self.normalize_node_type_features(
            graph=graph,
            support=support,
            random_state=self._random_state,
            node_type_features=node_type_features,
            allow_automatic_feature=False,
        )
        self._check_node_type_features_shapes(node_type_features)
        self._check_nan(node_type_features, "node type features")
        edge_type_features = self.normalize_edge_type_features(
            graph=graph,
            support=support,
            random_state=self._random_state,
            edge_type_features=edge_type_features,
            allow_automatic_feature=False,
        )
        self._check_edge_type_features_shapes(edge_type_features)
        self._check_nan(edge_type_features, "edge type features")

        if self._training_graph_density > support.get_density() * 3.0 or self._training_graph_density < support.get_density() / 3.0:
            raise ValueError(
                f"The density of the support graph has changed too much from the training graph. "
                f"The density of the training graph was {self._training_graph_density} while the "
                f"density of the support graph is {support.get_density()}. This may be due to a "
                f"change in the graph structure or the provided support graph is not the one used "
                f"during training. If you are using the same graph, please do provide the same "
                f"support graph during prediction as you did during training."
            )

        try:
            predictions: Union[np.ndarray, Iterator[np.ndarray]] = self._predict_proba(
                graph=graph,
                support=support,
                node_features=node_features,
                node_type_features=node_type_features,
                edge_type_features=edge_type_features,
                edge_features=self.normalize_edge_features(
                    graph=graph,
                    support=support,
                    random_state=self._random_state,
                    edge_features=edge_features,
                    allow_automatic_feature=False,
                ),
            )
            if isinstance(predictions, np.ndarray):
                if np.isnan(predictions).any():
                    # If the predictions have the terrible misfortune of having NaN values,
                    # we raise an extensive error including all of the information that we have
                    # about the graph and the current model, and how many NaN values there are.
                    raise ValueError(
                        f"The predictions for the graph {graph.get_name()} and the model {self.model_name()} "
                        f"from the library {self.library_name()} and task {self.task_name()} have NaN values. "
                        f"Specifically, there are {np.isnan(predictions).sum()} NaN values out of {len(predictions)} predictions."
                    )
                
                if (
                    not self.is_binary_prediction_task()
                    and not self.is_multilabel_prediction_task()
                    and (len(predictions.shape) == 1 or predictions.shape[1] == 2)
                ):
                    raise ValueError(
                        "This task is not a binary prediction, "
                        f"yet the {self.model_name()} model predict proba method has "
                        "returned a vector of prediction probabilities with "
                        f"shape {predictions.shape}. "
                    )
        except Exception as exception:
            raise RuntimeError(
                f"An exception was raised while calling the `._predict_proba` method of {self.model_name()} "
                f"implemented using the {self.library_name()} for the {self.task_name()} task. "
                f"Specifically, the class of the model is {self.__class__.__name__}."
            ) from exception

        return predictions

    def evaluate_predictions(
        self,
        ground_truth: np.ndarray,
        predictions: np.ndarray,
    ) -> Dict[str, Any]:
        """Return evaluations for the provided predictions.

        Parameters
        ----------------
        ground_truth: np.ndarray
            The ground truth to evaluate the predictions against.
        predictions: np.ndarray
            The predictions to be evaluated.
        """
        if self.is_binary_prediction_task():
            return express_measures.all_binary_metrics(
                ground_truth.flatten(), predictions.flatten()
            )

        return {
            **{
                metric.__name__: metric(ground_truth, predictions)
                for metric in (
                    accuracy_score,
                    hamming_loss,
                    *(
                        ()
                        if self.is_multilabel_prediction_task()
                        else (balanced_accuracy_score,)
                    ),
                )
            },
            **{
                metric.__name__: metric(
                    ground_truth, predictions, average="macro", zero_division=0
                )
                for metric in (
                    f1_score,
                    precision_score,
                    recall_score,
                )
            },
        }

    def evaluate_prediction_probabilities(
        self,
        ground_truth: np.ndarray,
        prediction_probabilities: np.ndarray,
    ) -> Dict[str, Any]:
        """Return evaluations for the provided predictions.

        Parameters
        ----------------
        ground_truth: np.ndarray
            The ground truth to evaluate the predictions against.
        prediction_probabilities: np.ndarray
            The predictions to be evaluated.
        """
        if self.is_binary_prediction_task():
            return {
                "auroc": express_measures.binary_auroc(
                    ground_truth.flatten(), prediction_probabilities.flatten()
                ),
                "auprc": express_measures.binary_auprc(
                    ground_truth.flatten(), prediction_probabilities.flatten()
                ),
            }

        @functools.wraps(roc_auc_score)
        def wrapper_roc_auc_score(*args, **kwargs):
            return roc_auc_score(*args, **kwargs, multi_class="ovr")

        return {"auroc": wrapper_roc_auc_score(ground_truth, prediction_probabilities)}

    @classmethod
    def split_graph_following_evaluation_schema(
        cls,
        graph: Graph,
        evaluation_schema: str,
        holdout_number: int,
        number_of_holdouts: int,
        **holdouts_kwargs: Dict,
    ) -> Tuple[Graph]:
        """Return train and test graphs tuple following the provided evaluation schema.

        Parameters
        ----------------------
        graph: Graph
            The graph to split.
        evaluation_schema: str
            The evaluation schema to follow.
        holdout_number: int
            The current holdout number.
        number_of_holdouts: int
            The total number of holdouts.
        holdouts_kwargs: Dict[str, Any]
            The kwargs to be forwarded to the holdout method.
        """
        must_be_in_set(
            evaluation_schema,
            cls.get_available_evaluation_schemas(),
            f"evaluation schema for {cls.task_name()}",
        )

    def _evaluate(
        self,
        graph: Graph,
        train: Graph,
        test: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]
        ] = None,
        node_type_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]
        ] = None,
        edge_type_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]
        ] = None,
        edge_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]
        ] = None,
        subgraph_of_interest: Optional[Graph] = None,
        random_state: int = 42,
        verbose: bool = True,
        **kwargs: Dict,
    ) -> List[Dict[str, Any]]:
        """Return model evaluation on the provided graphs."""
        raise NotImplementedError(
            "The _evaluate method should be implemented in the child "
            "classes of abstract classifier model."
        )

    @classmethod
    def _prepare_evaluation(
        cls,
        graph: Graph,
        train: Graph,
        test: Graph,
        support: Optional[Graph] = None,
        subgraph_of_interest: Optional[Graph] = None,
        random_state: int = 42,
        verbose: bool = True,
        **kwargs: Dict,
    ) -> Dict[str, Any]:
        """Return additional custom parameters for the current holdout."""
        raise NotImplementedError(
            "The _evaluate method should be implemented in the child "
            "classes of abstract classifier model."
        )

    @classmethod
    def iterate_classifier_models(
        cls,
        models: Union[
            str, Type["AbstractClassifierModel"], List[Type["AbstractClassifierModel"]]
        ],
        library_names: Optional[Union[str, List[str]]],
        smoke_test: bool,
    ) -> Iterator[Type["AbstractClassifierModel"]]:
        """Return iterator over the provided models after validation.

        Parameters
        -------------------
        models: Union[Type[AbstractClassifierModel], List[Type[AbstractClassifierModel]]]
            The models to validate and iterate on.
        expected_parent_class: Type[AbstractClassifierModel]
            The parent class to check the model against.
        library_names: Optional[Union[str, List[str]]] = None
            Library names from where to retrieve the provided model names.
        smoke_test: bool = False
            Whether this run should be considered a smoke test
            and therefore use the smoke test configurations for
            the provided model names and feature names.
        """
        if not isinstance(models, (list, tuple, pd.Series)):
            models = [models]

        number_of_models = len(models)

        if not isinstance(library_names, (list, tuple, pd.Series)):
            library_names = [library_names] * number_of_models

        if number_of_models == 0:
            raise ValueError("An empty list of models was provided.")

        number_of_libraries = len(library_names)

        if number_of_libraries != number_of_models:
            raise ValueError(
                f"The number of the provided models {number_of_models} "
                f"is different from the number of provided libraries {number_of_libraries}."
            )

        models = [
            cls.get_model_from_library(
                model, task_name=cls.task_name(), library_name=library_name
            )()
            if isinstance(model, str)
            else model
            for model, library_name in zip(models, library_names)
        ]

        for model in models:
            if not issubclass(model.__class__, cls):
                raise ValueError(
                    "The provided classifier model is expected to be "
                    f"an implementation of the {cls.__name__} class, but you provided "
                    f"an object of type {type(model)} that does not hereditate from "
                    "the expected class. If you are using a model provided from the GRAPE "
                    "library and you see this error, you should report it on the GitHub "
                    "repository of the library. If you are using a custom model, you should "
                    "check that you are correctly implementing the required abstract class "
                    "methods, such as the `_fit` and `_predict` methods."
                )

        # If this is a smoke test, we replace all of the
        # provided models with their smoke test version.
        if smoke_test:
            models = [
                model.__class__(**model.smoke_test_parameters()) for model in models
            ]

        bar = tqdm(
            models,
            total=number_of_models,
            disable=number_of_models == 1,
            dynamic_ncols=True,
            leave=False,
        )

        for model in bar:
            bar.set_description(
                f"Evaluating model {model.model_name()} from library {model.library_name()} on {model.task_name()}"
            )
            yield model.clone()

    @Cache(
        cache_path="{cache_dir}/{self.task_name()}/{graph.get_name()}/holdout_{holdout_number}/{self.model_name()}/{self.library_name()}/{_hash}.csv.gz",
        cache_dir="experiments",
        enable_cache_arg_name="enable_cache",
        args_to_ignore=[
            "verbose",
            "smoke_test",
            "train_of_interest",
            "test_of_interest",
            "train",
            "metadata",
        ],
        capture_enable_cache_arg_name=True,
        use_approximated_hash=True,
    )
    def _train_and_evaluate_model(
        self,
        graph: Graph,
        train_of_interest: Graph,
        test_of_interest: Graph,
        train: Graph,
        subgraph_of_interest: Graph,
        use_subgraph_as_support: bool,
        node_features: Optional[List[np.ndarray]],
        node_type_features: Optional[List[np.ndarray]],
        edge_type_features: Optional[List[np.ndarray]],
        edge_features: Optional[List[np.ndarray]],
        random_state: int,
        holdout_number: int,
        evaluation_schema: str,
        holdouts_kwargs: Dict[str, Any],
        features_names: List[str],
        features_parameters: Dict[str, Any],
        metadata: Dict[str, Any],
        **validation_kwargs,
    ) -> pd.DataFrame:
        """Run inner training and evaluation."""
        if self.is_stocastic():
            self.set_random_state(random_state * (holdout_number + 1))
        # Fit the model using the training graph
        training_start = time.time()
        self.fit(
            graph=train_of_interest,
            support=train_of_interest if use_subgraph_as_support else train,
            node_features=node_features,
            node_type_features=node_type_features,
            edge_type_features=edge_type_features,
            edge_features=edge_features,
        )
        time_required_for_training = time.time() - training_start

        start_evaluation = time.time()

        try:
            # We add the newly computed performance.
            model_performance = pd.DataFrame(
                self._evaluate(
                    graph=graph,
                    support=train_of_interest if use_subgraph_as_support else train,
                    train=train_of_interest,
                    test=test_of_interest,
                    node_features=node_features,
                    node_type_features=node_type_features,
                    edge_type_features=edge_type_features,
                    edge_features=edge_features,
                    subgraph_of_interest=subgraph_of_interest,
                    random_state=random_state * holdout_number,
                    verbose=False,
                    **validation_kwargs,
                )
            ).reset_index(drop=True)
        except RuntimeError as exception:
            raise exception
        except Exception as exception:
            raise RuntimeError(
                f"An exception was raised while calling the `._evaluate` method of {self.model_name()} "
                f"implemented using the {self.library_name()} for the {self.task_name()} task. "
                f"Specifically, the class of the model is {self.__class__.__name__}. "
            ) from exception

        time_required_for_evaluation = time.time() - start_evaluation

        model_performance["time_required_for_training"] = time_required_for_training
        model_performance["time_required_for_evaluation"] = time_required_for_evaluation
        model_performance["time"] = time.time()
        model_performance["task_name"] = self.task_name()
        model_performance["model_name"] = self.model_name()
        model_performance["library_name"] = self.library_name()
        model_performance["graph_name"] = graph.get_name()
        model_performance["nodes_number"] = graph.get_number_of_nodes()
        model_performance["edges_number"] = graph.get_number_of_directed_edges()
        model_performance["evaluation_schema"] = evaluation_schema
        model_performance["holdout_number"] = holdout_number
        model_performance["holdouts_kwargs"] = json.dumps(holdouts_kwargs)
        model_performance["use_subgraph_as_support"] = use_subgraph_as_support
        model_performance["node_feature_shapes"] = json.dumps([self._node_feature_shapes])
        model_performance["node_type_feature_shapes"] = json.dumps([self._node_type_feature_shapes])
        model_performance["edge_type_feature_shapes"] = json.dumps([self._edge_type_feature_shapes])

        for column_name, column_value in metadata.items():
            model_performance[column_name] = column_value

        df_model_parameters = pd.DataFrame(dict(), index=model_performance.index)
        df_features_parameters = pd.DataFrame(dict(), index=model_performance.index)

        for parameter_name, parameter_value in self.parameters().items():
            if isinstance(parameter_value, (list, tuple)):
                parameter_value = str(parameter_value)
            df_model_parameters[parameter_name] = parameter_value

        df_model_parameters.columns = [
            ["model_parameters"] * len(df_model_parameters.columns),
            df_model_parameters.columns,
        ]

        model_performance["features_names"] = format_list(features_names)

        for parameter, value in features_parameters.items():
            if parameter in df_features_parameters.columns:
                raise ValueError(
                    "There has been a collision between the parameters used in "
                    "one of the embedding models and the parameter "
                    "used for the validation and reporting of the task itself. "
                    f"The parameter that has caused the collision is {parameter}. "
                    "Please do change the name of the parameter in your model."
                )
            df_features_parameters[parameter] = str(value)

        df_features_parameters.columns = [
            ["features_parameters"] * len(df_features_parameters.columns),
            df_features_parameters.columns,
        ]

        model_performance = pd.concat(
            [model_performance, df_model_parameters, df_features_parameters], axis=1
        )

        return model_performance

    @classmethod
    @Cache(
        cache_path="{cache_dir}/{cls.task_name()}/{graph.get_name()}/holdout_{holdout_number}/{_hash}.csv.gz",
        cache_dir="experiments",
        enable_cache_arg_name="enable_cache",
        args_to_ignore=["verbose", "smoke_test", "number_of_holdouts", "metadata"],
        capture_enable_cache_arg_name=False,
        use_approximated_hash=True,
    )
    def _evaluate_on_single_holdout(
        cls,
        models: Union[
            Type["AbstractClassifierModel"], List[Type["AbstractClassifierModel"]]
        ],
        library_names: Optional[Union[str, List[str]]],
        graph: Graph,
        subgraph_of_interest: Graph,
        use_subgraph_as_support: bool,
        node_features: Optional[List[np.ndarray]],
        node_type_features: Optional[List[np.ndarray]],
        edge_type_features: Optional[List[np.ndarray]],
        edge_features: Optional[List[np.ndarray]],
        node_features_preprocessing_steps: Optional[
            Union[
                Type[AbstractFeaturePreprocessor],
                List[Type[AbstractFeaturePreprocessor]],
            ]
        ],
        random_state: int,
        holdout_number: int,
        number_of_holdouts: int,
        evaluation_schema: str,
        enable_cache: bool,
        smoke_test: bool,
        holdouts_kwargs: Dict[str, Any],
        subgraph_of_interest_has_compatible_nodes: Optional[bool],
        features_names: List[str],
        features_parameters: Dict[str, Any],
        metadata: Dict[str, Any],
        verbose: bool,
        **validation_kwargs,
    ) -> pd.DataFrame:
        starting_setting_up_holdout = time.time()

        # We create the graph split using the provided schema.
        train, test = cls.split_graph_following_evaluation_schema(
            graph=graph,
            evaluation_schema=evaluation_schema,
            random_state=random_state,
            holdout_number=holdout_number,
            number_of_holdouts=number_of_holdouts,
            **holdouts_kwargs,
        )

        # We compute the remaining features
        starting_to_compute_node_features = time.time()
        holdout_node_features = cls.normalize_node_features(
            graph=train,
            support=train,
            random_state=random_state * (holdout_number + 1),
            node_features=node_features,
            node_features_preprocessing_steps=node_features_preprocessing_steps,
            allow_automatic_feature=True,
            skip_evaluation_biased_feature=False,
            smoke_test=smoke_test,
            precompute_constant_stocastic_features=True,
        )
        time_required_to_compute_node_features = (
            time.time() - starting_to_compute_node_features
        )

        # We compute the remaining features
        starting_to_compute_node_type_features = time.time()
        holdout_node_type_features = cls.normalize_node_type_features(
            graph=train,
            support=train,
            random_state=random_state * (holdout_number + 1),
            node_type_features=node_type_features,
            allow_automatic_feature=True,
            skip_evaluation_biased_feature=False,
            smoke_test=smoke_test,
            precompute_constant_stocastic_features=True,
        )
        time_required_to_compute_node_type_features = (
            time.time() - starting_to_compute_node_type_features
        )

        # We compute the remaining features
        starting_to_compute_edge_type_features = time.time()
        holdout_edge_type_features = cls.normalize_edge_type_features(
            graph=train,
            support=train,
            random_state=random_state * (holdout_number + 1),
            edge_type_features=edge_type_features,
            allow_automatic_feature=True,
            skip_evaluation_biased_feature=False,
            smoke_test=smoke_test,
            precompute_constant_stocastic_features=True,
        )
        time_required_to_compute_edge_type_features = (
            time.time() - starting_to_compute_edge_type_features
        )

        # We execute the same thing as described above,
        # but now for the edge features instead that for
        # the node features.
        starting_to_compute_edge_features = time.time()
        holdout_edge_features = cls.normalize_edge_features(
            graph=train,
            support=train,
            random_state=random_state * (holdout_number + 1),
            edge_features=edge_features,
            allow_automatic_feature=True,
            skip_evaluation_biased_feature=False,
            smoke_test=smoke_test,
            precompute_constant_stocastic_features=True,
        )
        time_required_to_compute_edge_features = (
            time.time() - starting_to_compute_edge_features
        )

        if subgraph_of_interest is not None:
            # First we align the train and test graph to have
            # the same node dictionary of the subgraph of interest
            # when the subgraph of interest does not have
            # the same node dictionary as the original graph.
            if not subgraph_of_interest_has_compatible_nodes:
                train = train.filter_from_names(
                    node_names_to_keep_from_graph=subgraph_of_interest
                )
                test = test.filter_from_names(
                    node_names_to_keep_from_graph=subgraph_of_interest
                )

                # We adjust the node features to only include the node features
                # that the subgraph of interest allows us to use.
                if holdout_node_features is not None:
                    # We obtain the mapping from the old to the new node IDs
                    node_ids_mapping = train.get_node_ids_mapping_from_graph(graph)

                    holdout_node_features = [
                        holdout_node_feature[node_ids_mapping]
                        for holdout_node_feature in holdout_node_features
                    ]

            train_of_interest = train & subgraph_of_interest
            test_of_interest = test & subgraph_of_interest

            # We validate that the two graphs are still
            # valid for this task.
            for graph_partition, graph_partition_name in (
                (train_of_interest, "train"),
                (test_of_interest, "test"),
            ):
                if not graph_partition.has_nodes():
                    raise ValueError(
                        f"The {graph_partition_name} graph {graph_partition.get_name()} obtained from the evaluation "
                        f"schema {evaluation_schema}, once filtered using the provided "
                        "subgraph of interest, does not have any more nodes."
                    )
                if (
                    cls.task_name() in ("Edge Prediction", "Edge Label Prediction")
                    and not graph_partition.has_edges()
                ):
                    raise ValueError(
                        f"The {graph_partition_name} graph {graph_partition.get_name()} obtained from the evaluation "
                        f"schema {evaluation_schema}, once filtered using the provided "
                        "subgraph of interest, does not have any more edges which are "
                        f"essential when running a {cls.task_name()} task."
                    )
        else:
            train_of_interest = train
            test_of_interest = test

        additional_validation_kwargs = cls._prepare_evaluation(
            graph=graph,
            support=train,
            train=train_of_interest,
            test=test_of_interest,
            subgraph_of_interest=subgraph_of_interest,
            random_state=random_state * holdout_number,
            verbose=verbose,
            **validation_kwargs,
        )

        time_required_for_setting_up_holdout = time.time() - starting_setting_up_holdout

        metadata = dict(
            **metadata,
            time_required_for_setting_up_holdout=time_required_for_setting_up_holdout,
            time_required_to_compute_node_features=time_required_to_compute_node_features,
            time_required_to_compute_node_type_features=time_required_to_compute_node_type_features,
            time_required_to_compute_edge_type_features=time_required_to_compute_edge_type_features,
            time_required_to_compute_edge_features=time_required_to_compute_edge_features,
        )

        holdout_performance = pd.concat(
            [
                classifier._train_and_evaluate_model(
                    graph=graph,
                    train_of_interest=train_of_interest,
                    test_of_interest=test_of_interest,
                    train=train,
                    subgraph_of_interest=subgraph_of_interest,
                    use_subgraph_as_support=use_subgraph_as_support,
                    node_features=holdout_node_features,
                    node_type_features=holdout_node_type_features,
                    edge_type_features=holdout_edge_type_features,
                    edge_features=holdout_edge_features,
                    random_state=random_state,
                    holdout_number=holdout_number,
                    evaluation_schema=evaluation_schema,
                    holdouts_kwargs=holdouts_kwargs,
                    enable_cache=enable_cache,
                    features_names=features_names,
                    features_parameters=features_parameters,
                    metadata=metadata.copy(),
                    **additional_validation_kwargs,
                    **validation_kwargs,
                )
                for classifier in cls.iterate_classifier_models(
                    models=models, library_names=library_names, smoke_test=smoke_test
                )
            ]
        )

        return holdout_performance

    @classmethod
    @Cache(
        cache_path="{cache_dir}/{cls.task_name()}/{graph.get_name()}/{_hash}.csv.gz",
        cache_dir="experiments",
        enable_cache_arg_name="enable_top_layer_cache",
        args_to_ignore=["verbose", "smoke_test"],
        capture_enable_cache_arg_name=True,
        use_approximated_hash=True,
    )
    def evaluate(
        cls,
        models: Union[
            Type["AbstractClassifierModel"], List[Type["AbstractClassifierModel"]]
        ],
        graph: Graph,
        evaluation_schema: str,
        holdouts_kwargs: Dict[str, Any],
        library_names: Optional[Union[str, List[str]]] = None,
        node_features: Optional[
            Union[
                str,
                pd.DataFrame,
                np.ndarray,
                Type[AbstractEmbeddingModel],
                List[
                    Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]
                ],
            ]
        ] = None,
        node_type_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]
        ] = None,
        edge_type_features: Optional[
            Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]
        ] = None,
        edge_features: Optional[
            Union[
                Type[AbstractEdgeFeature],
                str,
                pd.DataFrame,
                np.ndarray,
                List[Union[str, pd.DataFrame, np.ndarray]],
            ]
        ] = None,
        node_features_preprocessing_steps: Optional[
            Union[
                Type[AbstractFeaturePreprocessor],
                List[Type[AbstractFeaturePreprocessor]],
            ]
        ] = None,
        subgraph_of_interest: Optional[Graph] = None,
        use_subgraph_as_support: bool = False,
        number_of_holdouts: int = 10,
        random_state: int = 42,
        verbose: bool = True,
        enable_cache: bool = False,
        precompute_constant_stocastic_features: bool = False,
        smoke_test: bool = False,
        number_of_slurm_nodes: Optional[int] = None,
        slurm_node_id_variable: str = "SLURM_GRAPE_ID",
        **validation_kwargs: Dict,
    ) -> pd.DataFrame:
        """Execute evaluation on the provided graph.

        Parameters
        --------------------
        models: Union[Type["AbstractClassifierModel"], List[Type["AbstractClassifierModel"]]]
            The model(s) to be evaluated.
        graph: Graph
            The graph to run predictions on.
        evaluation_schema: str
            The schema for the evaluation to follow.
        holdouts_kwargs: Dict[str, Any]
            Parameters to forward to the desired evaluation schema.
        library_names: Optional[Union[str, List[str]]] = None
            The library names of the models, needed when a desired model is implemented in multiple
            libraries and it is unclear which one to use.
        node_features: Optional[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel], List[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]]]] = None
            The node features to use.
        node_type_features: Optional[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel], List[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]]]] = None
            The node features to use.
        edge_type_features: Optional[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEdgeFeature], List[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEdgeFeature]]]]] = None
            The edge features to use.
        edge_features: Optional[Union[str, pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]] = None
            The edge features to use.
        subgraph_of_interest: Optional[Graph] = None
            Optional subgraph where to focus the task.
            This is applied to the train and test graph
            after the desired holdout schema is applied.
        use_subgraph_as_support: bool = False
            Whether to use the provided subgraph as support or
            to use the train graph (not filtered by the subgraph).
        skip_evaluation_biased_feature: bool = False
            Whether to skip feature names that are known to be biased
            when running an holdout. These features should be computed
            exclusively on the training graph and not the entire graph.
        number_of_holdouts: int = 10
            The number of holdouts to execute.
        random_state: int = 42
            The random state to use for the holdouts.
        verbose: bool = True
            Whether to show a loading bar while computing holdouts.
        enable_cache: bool = False
            Whether to enable the cache.
        precompute_constant_stocastic_features: bool = False
            Whether to precompute once the constant automatic stocastic
            features before starting the embedding loop. This means that,
            when left set to false, while the features will be computed
            using the same input data, the random state between runs will
            be different and therefore the experiment performance will
            capture more of the variance derived from the stocastic aspect
            of the considered method. When set to true, they are only computed
            once and therefore the experiment will be overall faster.
        smoke_test: bool = False
            Whether this run should be considered a smoke test
            and therefore use the smoke test configurations for
            the provided model names and feature names.
        number_of_slurm_nodes: Optional[int] = None
            Number of SLURM nodes to consider as available.
            This variable is used to parallelize the holdouts accordingly.
        slurm_node_id_variable: str = "SLURM_GRAPE_ID"
            Name of the system variable to use as SLURM node id.
            It must be set in the slurm bash script.
        **validation_kwargs: Dict
            kwargs to be forwarded to the model `_evaluate` method.
        """
        if not isinstance(number_of_holdouts, int) or number_of_holdouts <= 0:
            raise ValueError(
                "The number of holdouts must be a strictly positive integer, "
                f"but {number_of_holdouts} was provided."
            )

        if subgraph_of_interest is not None:
            if cls.task_name() not in ("Edge Prediction", "Edge Label Prediction"):
                raise ValueError(
                    "A subgraph of interest was provided, but this parameter "
                    "is only currently supported for Edge Prediction and "
                    f"Edge Label Prediction tasks and not the {cls.task_name()} task."
                )

            if not graph.contains(subgraph_of_interest):
                raise ValueError(
                    "The provided subgraph of interest is not "
                    f"contained in the provided graph {graph.get_name()}. "
                    "Potentially you edited the graph and removed some nodes "
                    "or edges in the graph processing step, such as reoving the "
                    "connected components, self-loops, multi-edges or dentritic "
                    "elements?"
                )

            if not subgraph_of_interest.has_edges():
                raise ValueError(
                    "The provided subgraph of interest does not have any edges!"
                )

            # We check whether the subgraph of interest shares the same vocabulary
            # of the main graph. If this is true, we can skip the filtering step to
            # drop the nodes from the train and test graph.
            subgraph_of_interest_has_compatible_nodes = (
                graph.has_compatible_node_vocabularies(subgraph_of_interest)
            )
        else:
            if use_subgraph_as_support:
                raise ValueError(
                    "No subgraph of interest was provided but "
                    "it has been requested to use the subgraph "
                    "of interest as support. It is not clear "
                    "how to proceed."
                )
            subgraph_of_interest_has_compatible_nodes = None

        if number_of_slurm_nodes is not None:
            must_be_in_slurm_node()
            if not isinstance(number_of_slurm_nodes, int) or number_of_slurm_nodes <= 0:
                raise ValueError(
                    "The number of SLURM nodes must be a positive integer value."
                )
            if number_of_holdouts > number_of_slurm_nodes:
                raise ValueError(
                    "Please be advised that you are currently running an excessive "
                    "parametrization of the SLURM cluster. We currently can only parallelize "
                    "the execution of different holdouts. "
                    f"The number of holdouts requested are {number_of_holdouts} but you are "
                    f"currently using {number_of_slurm_nodes} SLURM nodes! "
                    "Possibly, you are currently running a task such as a grid search "
                    "and therefore you intend us to parallelize only the sub-segment of SLURM "
                    "nodes necessary to run the holdouts."
                )

        # Retrieve the set of provided automatic features parameters
        # so we can put them in the report.
        features_parameters = {
            parameter_name: value
            for features in (
                node_features
                if isinstance(node_features, (list, tuple))
                else (node_features,),
                node_type_features
                if isinstance(node_type_features, (list, tuple))
                else (node_type_features,),
                edge_features
                if isinstance(edge_features, (list, tuple))
                else (edge_features,),
            )
            for feature in features
            if issubclass(feature.__class__, AbstractModel)
            for parameter_name, value in feature.parameters().items()
        }

        # Retrieve the set of provided automatic features names
        # so we can put them in the report.
        features_names = list(
            {
                feature.model_name()
                for features in (
                    node_features
                    if isinstance(node_features, (list, tuple))
                    else (node_features,),
                    node_type_features
                    if isinstance(node_type_features, (list, tuple))
                    else (node_type_features,),
                    edge_features
                    if isinstance(edge_features, (list, tuple))
                    else (edge_features,),
                )
                for feature in features
                if issubclass(feature.__class__, AbstractEmbeddingModel)
            }
        )

        # We normalize and/or compute the node features, having
        # the care of skipping the features that induce bias when
        # computed on the entire graph.
        # This way we compute only once the features that do not
        # cause biases for this task, while recomputing those
        # that cause biases at each holdout, avoiding said biases.
        starting_to_compute_constant_node_features = time.time()
        node_features = cls.normalize_node_features(
            graph=graph,
            support=graph,
            random_state=random_state,
            node_features=node_features,
            allow_automatic_feature=True,
            skip_evaluation_biased_feature=True,
            precompute_constant_stocastic_features=precompute_constant_stocastic_features,
            smoke_test=smoke_test,
        )
        time_required_to_compute_constant_node_features = (
            time.time() - starting_to_compute_constant_node_features
        )

        # We execute the same thing as described above,
        # but now for the node type features instead that for
        # the node features.
        starting_to_compute_constant_node_type_features = time.time()
        node_type_features = cls.normalize_node_type_features(
            graph=graph,
            support=graph,
            random_state=random_state,
            node_type_features=node_type_features,
            allow_automatic_feature=True,
            skip_evaluation_biased_feature=True,
            precompute_constant_stocastic_features=precompute_constant_stocastic_features,
            smoke_test=smoke_test,
        )
        time_required_to_compute_constant_node_type_features = (
            time.time() - starting_to_compute_constant_node_type_features
        )

        # We execute the same thing as described above,
        # but now for the edge features instead that for
        # the node features.
        starting_to_compute_constant_edge_features = time.time()
        edge_features = cls.normalize_edge_features(
            graph=graph,
            support=graph,
            random_state=random_state,
            edge_features=edge_features,
            allow_automatic_feature=True,
            skip_evaluation_biased_feature=True,
            precompute_constant_stocastic_features=precompute_constant_stocastic_features,
            smoke_test=smoke_test,
        )
        time_required_to_compute_constant_edge_features = (
            time.time() - starting_to_compute_constant_edge_features
        )

        metadata = dict(
            number_of_threads=os.cpu_count(),
            python_version=platform.python_version(),
            platform=platform.platform(),
            node=platform.node(),
            embiggen_version=__embiggen_version__,
            number_of_holdouts=number_of_holdouts,
            number_of_slurm_nodes=number_of_slurm_nodes,
            time_required_to_compute_constant_node_features=time_required_to_compute_constant_node_features,
            time_required_to_compute_constant_node_type_features=time_required_to_compute_constant_node_type_features,
            time_required_to_compute_constant_edge_features=time_required_to_compute_constant_edge_features,
        )

        if number_of_slurm_nodes is not None:
            if slurm_node_id_variable not in os.environ:
                raise ValueError(
                    (
                        "Please do be advised that you have not provided "
                        "the {slurm_node_id_variable} variable but you have provided specified that "
                        "we should parallelize the holdouts across {number_of_slurm_nodes} nodes. "
                        "Please do make available this variable in the "
                        "slurm bash script by using the `export` flag "
                        "in a script similar to the following:\n"
                        "`srun --export=ALL,{slurm_node_id_variable}=$node_id` python3 your_script.py\n"
                        "You can learn more about this in the library tutorials."
                    ).format(
                        slurm_node_id_variable=slurm_node_id_variable,
                        number_of_slurm_nodes=number_of_slurm_nodes,
                    )
                )
            slurm_node_id = int(os.environ[slurm_node_id_variable])
            metadata["slurm_node_id"] = slurm_node_id
            metadata["number_of_slurm_nodes"] = number_of_slurm_nodes

        # We start to iterate on the holdouts.
        performance = pd.concat(
            [
                cls._evaluate_on_single_holdout(
                    models=models,
                    library_names=library_names,
                    graph=graph,
                    subgraph_of_interest=subgraph_of_interest,
                    use_subgraph_as_support=use_subgraph_as_support,
                    node_features=node_features,
                    node_type_features=node_type_features,
                    edge_type_features=edge_type_features,
                    edge_features=edge_features,
                    node_features_preprocessing_steps=node_features_preprocessing_steps,
                    random_state=random_state,
                    holdout_number=holdout_number,
                    number_of_holdouts=number_of_holdouts,
                    evaluation_schema=evaluation_schema,
                    enable_cache=enable_cache,
                    smoke_test=smoke_test,
                    holdouts_kwargs=holdouts_kwargs,
                    subgraph_of_interest_has_compatible_nodes=subgraph_of_interest_has_compatible_nodes,
                    verbose=verbose
                    and (number_of_slurm_nodes is None or slurm_node_id == 0),
                    features_names=features_names,
                    features_parameters=features_parameters,
                    metadata=metadata.copy(),
                    **validation_kwargs,
                )
                for holdout_number in trange(
                    number_of_holdouts,
                    disable=not (
                        verbose
                        and (number_of_slurm_nodes is None or slurm_node_id == 0)
                    ),
                    leave=False,
                    dynamic_ncols=True,
                    desc=f"Evaluating on {graph.get_name()}",
                )
                if (
                    number_of_slurm_nodes is None
                    or (
                        # We need to also mode the number of SLURM node IDs
                        # because the user may be parallelizing across many
                        # diffent nodes in contexts such as wide grid searches.
                        slurm_node_id
                        % number_of_slurm_nodes
                    )
                    == (
                        # We need to mode the holdout number as the number
                        # of holdouts may exceed the number of available SLURM
                        # nodes that the user has made available to this pipeline.
                        holdout_number
                        % number_of_slurm_nodes
                    )
                )
            ]
        )

        # We save the constant values for this model
        # execution.
        return performance

    @classmethod
    def is_stocastic(cls) -> bool:
        """Returns whether the model is stocastic and has therefore a random state."""
        return True
