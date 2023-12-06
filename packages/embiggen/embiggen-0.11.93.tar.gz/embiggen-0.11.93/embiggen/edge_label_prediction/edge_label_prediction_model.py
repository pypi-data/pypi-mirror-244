"""Module providing abstract edge label prediction model."""
from typing import Optional, Union, List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from ensmallen import Graph
from embiggen.utils.abstract_models import AbstractClassifierModel


class AbstractEdgeLabelPredictionModel(AbstractClassifierModel):
    """Class defining an abstract edge label prediction model."""

    def __init__(self, random_state: Optional[int] = None):
        """Create new abstract edge-label prediction model.

        Parameters
        ---------------
        random_state: Optional[int] = None
            The random state to use if the model is stocastic.
        """
        self._is_binary_prediction_task = None
        self._is_multilabel_prediction_task = None
        self._number_of_output_labels = None
        super().__init__(random_state=random_state)

    @classmethod
    def requires_edge_types(cls) -> bool:
        """Returns whether this method requires node types."""
        return True

    @classmethod
    def task_name(cls) -> str:
        """Returns name of the task this model is used for."""
        return "Edge Label Prediction"

    @classmethod
    def is_topological(cls) -> bool:
        return False

    def is_binary_prediction_task(self) -> bool:
        """Returns whether the model was fit on a binary prediction task."""
        return self._is_binary_prediction_task

    def is_multilabel_prediction_task(self) -> bool:
        """Returns whether the model was fit on a multilabel prediction task."""
        return self._is_multilabel_prediction_task

    @classmethod
    def get_available_evaluation_schemas(cls) -> List[str]:
        """Returns available evaluation schemas for this task."""
        return [
            "Stratified Monte Carlo",
            "Stratified Kfold",
            "Kfold",
            "Monte Carlo",
        ]

    @classmethod
    def split_graph_following_evaluation_schema(
        cls,
        graph: Graph,
        evaluation_schema: str,
        random_state: int,
        holdout_number: int,
        number_of_holdouts: int,
        **holdouts_kwargs: Dict[str, Any],
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
            The number of holdouts that will be generated throught the evaluation.
        holdouts_kwargs: Dict[str, Any]
            The kwargs to be forwarded to the holdout method.
        """
        if evaluation_schema in ("Monte Carlo", "Stratified Monte Carlo"):
            return graph.get_edge_label_holdout_graphs(
                **holdouts_kwargs,
                use_stratification="Stratified" in evaluation_schema,
                random_state=random_state+holdout_number,
            )
        if evaluation_schema in ("Kfold", "Stratified Kfold"):
            return graph.get_edge_label_kfold(
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
        edge_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]] = None,
        subgraph_of_interest: Optional[Graph] = None,
        random_state: int = 42,
        verbose: bool = True,
    ) -> List[Dict[str, Any]]:
        """Return model evaluation on the provided graphs."""
        train_size = train.get_number_of_known_edge_types() / graph.get_number_of_known_edge_types()

        performance = []
        for evaluation_mode, evaluation_graph in (
            ("train", train),
            ("test", test),
        ):
            if evaluation_graph.is_directed():
                mask = evaluation_graph.get_directed_edges_with_known_edge_types_mask()
            else:
                mask = evaluation_graph.get_upper_triangular_known_edge_types_mask()

            prediction_probabilities = self.predict_proba(
                evaluation_graph,
                support=support,
                node_features=node_features,
                node_type_features=node_type_features,
                edge_features=edge_features
            )

            if prediction_probabilities.shape[0] != mask.shape[0]:
                raise RuntimeError(
                    "The number of predictions and the number of edges "
                    "in the graph do not match. "
                    f"Found {prediction_probabilities.shape[0]} predictions "
                    f"and {mask.shape[0]} edges."
                )

            prediction_probabilities = prediction_probabilities[mask]

            if evaluation_graph.is_directed():
                labels = evaluation_graph.get_directed_known_edge_type_ids()
            else:
                labels = evaluation_graph.get_upper_triangular_known_edge_type_ids()
            
            if self.is_binary_prediction_task():
                predictions = prediction_probabilities
                labels = labels == 1
            elif self.is_multilabel_prediction_task():
                # TODO! support multilabel prediction!
                raise NotImplementedError(
                    "Currently we do not support multi-label edge-label prediction "
                    f"in the {self.model_name()} from the {self.library_name()} "
                    f"as it is implemented in the {self.__class__.__name__} class."
                )
            else:
                predictions = prediction_probabilities.argmax(axis=-1)

            performance.append({
                "evaluation_mode": evaluation_mode,
                "train_size": train_size,
                "known_edges_number": graph.get_number_of_known_edge_types(),
                **self.evaluate_predictions(
                    labels,
                    predictions,
                ),
                **self.evaluate_prediction_probabilities(
                    labels,
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
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node type features to use.
        edge_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge type features to use.
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge features to use.
        """
        non_zero_edge_types = sum([
            1
            for count in graph.get_edge_type_names_counts_hashmap().values()
            if count > 0
        ])

        if non_zero_edge_types < 2:
            raise ValueError(
                "The provided training graph has less than two non-zero edge types. "
                "It is unclear how to proceeed."
            )

        self._is_binary_prediction_task = non_zero_edge_types == 2
        self._is_multilabel_prediction_task = graph.is_multigraph()
        self._number_of_output_labels = graph.get_number_of_edge_types()

        if self._is_multilabel_prediction_task:
            raise ValueError(
                "Currently we do not support multi-label edge prediction."
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
        return True

    @classmethod
    def task_involves_node_types(cls) -> bool:
        """Returns whether the model task involves node types."""
        return False

    @classmethod
    def task_involves_topology(cls) -> bool:
        """Returns whether the model task involves topology."""
        return False
    
    def is_using_node_types(self) -> bool:
        """Whether the current model is using node types."""
        return self._is_using_node_type_features or self.requires_node_types()

    @classmethod
    def supports_multilabel_prediction(cls) -> bool:
        """Returns whether the model supports multilabel prediction.
        
        Implementation details
        ----------------------
        At this time, no model supports multilabel prediction for the
        edge label prediction task.
        """
        return False
    
    @classmethod
    def can_use_edge_type_features(cls) -> bool:
        """Returns whether the model can use edge type features."""
        return False
    
    @classmethod
    def can_use_edge_features(cls) -> bool:
        """Returns whether the model can use edge features."""
        return True
    
    @classmethod
    def requires_edge_features(cls) -> bool:
        """Returns whether the model requires edge features."""
        return False
    
    @classmethod
    def can_use_node_type_features(cls) -> bool:
        """Returns whether the model can use node type features."""
        return True