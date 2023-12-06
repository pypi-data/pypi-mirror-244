"""Module providing abstract node label prediction model."""
from typing import Optional, Union, List, Dict, Any, Tuple
import pandas as pd
import numpy as np
import warnings
from ensmallen import Graph
from embiggen.utils.abstract_models import AbstractClassifierModel, abstract_class


@abstract_class
class AbstractNodeLabelPredictionModel(AbstractClassifierModel):
    """Class defining an abstract node label prediction model."""

    def __init__(self, random_state: Optional[int] = None):
        """Create new abstract node-label prediction model.

        Parameters
        ---------------
        random_state: Optional[int] = None
            The random state to use if the model is stocastic.
        """
        self._is_binary_prediction_task = None
        self._is_multilabel_prediction_task = None
        super().__init__(random_state=random_state)

    @classmethod
    def requires_node_types(cls) -> bool:
        """Returns whether this method requires node types."""
        return True

    @classmethod
    def task_name(cls) -> str:
        """Returns name of the task this model is used for."""
        return "Node Label Prediction"

    @classmethod
    def is_topological(cls) -> bool:
        return False

    @classmethod
    def get_available_evaluation_schemas(cls) -> List[str]:
        """Returns available evaluation schemas for this task."""
        return [
            "Stratified Monte Carlo",
            "Stratified Kfold",
            "Monte Carlo",
            "Kfold",
        ]

    def is_binary_prediction_task(self) -> bool:
        """Returns whether the model was fit on a binary prediction task."""
        return self._is_binary_prediction_task

    def is_multilabel_prediction_task(self) -> bool:
        """Returns whether the model was fit on a multilabel prediction task."""
        return self._is_multilabel_prediction_task

    @classmethod
    def split_graph_following_evaluation_schema(
        cls,
        graph: Graph,
        evaluation_schema: str,
        random_state: int,
        holdout_number: int,
        number_of_holdouts: int,
        **holdouts_kwargs: Dict
    ) -> Tuple[Graph]:
        """Return train and test graphs tuple following the provided evaluation schema.

        Parameters
        ----------------------
        graph: Graph
            The graph to split.
        evaluation_schema: str
            The evaluation schema to follow.
        random_state: int
            The random state for the evaluation
        holdout_number: int
            The current holdout number.
        number_of_holdouts: int
            The total number of holdouts.
        holdouts_kwargs: Dict[str, Any]
            The kwargs to be forwarded to the holdout method.
        """
        if evaluation_schema in ("Stratified Monte Carlo", "Monte Carlo"):
            return graph.get_node_label_holdout_graphs(
                **holdouts_kwargs,
                use_stratification="Stratified" in evaluation_schema,
                random_state=random_state+holdout_number,
            )
        if evaluation_schema in ("Kfold", "Stratified Kfold"):
            return graph.get_node_label_kfold(
                k=number_of_holdouts,
                k_index=holdout_number,
                use_stratification="Stratified" in evaluation_schema,
                random_state=random_state,
            )
        super().split_graph_following_evaluation_schema(
            graph=graph,
            evaluation_schema=evaluation_schema,
            random_state=random_state,
            holdout_number=holdout_number,
            number_of_holdouts=number_of_holdouts,
            **holdouts_kwargs,
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
        **kwargs: Dict
    ) -> Dict[str, Any]:
        """Return additional custom parameters for the current holdout."""
        return {}

    def _evaluate(
        self,
        graph: Graph,
        train: Graph,
        test: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]] = None,
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]] = None,
        edge_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]] = None,
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]] = None,
        subgraph_of_interest: Optional[Graph] = None,
        random_state: int = 42,
        verbose: bool = True,
    ) -> List[Dict[str, Any]]:
        """Return model evaluation on the provided graphs."""
        train_size = train.get_number_of_known_node_types(
        ) / graph.get_number_of_known_node_types()

        if self.is_multilabel_prediction_task():
            labels = graph.get_one_hot_encoded_node_types()
        elif self.is_binary_prediction_task():
            labels = graph.get_boolean_node_type_ids()
        else:
            labels = graph.get_single_label_node_type_ids()

        performance = []
        for evaluation_mode, evaluation_graph in (
            ("train", train),
            ("test", test),
        ):
            prediction_probabilities = self.predict_proba(
                evaluation_graph,
                support=support,
                node_features=node_features,
                node_type_features=node_type_features,
                edge_type_features=edge_type_features,
                edge_features=edge_features
            )

            if self.is_binary_prediction_task():
                if prediction_probabilities.shape[1] == 1:
                    predictions = prediction_probabilities
                elif prediction_probabilities.shape[1] == 2:
                    predictions = prediction_probabilities[:, 1]
                    prediction_probabilities = prediction_probabilities[:, 1]
                else:
                    raise NotImplementedError(
                        f"The model {self.model_name()} as implemented in "
                        f"the library {self.library_name()} for the task "
                        f"{self.task_name()} has produced a binary prediction "
                        f"result with shape {prediction_probabilities.shape}, "
                        "which is unclear how to handle for evaluation. "
                        "Please open an issue and pull request to clarify what "
                        "you expect to happen here."
                    )
            elif self.is_multilabel_prediction_task():
                predictions = prediction_probabilities > 0.5
            else:
                predictions = prediction_probabilities.argmax(axis=-1)

            mask = evaluation_graph.get_known_node_types_mask()
            prediction_probabilities = prediction_probabilities[mask]
            predictions = predictions[mask]
            labels_subset = labels[mask]

            performance.append({
                "evaluation_mode": evaluation_mode,
                "train_size": train_size,
                "known_nodes_number": evaluation_graph.get_number_of_known_node_types(),
                **self.evaluate_predictions(
                    labels_subset,
                    predictions,
                ),
                **self.evaluate_prediction_probabilities(
                    labels_subset,
                    prediction_probabilities,
                ),
            })

        return performance

    def fit(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        edge_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
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
        node_type_features: Optional[Union[str, pd.DataFrame, np.ndarray, AbstractEmbeddingModel, List[Union[str, pd.DataFrame, np.ndarray, AbstractEmbeddingModel]]]] = None
            The node type features to use.
        edge_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge type features to use.
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge features to use.
            
        Raises
        --------------------
        ValueError
            If the graph has less than two node types.
        NotImplementedError
            If edge features are provided.
            If node type features are provided.
            If edge type features are provided.
        """
        non_zero_node_types = sum([
            1
            for count in graph.get_node_type_names_counts_hashmap().values()
            if count > 0
        ])

        if non_zero_node_types < 2:
            raise ValueError(
                "The provided training graph has less than two non-zero node types. "
                "It is unclear how to proceeed."
            )

        self._is_binary_prediction_task = non_zero_node_types == 2
        self._is_multilabel_prediction_task = graph.has_multilabel_node_types()

        node_type_counts = graph.get_node_type_names_counts_hashmap()
        most_common_node_type_name, most_common_count = max(
            node_type_counts.items(),
            key=lambda x: x[1]
        )
        least_common_node_type_name, least_common_count = min(
            node_type_counts.items(),
            key=lambda x: x[1]
        )

        if most_common_count > least_common_count * 20:
            warnings.warn(
                "Please do be advised that this graph defines "
                "an unbalanced node-label prediction task, with the "
                f"most common node type `{most_common_node_type_name}` appearing {most_common_count} times, "
                f"while the least common one, `{least_common_node_type_name}`, appears only `{least_common_count}` times. "
                "Do take this into account when designing the node-label prediction model."
            )

        super().fit(
            graph=graph,
            support=support,
            node_features=node_features,
            node_type_features=node_type_features,
            edge_type_features=edge_type_features,
            edge_features=edge_features,
        )

    @classmethod
    def task_involves_edge_weights(cls) -> bool:
        """Returns whether the model task involves edge weights."""
        return False

    @classmethod
    def task_involves_edge_types(cls) -> bool:
        """Returns whether the model task involves edge types."""
        return False

    @classmethod
    def task_involves_node_types(cls) -> bool:
        """Returns whether the model task involves node types."""
        return True

    @classmethod
    def task_involves_topology(cls) -> bool:
        """Returns whether the model task involves topology."""
        return False
    
    @classmethod
    def can_use_edge_type_features(cls) -> bool:
        """Returns whether the model can use edge type features."""
        return False
    
    @classmethod
    def can_use_node_type_features(cls) -> bool:
        """Returns whether the model can use node type features."""
        return False
    
    @classmethod
    def can_use_edge_features(cls) -> bool:
        """Returns whether the model can use edge features."""
        return False