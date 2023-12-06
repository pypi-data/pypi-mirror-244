"""NodeTransformer class to convert nodes to edge embeddings."""
from typing import List, Union, Optional
import numpy as np
import pandas as pd
from ensmallen import Graph


class NodeTransformer:
    """NodeTransformer class to convert nodes to edge embeddings."""

    def __init__(
        self,
        aligned_mapping: bool = False,
    ):
        """Create new NodeTransformer object.

        Parameters
        -------------------
        aligned_mapping: bool = False,
            This parameter specifies whether the mapping of the embeddings nodes
            matches the internal node mapping of the given graph.
            If these two mappings do not match, the generated edge embedding
            will be meaningless.
        """
        self._node_feature = []
        self._node_type_feature = []
        self._aligned_mapping = aligned_mapping

    def fit(
        self,
        node_feature: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        node_type_feature: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
    ):
        """Fit the model.

        Parameters
        -------------------------
        node_feature: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            Node feature to use to fit the transformer.
        node_type_feature: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            Node type feature to use to fit the transformer.
        """
        if node_feature is None:
            node_feature = []
        if not isinstance(node_feature, list):
            node_feature = [node_feature]

        if node_type_feature is None:
            node_type_feature = []
        if not isinstance(node_type_feature, list):
            node_type_feature = [node_type_feature]

        # We check if any of the provided node features
        # is neither a numpy array nor a pandas dataframe.
        for features, feature_name in (
            (node_type_feature, "node type"),
            (node_feature, "node"),
        ):
            for feature in features:
                if not isinstance(feature, (pd.DataFrame, np.ndarray)):
                    raise ValueError(
                        (
                            f"One of the provided {feature_name} features is not "
                            "neither a pandas DataFrame nor a numpy array, but "
                            f"of type {type(feature)}. It is not clear "
                            "what to do with this feature."
                        )
                    )
                # We check whether the provided features contain any NaN
                if isinstance(feature, pd.DataFrame) and feature.isna().any().any():
                    raise ValueError(
                        (
                            f"One of the provided {feature_name} features contains NaNs. "
                            "This is not supported. The DataFrame has shape "
                            f"{feature.shape} and the first 5 rows are:\n"
                            f"{feature.head(5)}"
                        )
                    )
                
                if isinstance(feature, np.ndarray) and np.isnan(feature).any():
                    raise ValueError(
                        (
                            f"One of the provided {feature_name} features contains NaNs. "
                            "This is not supported. The array has shape "
                            f"{feature.shape} and the first 5 rows are:\n"
                            f"{feature[:5]}"
                        )
                    )
                

            # We check if, while the parameters for alignment
            # has not been provided, numpy arrays were provided.
            # This would be an issue as we cannot check for alignment
            # in numpy arrays.
            if not self._aligned_mapping and any(
                isinstance(nf, np.ndarray)
                for nf in features
            ):
                raise ValueError(
                    "A numpy array feature was provided while the "
                    f"aligned mapping parameter was set to false. "
                    "If you intend to specify that you are providing a numpy "
                    f"array {feature_name} feature that is aligned with the vocabulary "
                    "of the graph set the `aligned_mapping` parameter "
                    "to True."
                )

        if self._aligned_mapping:
            if len(node_feature) > 1:
                self._node_feature = np.hstack([
                    nf.to_numpy() if isinstance(nf, pd.DataFrame) else nf
                    for nf in node_feature
                ])
            elif len(node_feature) == 1:
                self._node_feature = node_feature[0]

            if len(node_type_feature) > 1:
                self._node_type_feature = np.hstack([
                    nf.to_numpy() if isinstance(nf, pd.DataFrame) else nf
                    for nf in node_type_feature
                ])
            elif len(node_type_feature) == 1:
                self._node_type_feature = node_type_feature[0]
        else:
            if len(node_feature) > 0:
                self._node_feature = pd.concat(node_feature, axis=1)
            if len(node_type_feature) > 0:
                self._node_type_feature = pd.concat(node_type_feature, axis=1)

    def has_node_type_features(self) -> bool:
        """Return whether the transformer has node type feature."""
        return len(self._node_type_feature) > 0
    
    def has_node_features(self) -> bool:
        """Return whether the transformer has node feature."""
        return len(self._node_feature) > 0

    def is_aligned_mapping(self) -> bool:
        """Return whether the transformer can assume aligned mapping."""
        return self._aligned_mapping

    def is_fit(self) -> bool:
        """Return whether the transformer is fitted."""
        return len(self._node_feature) + len(self._node_type_feature) > 0

    def transform(
        self,
        nodes: Optional[Union[Graph, List[str], List[int]]] = None,
        node_types: Optional[Union[Graph, List[Optional[List[str]]], List[Optional[List[int]]]]] = None,
    ) -> np.ndarray:
        """Return embeddings from given node.

        Parameters
        --------------------------
        nodes: Optional[Union[List[str], List[int]]] = None
            List of nodes whose embedding is to be returned.
            This can be either a list of strings, or a graph, or if the
            aligned_mapping is setted, then this methods also accepts
            a list of ints.
        node_types: Optional[Union[Graph, List[Optional[List[str]]], List[Optional[List[int]]]]] = None,
            List of node types whose embedding is to be returned.
            This can be either a list of strings, or a graph, or if the
            aligned_mapping is setted, then this methods also accepts
            a list of ints.

        Raises
        --------------------------
        ValueError,
            If embedding is not fitted.

        Returns
        --------------------------
        Numpy array of embeddings.
        """
        if not self.is_fit():
            raise ValueError(
                "Transformer was not fitted yet."
            )

        node_type_features = None
        node_features = None

        if self._aligned_mapping:
            if nodes is not None and self.has_node_features():
                if not isinstance(nodes, (np.ndarray, Graph)):
                    raise ValueError(
                        "The provided nodes are not numpy array and the "
                        "node IDs or Graph are expected to be aligned."
                    )

                if isinstance(nodes, Graph):
                    node_features = self._node_feature
                else:
                    node_features = self._node_feature[nodes]

            if node_types is not None and self.has_node_type_features():
                if isinstance(node_types, Graph):
                    node_types = node_types.get_node_type_ids()
                    if isinstance(nodes, np.ndarray):
                        node_types = [
                            node_types[node]
                            for node in nodes
                        ]
                node_type_feature_dimensionality = self._node_type_feature.shape[1]
                node_type_features = np.vstack([
                    np.mean(
                        self._node_type_feature[node_type_ids],
                        axis=0
                    )
                    if node_type_ids is not None
                    else
                    np.zeros(shape=node_type_feature_dimensionality)
                    for node_type_ids in node_types
                ])
        else:
            if nodes is not None and self.has_node_features():
                if isinstance(nodes, Graph):
                    nodes = nodes.get_node_names()

                node_features = self._node_feature.loc[nodes].to_numpy()

            if node_types is not None and self.has_node_type_features():
                node_type_feature_dimensionality = self._node_type_feature.shape[1]
                node_type_features = np.vstack([
                    np.mean(
                        self._node_feature.loc[node_type_names].to_numpy(),
                        axis=0
                    )
                    if node_type_names is not None
                    else
                    np.zeros(shape=node_type_feature_dimensionality)
                    for node_type_names in node_types
                ])

        if node_features is None:
            node_features = node_type_features
        elif node_type_features is not None:
            node_features = np.hstack([
                node_features,
                node_type_features
            ])

        return node_features
