"""Module providing Perceptron for edge prediction."""
import json
from typing import Any, Dict, List, Optional, Union

import compress_json
import compress_pickle
import numpy as np
from ensmallen import Graph, models # pylint: disable=no-name-in-module

from embiggen.edge_prediction.edge_prediction_model import \
    AbstractEdgePredictionModel
from embiggen.embedding_transformers import NodeTransformer


class PerceptronEdgePrediction(AbstractEdgePredictionModel):
    """Perceptron model for edge prediction."""

    def __init__(
        self,
        edge_features: Optional[Union[str, List[str]]] = "JaccardCoefficient",
        edge_embeddings: Optional[Union[str, List[str]]] = None,
        cooccurrence_iterations: int = 100,
        cooccurrence_window_size: int = 10,
        number_of_epochs: int = 1000,
        number_of_edges_per_mini_batch: int = 4096,
        learning_rate: float = 0.001,
        first_order_decay_factor: float = 0.9,
        second_order_decay_factor: float = 0.999,
        avoid_false_negatives: bool = False,
        use_scale_free_distribution: bool = True,
        random_state: int = 42,
        verbose: bool = True
    ):
        """Create new Perceptron object.

        Parameters
        ------------------------
        edge_features: Optional[Union[str, List[str]]] = "JaccardCoefficient"
            The edge features to compute for each edge.
            Zero or more edge features can be used at once.
            The currently supported edge features are:
            - Degree,
            - AdamicAdar,
            - JaccardCoefficient,
            - Cooccurrence,
            - ResourceAllocationIndex,
            - PreferentialAttachment,
        edge_embeddings: Optional[Union[str, List[str]]] = None
            The embedding methods to use for the provided node features.
            Zero or more edge emmbedding methods can be used at once.
            The currently supported edge embedding are:
            - CosineSimilarity,
            - EuclideanDistance,
            - Concatenate,
            - Hadamard,
            - L1,
            - L2,
            - Add,
            - Sub,
            - Maximum,
            - Minimum,
        cooccurrence_iterations: int = 100
            Number of iterations to run when computing the cooccurrence metric.
            By default 100.
        cooccurrence_window_size: int = 10
            Window size to consider to measure the cooccurrence.
            By default 100.
        number_of_epochs: int = 1000
            The number of epochs to train the model for. By default, 100.
        number_of_edges_per_mini_batch: int = 4096
            The number of samples to include for each mini-batch. By default 4096.
        learning_rate: float = 0.001
            Learning rate to use while training the model.
            By default 0.001.
        first_order_decay_factor: float = 0.9
            First order decay factor for the first order momentum.
            By default 0.9.
        second_order_decay_factor: float = 0.999
            Second order decay factor for the second order momentum.
            By default 0.999.
        avoid_false_negatives: bool = False
            Whether to avoid sampling false negatives.
            This may cause a slower training.
        use_scale_free_distribution: bool = True
            Whether to train model using a scale free distribution for the negatives.
        random_state: int = 42
            The random state to reproduce the model initialization and training. By default, 42.
        verbose: bool = True
            Whether to show epochs loading bar.
        """
        super().__init__(random_state=random_state)

        if isinstance(edge_features, str):
            edge_features = [edge_features]

        if isinstance(edge_embeddings, str):
            edge_embeddings = [edge_embeddings]

        self._model_kwargs = dict(
            edge_features=edge_features,
            edge_embeddings=edge_embeddings,
            cooccurrence_iterations=cooccurrence_iterations,
            cooccurrence_window_size=cooccurrence_window_size,
            number_of_epochs=number_of_epochs,
            number_of_edges_per_mini_batch=number_of_edges_per_mini_batch,
            learning_rate=learning_rate,
            first_order_decay_factor=first_order_decay_factor,
            second_order_decay_factor=second_order_decay_factor,
            avoid_false_negatives=avoid_false_negatives,
            use_scale_free_distribution=use_scale_free_distribution,
        )
        self._verbose = verbose
        self._model = models.EdgePredictionPerceptron(
            **self._model_kwargs,
            random_state=random_state
        )

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters used for this model."""
        return dict(
            **super().parameters(),
            **self._model_kwargs
        )

    def clone(self) -> "PerceptronEdgePrediction":
        return PerceptronEdgePrediction(**self.parameters())

    @classmethod
    def smoke_test_parameters(cls) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        return dict(
            number_of_epochs=1,
            edge_features="Degree"
        )

    def _fit(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[List[np.ndarray]] = None,
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
        edge_features: Optional[List[np.ndarray]] = None
            The edge features to use.
        """
        if edge_type_features is not None and len(edge_type_features) > 0:
            raise NotImplementedError(
                "Edge type features are not yet supported by "
                f"the model {self.model_name()} from {self.library_name()} library "
                f"for the task of {self.task_name()}. "
                f"Received object of type {type(edge_type_features)}."
            )
        
        if edge_features is not None and len(edge_features) > 0:
            raise NotImplementedError(
                "Edge features are not yet supported by "
                f"the model {self.model_name()} from {self.library_name()} library "
                f"for the task of {self.task_name()}. "
                f"Received object of type {type(edge_features)}."
            )

        new_node_features = []
        if node_features is not None:
            for node_feature in node_features:
                if not node_feature.data.c_contiguous:
                    node_feature = np.ascontiguousarray(node_feature)
                new_node_features.append(node_feature)

        if node_type_features is not None:
            for node_type_feature in node_type_features:
                node_transformer = NodeTransformer(
                    aligned_mapping=True
                )
                node_transformer.fit(
                    node_type_feature=node_type_feature
                )
                node_feature = node_transformer.transform(
                    node_types=graph
                )
                if not node_feature.data.c_contiguous:
                    node_feature = np.ascontiguousarray(node_feature)
                new_node_features.append(node_feature)

        self._model.fit(
            graph=graph,
            node_features=new_node_features,
            verbose=self._verbose,
            support=support
        )

    def _predict(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[List[np.ndarray]] = None,
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
        node_features: Optional[List[np.ndarray]]
            The node features to use.
        node_type_features: Optional[List[np.ndarray]] = None
            The node type features to use.
        edge_type_features: Optional[List[np.ndarray]] = None
            The edge type features to use.
        edge_features: Optional[List[np.ndarray]] = None
            The edge features to use.
        """
        return self._predict_proba(
            graph=graph,
            support=support,
            node_features=node_features,
            node_type_features=node_type_features,
            edge_features=edge_features
        ) > 0.5

    def _predict_proba(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[List[np.ndarray]] = None,
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
        edge_features: Optional[List[np.ndarray]] = None
            The edge features to use.
        """
        new_node_features = []
        for node_feature in node_features:
            if not node_feature.data.c_contiguous:
                node_feature = np.ascontiguousarray(node_feature)
            new_node_features.append(node_feature)
        
        for node_type_feature in node_type_features:
            node_transformer = NodeTransformer(
                aligned_mapping=True
            )
            node_transformer.fit(
                node_type_feature=node_type_feature
            )
            node_feature = node_transformer.transform(
                node_types=graph
            )
            if not node_feature.data.c_contiguous:
                node_feature = np.ascontiguousarray(node_feature)
            new_node_features.append(node_feature)

        return self._model.predict(
            graph=graph,
            node_features=new_node_features,
            support=support
        )

    @classmethod
    def requires_node_types(cls) -> bool:
        """Returns whether the model requires node types."""
        return False

    @classmethod
    def can_use_node_types(cls) -> bool:
        """Returns whether the model can optionally use node types."""
        return True
    
    @classmethod
    def requires_edge_types(cls) -> bool:
        """Returns whether the model requires edge types."""
        return False
    
    @classmethod
    def can_use_edge_types(cls) -> bool:
        """Returns whether the model can optionally use edge types."""
        return True
    
    @classmethod
    def can_use_edge_weights(cls) -> bool:
        """Returns whether the model can optionally use edge weights."""
        return False

    @classmethod
    def model_name(cls) -> str:
        return "Perceptron"

    @classmethod
    def library_name(cls) -> str:
        return "Ensmallen"

    @classmethod
    def load(cls, path: str):
        """Load a saved version of the model from the provided path.

        Parameters
        -------------------
        path: str
            Path from where to load the model.
        """
        data = compress_json.load(path)
        model = PerceptronEdgePrediction(**data["parameters"])
        model._model = models.EdgePredictionPerceptron.loads(
            json.dumps(data["inner_model"])
        )
        for key, value in data["metadata"].items():
            setattr(model, key, value)
        return model

    def dumps(self) -> Dict[str, Any]:
        """Dumps the current model as dictionary."""
        return dict(
            parameters=self.parameters(),
            inner_model=json.loads(self._model.dumps()),
            metadata=dict(
                _fitting_was_executed=self._fitting_was_executed
            )
        )

    def dump(self, path: str):
        """Dump the current model at the provided path.

        Parameters
        -------------------
        path: str
            Path from where to dump the model.
        """
        if ".json" in path:
            compress_json.dump(
                self.dumps(),
                path
            )
        if ".pkl" in path:
            compress_pickle.dump(
                self.dumps(),
                path
            )

        raise NotImplementedError(
            "The provided path does not have a valid extension. "
            "Please use either .json or .pkl, followed by the eventual "
            "desired compression algorithm extension."
        )

    @classmethod
    def can_use_edge_type_features(cls) -> bool:
        return False
    
    @classmethod
    def can_use_edge_features(cls) -> bool:
        return False
    
    