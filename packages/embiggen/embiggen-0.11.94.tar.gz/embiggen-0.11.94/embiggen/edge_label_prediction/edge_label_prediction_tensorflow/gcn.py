"""GCN model for edge-label prediction."""
from typing import Dict, List, Optional, Type, Union, Any

import numpy as np
from ensmallen import Graph
from tensorflow.keras.optimizers import Optimizer

from embiggen.edge_label_prediction.edge_label_prediction_model import \
    AbstractEdgeLabelPredictionModel
from embiggen.sequences.tensorflow_sequences import (
    GCNEdgeLabelPredictionSequence, GCNEdgeLabelPredictionTrainingSequence)
from embiggen.utils.abstract_edge_gcn import (AbstractEdgeFeature,
                                              AbstractEdgeGCN, abstract_class)


@abstract_class
class GCNEdgeLabelPrediction(AbstractEdgeGCN, AbstractEdgeLabelPredictionModel):
    """GCN model for edge-label prediction."""

    def __init__(
        self,
        kernels: Optional[Union[str, List[str]]],
        epochs: int = 1000,
        number_of_graph_convolution_layers: int = 2,
        number_of_units_per_graph_convolution_layers: Union[int, List[int]] = 128,
        number_of_ffnn_body_layers: int = 2,
        number_of_ffnn_head_layers: int = 1,
        number_of_units_per_ffnn_body_layer: Union[int, List[int]] = 128,
        number_of_units_per_ffnn_head_layer: Union[int, List[int]] = 128,
        dropout_rate: float = 0.3,
        batch_size: Optional[int] = None,
        apply_norm: bool = False,
        combiner: str = "sum",
        edge_embedding_methods: Union[List[str], str] = "Concatenate",
        optimizer: Union[str, Type[Optimizer]] = "adam",
        early_stopping_min_delta: float = 0.0001,
        early_stopping_patience: int = 20,
        reduce_lr_min_delta: float = 0.0001,
        reduce_lr_patience: int = 5,
        early_stopping_monitor: str = "loss",
        early_stopping_mode: str = "min",
        reduce_lr_monitor: str = "loss",
        reduce_lr_mode: str = "min",
        reduce_lr_factor: float = 0.9,
        use_class_weights: bool = True,
        random_state: int = 42,
        use_edge_metrics: bool = False,
        use_node_embedding: bool = False,
        node_embedding_size: int = 50,
        use_node_type_embedding: bool = False,
        node_type_embedding_size: int = 50,
        residual_convolutional_layers: bool = False,
        siamese_node_feature_module: bool = True,
        handling_multi_graph: str = "warn",
        node_feature_names: Optional[Union[str, List[str]]] = None,
        node_type_feature_names: Optional[Union[str, List[str]]] = None,
        verbose: bool = False
    ):
        """Create new Kipf GCN object.

        Parameters
        -------------------------------
        kernels: Optional[Union[str, List[str]]]
            The type of normalization to use. It can either be:
            * "Weights", to just use the graph weights themselves.
            * "Left Normalized Laplacian", for the left normalized Laplacian.
            * "Right Normalized Laplacian", for the right normalized Laplacian.
            * "Symmetric Normalized Laplacian", for the symmetric normalized Laplacian.
            * "Transposed Left Normalized Laplacian", for the transposed left normalized Laplacian.
            * "Transposed Right Normalized Laplacian", for the transposed right normalized Laplacian.
            * "Transposed Symmetric Normalized Laplacian", for the transposed symmetric normalized Laplacian.
            * "Weighted Left Normalized Laplacian", for the weighted left normalized Laplacian.
            * "Weighted Right Normalized Laplacian", for the weighted right normalized Laplacian.
            * "Weighted Symmetric Normalized Laplacian", for the weighted symmetric normalized Laplacian.
            * "Transposed Weighted Left Normalized Laplacian", for the transposed weighted left normalized Laplacian.
            * "Transposed Weighted Right Normalized Laplacian", for the transposed weighted right normalized Laplacian.
            * "Transposed Weighted Symmetric Normalized Laplacian", for the transposed weighted symmetric normalized Laplacian.
        epochs: int = 1000
            Epochs to train the model for.
        number_of_graph_convolution_layers: int = 2
            Number of layers in the body subsection of the GCN section of the model.
        number_of_gcn_head_layers: int = 1
            Number of layers in the head subsection of the GCN section of the model.
        number_of_ffnn_body_layers: int = 2
            Number of layers in the body subsection of the FFNN section of the model.
        number_of_ffnn_head_layers: int = 1
            Number of layers in the head subsection of the FFNN section of the model.
        number_of_units_per_gcn_body_layer: Union[int, List[int]] = 128
            Number of units per gcn body layer.
        number_of_units_per_gcn_head_layer: Union[int, List[int]] = 128
            Number of units per gcn head layer.
        number_of_units_per_ffnn_body_layer: Union[int, List[int]] = 128
            Number of units per ffnn body layer.
        number_of_units_per_ffnn_head_layer: Union[int, List[int]] = 128
            Number of units per ffnn head layer.
        dropout_rate: float = 0.3
            Float between 0 and 1.
            Fraction of the input units to dropout.
        batch_size: Optional[int] = None
            Batch size to use while training the model.
            If None, the batch size will be the number of nodes.
            In all model parametrization that involve a number of graph
            convolution layers, the batch size will be the number of nodes.
        apply_norm: bool = False
            Whether to normalize the output of the convolution operations,
            after applying the level activations.
        combiner: str = "mean"
            A string specifying the reduction op.
            Currently "mean", "sqrtn" and "sum" are supported. 
            "sum" computes the weighted sum of the embedding results for each row.
            "mean" is the weighted sum divided by the total weight.
            "sqrtn" is the weighted sum divided by the square root of the sum of the squares of the weights.
            Defaults to mean.
        edge_embedding_method: str = "Concatenate"
            The edge embedding method to use to put togheter the
            source and destination node features, which includes:
            - Concatenate
            - Average
            - Hadamard
            - L1
            - L2
            - Maximum
            - Minimum
            - Add
            - Subtract
            - Dot
        optimizer: Union[str, Type[Optimizer]] = "adam"
            The optimizer to use while training the model.
            By default, we use `LazyAdam`, which should be faster
            than Adam when handling sparse gradients such as the one
            we are using to train this model.
            When the tensorflow addons module is not available,
            we automatically switch back to `Adam`.
        early_stopping_min_delta: float
            Minimum delta of metric to stop the training.
        early_stopping_patience: int
            Number of epochs to wait for when the given minimum delta is not
            achieved after which trigger early stopping.
        reduce_lr_min_delta: float
            Minimum delta of metric to reduce learning rate.
        reduce_lr_patience: int
            Number of epochs to wait for when the given minimum delta is not
            achieved after which reducing learning rate.
        early_stopping_monitor: str = "loss",
            Metric to monitor for early stopping.
        early_stopping_mode: str = "min",
            Direction of the variation of the monitored metric for early stopping.
        reduce_lr_monitor: str = "loss",
            Metric to monitor for reducing learning rate.
        reduce_lr_mode: str = "min",
            Direction of the variation of the monitored metric for learning rate.
        reduce_lr_factor: float = 0.9,
            Factor for reduction of learning rate.
        use_class_weights: bool = True
            Whether to use class weights to rebalance the loss relative to unbalanced classes.
            Learn more about class weights here: https://www.tensorflow.org/tutorials/structured_data/imbalanced_data
        use_node_embedding: bool = False
            Whether to use a node embedding layer to let the model automatically
            learn an embedding of the nodes.
        node_embedding_size: int = 50
            Size of the node embedding.
        use_node_types: Union[bool, str] = "auto"
            Whether to use the node types while training the model.
            By default, automatically uses them if the graph has them.
        node_type_embedding_size: int = 50
            Size of the embedding for the node types.
        training_unbalance_rate: float = 1.0
            Unbalance rate for the training non-existing edges.
        use_edge_metrics: bool = False
            Whether to use the edge metrics from traditional edge prediction.
            These metrics currently include:
            - Adamic Adar
            - Jaccard Coefficient
            - Resource allocation index
            - Preferential attachment
        random_state: int = 42
            Random state to reproduce the training samples.
        use_node_embedding: bool = False
            Whether to use a node embedding layer that is automatically learned
            by the model while it trains. Please do be advised that by using
            a node embedding layer you are making a closed-world assumption,
            and this model will not work on graphs with a different node vocabulary.
        node_embedding_size: int = 50
            Dimension of the node embedding.
        use_node_type_embedding: bool = False
            Whether to use a node type embedding layer that is automatically learned
            by the model while it trains. Please do be advised that by using
            a node type embedding layer you are making a closed-world assumption,
            and this model will not work on graphs with a different node vocabulary.
        node_type_embedding_size: int = 50
            Dimension of the node type embedding.
        residual_convolutional_layers: bool = False
            Whether to use residual connections between convolutional layers.
        siamese_node_feature_module: bool = True
            Whether to use a siamese module to process the node features.
        handling_multi_graph: str = "warn"
            How to behave when dealing with multigraphs.
            Possible behaviours are:
            - "warn"
            - "raise"
            - "drop"
        node_feature_names: Optional[Union[str, List[str]]] = None
            Names of the node features.
            This is used as the layer names.
        node_type_feature_names: Optional[Union[str, List[str]]] = None
            Names of the node type features.
            This is used as the layer names.
        verbose: bool = False
            Whether to show loading bars.
        """
        AbstractEdgeGCN.__init__(
            self,
            kernels=kernels,
            epochs=epochs,
            number_of_graph_convolution_layers=number_of_graph_convolution_layers,
            number_of_units_per_graph_convolution_layers=number_of_units_per_graph_convolution_layers,
            number_of_ffnn_body_layers=number_of_ffnn_body_layers,
            number_of_ffnn_head_layers=number_of_ffnn_head_layers,
            number_of_units_per_ffnn_body_layer=number_of_units_per_ffnn_body_layer,
            number_of_units_per_ffnn_head_layer=number_of_units_per_ffnn_head_layer,
            dropout_rate=dropout_rate,
            batch_size=batch_size,
            apply_norm=apply_norm,
            combiner=combiner,
            edge_embedding_methods=edge_embedding_methods,
            optimizer=optimizer,
            early_stopping_min_delta=early_stopping_min_delta,
            early_stopping_patience=early_stopping_patience,
            reduce_lr_min_delta=reduce_lr_min_delta,
            reduce_lr_patience=reduce_lr_patience,
            early_stopping_monitor=early_stopping_monitor,
            early_stopping_mode=early_stopping_mode,
            reduce_lr_monitor=reduce_lr_monitor,
            reduce_lr_mode=reduce_lr_mode,
            reduce_lr_factor=reduce_lr_factor,
            use_class_weights=use_class_weights,
            use_edge_metrics=use_edge_metrics,
            random_state=random_state,
            use_node_embedding=use_node_embedding,
            node_embedding_size=node_embedding_size,
            use_node_type_embedding=use_node_type_embedding,
            node_type_embedding_size=node_type_embedding_size,
            residual_convolutional_layers=residual_convolutional_layers,
            siamese_node_feature_module=siamese_node_feature_module,
            handling_multi_graph=handling_multi_graph,
            node_feature_names=node_feature_names,
            node_type_feature_names=node_type_feature_names,
            verbose=verbose,
        )
        AbstractEdgeLabelPredictionModel.__init__(self, random_state=random_state)

    def _get_model_prediction_input(
        self,
        graph: Graph,
        support: Graph,
        node_features: List[np.ndarray],
        node_type_features: List[np.ndarray],
        edge_type_features: List[np.ndarray],
        edge_features: List[Union[Type[AbstractEdgeFeature], np.ndarray]],
    ) -> GCNEdgeLabelPredictionSequence:
        """Returns prediction sequence."""
        return GCNEdgeLabelPredictionSequence(
            graph,
            support=support,
            kernels=self.convert_graph_to_kernels(support),
            batch_size=self.get_batch_size_from_graph(graph),
            node_features=node_features,
            return_node_ids=self._use_node_embedding,
            return_edge_node_ids=self._use_node_embedding or self.has_kernels(),
            return_node_types=self._use_node_type_embedding,
            node_type_features=node_type_features,
            use_edge_metrics=self._use_edge_metrics,
            edge_features=edge_features
        )

    def _get_model_training_input(
        self,
        graph: Graph,
        support: Graph,
        node_features: List[np.ndarray],
        node_type_features: List[np.ndarray],
        edge_type_features: List[np.ndarray],
        edge_features: List[Union[Type[AbstractEdgeFeature], np.ndarray]],
    ) -> GCNEdgeLabelPredictionTrainingSequence:
        """Returns training input tuple."""
        return GCNEdgeLabelPredictionTrainingSequence(
            graph=graph,
            support=support,
            kernels=self.convert_graph_to_kernels(support),
            batch_size=self.get_batch_size_from_graph(graph),
            node_features=node_features,
            return_node_ids=self._use_node_embedding,
            return_edge_node_ids=self._use_node_embedding or self.has_kernels(),
            return_node_types=self._use_node_type_embedding,
            node_type_features=node_type_features,
            use_edge_metrics=self._use_edge_metrics,
            edge_features=edge_features,
        )

    def _get_class_weights(self, graph: Graph) -> Dict[int, float]:
        """Returns dictionary with class weights."""
        number_of_directed_edges = graph.get_number_of_directed_edges()
        edge_types_number = graph.get_number_of_edge_types()
        return {
            edge_type_id: number_of_directed_edges / count / edge_types_number
            for edge_type_id, count in graph.get_edge_type_id_counts_hashmap().items()
        }

    def get_output_classes(self, graph: Graph) -> int:
        """Returns number of output classes."""
        if self.is_binary_prediction_task():
            return 1
        return graph.get_number_of_edge_types()

    def _predict_proba(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[List[np.ndarray]] = None,
        node_type_features: Optional[List[np.ndarray]] = None,
        edge_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[Union[Type[AbstractEdgeFeature], List[Union[Type[AbstractEdgeFeature], np.ndarray]]]] = None,
    ) -> np.ndarray:
        """Run predictions on the provided graph."""
        predictions = super()._predict_proba(
            graph,
            support=support,
            node_features=node_features,
            node_type_features=node_type_features,
            edge_type_features=edge_type_features,
            edge_features=edge_features
        )
        # The model will padd the predictions with a few zeros
        # in order to run the GCN portion of the model, which
        # always requires a batch size equal to the nodes number.
        return predictions[:graph.get_number_of_edges()]
    
    def parameters(self) -> Dict[str, Any]:
        """Returns parameters used for this model."""
        removed = [
            "use_edge_type_embedding",
            "edge_type_embedding_size",
            "edge_type_feature_names"
        ]
        return dict(
            **{
                key: value
                for key, value in AbstractEdgeGCN.parameters(self).items()
                if key not in removed
            },
        )