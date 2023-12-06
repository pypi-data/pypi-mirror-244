"""GCN model for node-label prediction."""
from typing import List, Union, Optional, Dict, Type, Tuple, Any

import numpy as np
from tensorflow.keras.layers import Dense, Concatenate  # pylint: disable=import-error,no-name-in-module
from tensorflow.keras.models import Model  # pylint: disable=import-error,no-name-in-module
from tensorflow.keras.optimizers import \
    Optimizer  # pylint: disable=import-error,no-name-in-module

from ensmallen import Graph
from tensorflow.keras.utils import Sequence
from embiggen.utils.abstract_gcn import AbstractGCN, abstract_class
from embiggen.utils.normalize_model_structural_parameters import normalize_model_list_parameter
from embiggen.node_label_prediction.node_label_prediction_model import AbstractNodeLabelPredictionModel
from embiggen.utils.number_to_ordinal import number_to_ordinal

@abstract_class
class GCNNodeLabelPrediction(AbstractGCN, AbstractNodeLabelPredictionModel):
    """GCN model for node-label prediction."""

    def __init__(
        self,
        kernels: Optional[Union[str, List[str]]],
        epochs: int = 1000,
        number_of_graph_convolution_layers: int = 2,
        number_of_head_layers: int = 1,
        number_of_units_per_graph_convolution_layers: Union[int, List[int]] = 128,
        number_of_units_per_head_layer: Union[int, List[int]] = 128,
        dropout_rate: float = 0.1,
        batch_size: Optional[int] = None,
        apply_norm: bool = False,
        combiner: str = "sum",
        optimizer: Union[str, Optimizer] = "adam",
        early_stopping_min_delta: float = 0.0001,
        early_stopping_patience: int = 30,
        reduce_lr_min_delta: float = 0.001,
        reduce_lr_patience: int = 20,
        early_stopping_monitor: str = "loss",
        early_stopping_mode: str = "min",
        reduce_lr_monitor: str = "loss",
        reduce_lr_mode: str = "min",
        reduce_lr_factor: float = 0.9,
        use_class_weights: bool = True,
        random_state: int = 42,
        use_node_embedding: bool = False,
        node_embedding_size: int = 50,
        residual_convolutional_layers: bool = False,
        handling_multi_graph: str = "warn",
        node_feature_names: Optional[Union[str, List[str]]] = None,
        node_type_feature_names: Optional[Union[str, List[str]]] = None,
        verbose: bool = True
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
        number_of_units_per_hidden_layer: Union[int, List[int]] = 128
            Number of units per hidden layer.
        number_of_hidden_layers: int = 3
            Number of graph convolution layer.
        number_of_units_per_hidden_layer: Union[int, List[int]] = 128
            Number of units per hidden layer.
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
        optimizer: str = "Adam"
            The optimizer to use while training the model.
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
        random_state: int = 42
            The random state to use to reproduce the training.
        use_node_embedding: bool = False
            Whether to use a node embedding layer that is automatically learned
            by the model while it trains. Please do be advised that by using
            a node embedding layer you are making a closed-world assumption,
            and this model will not work on graphs with a different node vocabulary.
        node_embedding_size: int = 50
            Dimension of the node embedding.
        residual_convolutional_layers: bool = False
            Whether to use residual connections between convolutional layers.
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
        verbose: bool = True
            Whether to show loading bars.
        """
        AbstractGCN.__init__(
            self,
            kernels=kernels,
            epochs=epochs,
            number_of_graph_convolution_layers=number_of_graph_convolution_layers,
            number_of_units_per_graph_convolution_layers=number_of_units_per_graph_convolution_layers,
            dropout_rate=dropout_rate,
            batch_size=batch_size,
            apply_norm=apply_norm,
            combiner=combiner,
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
            random_state=random_state,
            use_node_embedding=use_node_embedding,
            node_embedding_size=node_embedding_size,
            residual_convolutional_layers=residual_convolutional_layers,
            handling_multi_graph=handling_multi_graph,
            node_feature_names=node_feature_names,
            node_type_feature_names=node_type_feature_names,
            use_node_type_embedding=False,
            verbose=verbose,
        )
        AbstractNodeLabelPredictionModel.__init__(self, random_state=random_state)
        self._number_of_units_per_head_layer = normalize_model_list_parameter(
            number_of_units_per_head_layer,
            number_of_head_layers,
            object_type=int,
            can_be_empty=True
        )

    def _build_model(
        self,
        graph: Graph,
        graph_convolution_model: Model,
        edge_type_features: Optional[List[np.ndarray]] = None,
        edge_features: Optional[List[np.ndarray]] = None,
    ):
        """Create new GCN model."""
        hidden = graph_convolution_model.output

        if isinstance(hidden, list):
            hidden = Concatenate(
                name="ConcatenatedNodeFeatures",
                axis=-1
            )(hidden)

        # Building the head of the model.
        for i, units in enumerate(self._number_of_units_per_head_layer):
            if len(self._number_of_units_per_head_layer) > 1:
                ordinal = number_to_ordinal(i + 1)
            else:
                ordinal = ""
            hidden = Dense(
                units=units,
                activation="relu",
                name=f"{ordinal}HeadLayer"
            )(hidden)

        output = Dense(
            units=self.get_output_classes(graph),
            activation=self.get_output_activation_name(),
            name="Output"
        )(hidden)

        # Building the the model.
        model = Model(
            inputs=graph_convolution_model.inputs,
            outputs=output,
            name=self.model_name().replace(" ", "_")
        )

        model.compile(
            loss=self.get_loss_name(),
            optimizer=self._optimizer,
            weighted_metrics="accuracy"
        )

        return model

    def get_output_classes(self, graph: Graph) -> int:
        """Returns number of output classes."""
        if self.is_binary_prediction_task():
            return 1
        return graph.get_number_of_node_types()

    def _get_class_weights(self, graph: Graph) -> Dict[int, float]:
        """Returns dictionary with class weights."""
        nodes_number = graph.get_number_of_nodes()
        node_types_number = graph.get_number_of_node_types()
        return {
            node_type_id: nodes_number / count / node_types_number
            for node_type_id, count in graph.get_node_type_id_counts_hashmap().items()
        }

    def _get_model_training_input(
        self,
        graph: Graph,
        support: Graph,
        node_features: Optional[List[np.ndarray]],
        node_type_features: Optional[List[np.ndarray]],
        edge_type_features: Optional[List[np.ndarray]],
        edge_features: Optional[List[np.ndarray]],
    ) -> Tuple[Union[np.ndarray, Type[Sequence]]]:
        """Returns training input tuple."""
        if node_type_features is not None and len(node_type_features) > 0:
            raise NotImplementedError(
                "Node type features are not supported by this model."
            )
        
        if edge_type_features is not None and len(edge_type_features) > 0:
            raise NotImplementedError(
                "Edge type features are not supported by this model."
            )
        
        if edge_features is not None and len(edge_features) > 0:
            raise NotImplementedError(
                "Edge features are not supported by this model."
            )

        kernels = self.convert_graph_to_kernels(support)
        return (
            *(
                ()
                if kernels is None
                else kernels
            ),
            *(
                ()
                if node_features is None
                else node_features
            ),
            *(
                (graph.get_node_ids(),)
                if self._use_node_embedding
                else ()
            )
        )

    def _get_model_training_output(
        self,
        graph: Graph,
    ) -> Optional[np.ndarray]:
        """Returns training output tuple."""
        if self.is_multilabel_prediction_task():
            return graph.get_one_hot_encoded_node_types()
        if self.is_binary_prediction_task():
            return graph.get_boolean_node_type_ids()
        return graph.get_single_label_node_type_ids()

    def _get_model_training_sample_weights(
        self,
        graph: Graph,
    ) -> Optional[np.ndarray]:
        """Returns training output tuple."""
        return graph.get_known_node_types_mask().astype(np.float32)

    def _get_model_prediction_input(
        self,
        graph: Graph,
        support: Graph,
        node_features: Optional[List[np.ndarray]],
        node_type_features: Optional[List[np.ndarray]],
        edge_type_features: Optional[List[np.ndarray]],
        edge_features: Optional[List[np.ndarray]],
    ) -> Tuple[Union[np.ndarray, Type[Sequence]]]:
        """Returns dictionary with class weights."""
        return self._get_model_training_input(
            graph,
            support,
            node_features,
            node_type_features,
            edge_type_features,
            edge_features
        )

    @classmethod
    def can_use_edge_types(cls) -> bool:
        """Returns whether the model can optionally use edge types."""
        return False

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        removed = [
            "use_node_type_embedding",
            "node_type_embedding_size"
        ]
        return dict(
            **{
                key: value
                for key, value in AbstractGCN.parameters(self).items()
                if key not in removed
            }
        )
    
    @classmethod
    def supports_multilabel_prediction(cls) -> bool:
        """Returns whether the model supports multilabel prediction."""
        return True
    