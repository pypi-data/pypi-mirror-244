"""Subclass providing EmbeddingResult object."""
import inspect
import types
import warnings
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd


class EmbeddingResult:

    def __init__(
        self,
        embedding_method_name: str,
        node_embeddings: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        edge_embeddings: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        node_type_embeddings: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        edge_type_embeddings: Optional[Union[pd.DataFrame,
                                             np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
    ):
        """Create new Embedding Result.

        Parameters
        ---------------------------
        embedding_method_name: str
            The embedding algorithm used.
        node_embeddings: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node embedding(s).
            Some algorithms return multiple node embedding.
        edge_embeddings: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge embedding(s).
            Some algorithms return multiple edge embedding.
        node_type_embeddings: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node type embedding(s).
            Some algorithms return multiple node type embedding.
        edge_type_embeddings: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge type embedding(s).
            Some algorithms return multiple edge type embedding.
        """
        if node_embeddings is not None and not isinstance(node_embeddings, list):
            node_embeddings = [node_embeddings]

        if edge_embeddings is not None and not isinstance(edge_embeddings, list):
            edge_embeddings = [edge_embeddings]

        if node_type_embeddings is not None and not isinstance(node_type_embeddings, list):
            node_type_embeddings = [node_type_embeddings]

        if edge_type_embeddings is not None and not isinstance(edge_type_embeddings, list):
            edge_type_embeddings = [edge_type_embeddings]

        for embedding_list, embedding_list_name in (
            (node_embeddings, "node embedding"),
            (edge_embeddings, "edge embedding"),
            (node_type_embeddings, "node type embedding"),
            (edge_type_embeddings, "node edge embedding"),
        ):
            if embedding_list is None:
                continue
            for embedding in embedding_list:

                if not isinstance(embedding, (np.ndarray, pd.DataFrame)):
                    raise ValueError(
                        f"One of the provided {embedding_list_name} "
                        f"computed with the {embedding_method_name} method is neither a "
                        f"numpy array or a pandas DataFrame, but a `{type(embedding)}` object."
                    )
                
                if embedding.shape[0] == 0:
                    raise ValueError(
                        "One of the provided {embedding_list_name} "
                        f"computed with the {embedding_method_name} method "
                        "is empty."
                    )
                
                # If the embedding size is too big, we skip the checking step.
                if embedding.shape[0] > 1_000_000:
                    continue

                if isinstance(embedding, pd.DataFrame):
                    numpy_embedding = embedding.to_numpy()
                else:
                    numpy_embedding = embedding

                if np.isnan(numpy_embedding).any():
                    raise ValueError(
                        f"One of the provided {embedding_list_name} "
                        f"computed with the {embedding_method_name} method "
                        "contains NaN values."
                    )

                if np.isinf(numpy_embedding).any():
                    number = np.sum(np.isinf(numpy_embedding))
                    raise ValueError(
                        f"One of the provided {embedding_list_name} "
                        f"computed with the {embedding_method_name} method "
                        f"contains {number} infinite values."
                    )

                if np.isclose(numpy_embedding, 0.0).all():
                    warnings.warn(
                        f"One of the provided {embedding_list_name} "
                        f"computed with the {embedding_method_name} method "
                        "contains exclusively zeros."
                    )

        self._embedding_method_name: str = embedding_method_name
        self._node_embeddings: List[np.ndarray] = node_embeddings
        self._edge_embeddings: List[np.ndarray] = edge_embeddings
        self._node_type_embeddings: List[np.ndarray] = node_type_embeddings
        self._edge_type_embeddings: List[np.ndarray] = edge_type_embeddings

        if self.is_single_embedding():
            embedding = self.get_single_embedding()
            for method_name, method in inspect.getmembers(
                embedding, lambda o: isinstance(o, types.MethodType)
            ):
                def metawrap(method_name: str):
                    def wrapper(*args, **kwargs):
                        return getattr(embedding, method_name)(
                            *args,
                            **kwargs
                        )
                    wrapper.__doc__ = method.__doc__
                    wrapper.__name__ = method.__name__
                    return wrapper

                setattr(self, method_name, metawrap(method_name))


    def get_single_embedding(self) -> Union[np.ndarray, pd.DataFrame]:
        """Returns the single non-None embedding."""
        assert self.is_single_embedding()
        for embeddings in (
            self._node_embeddings,
            self._edge_embeddings,
            self._node_type_embeddings,
            self._edge_type_embeddings
        ):
            if embeddings is not None:
                return embeddings[0]

    def is_single_embedding(self) -> bool:
        """Returns whether the wrapper contains a single embedding."""
        return self.number_of_embeddings() == 1

    def number_of_embeddings(self) -> int:
        """Returns the number of embedding included in the wrapper."""
        total = 0
        for embeddings in (
            self._node_embeddings,
            self._edge_embeddings,
            self._node_type_embeddings,
            self._edge_type_embeddings
        ):
            if embeddings is not None:
                total += len(embeddings)
        return total

    def get_all_node_embedding(self) -> List[Union[pd.DataFrame, np.ndarray]]:
        """Return a list with all the computed node embedding.
        
        Implementation details
        ----------------------
        Different embedding methods compute a different number of node embeddings.
        For example, the LINE method computes a single embedding for each node,
        while an embedding based on SkipGram, such as Node2Vec SkipGram,
        computes two embeddings for each node: one for the node context and one for the node itself.

        For this reason, to standardize the access to the node embeddings,
        this method returns a list of node embeddings.

        Raises
        ----------------
        ValueError
            If the node embeddings were not computed by the embedding method.
        """
        if self._node_embeddings is None:
            raise ValueError(
                "The node embedding were requested but they "
                f"were not computed by the {self._embedding_method_name} method."
            )
        return self._node_embeddings

    def get_all_edge_embedding(self) -> List[Union[pd.DataFrame, np.ndarray]]:
        """Return a list with all the computed edge embedding.
        
        Implementation details
        ----------------------
        Different embedding methods compute a different number of edge embeddings.
        For example, a method such as HyperSketching produces three different edge
        embeddings for each edge: one for the exclusive overlaps matrix, one for the
        exclusive left difference and one for the exclusive right difference.

        For this reason, to standardize the access to the edge embeddings,
        this method returns a list of edge embeddings.

        Raises
        ----------------
        ValueError
            If the edge embeddings were not computed by the embedding method.

        """
        if self._edge_embeddings is None:
            raise ValueError(
                "The edge embedding were requested but they "
                f"were not computed by the {self._embedding_method_name} method."
            )
        return self._edge_embeddings

    def get_all_node_type_embeddings(self) -> List[Union[pd.DataFrame, np.ndarray]]:
        """Return a list with all the computed node type embedding."""
        if self._node_type_embeddings is None:
            raise ValueError(
                "The node types embedding were requested but they "
                f"were not computed by the {self._embedding_method_name} method."
            )
        return self._node_type_embeddings

    def get_all_edge_type_embeddings(self) -> List[Union[pd.DataFrame, np.ndarray]]:
        """Return a list with all the computed edge type embedding."""
        if self._edge_type_embeddings is None:
            raise ValueError(
                "The edge types embedding were requested but they "
                f"were not computed by the {self._embedding_method_name} method."
            )
        return self._edge_type_embeddings

    def get_node_embedding_from_index(self, index: int) -> Union[pd.DataFrame, np.ndarray]:
        """Return a computed node embedding curresponding to the provided index.

        Parameters
        ----------------
        index: int
            The index of the node embedding to return.

        Raises
        ----------------
        IndexError
            If the provided index is higher than the number of available embeddings.
        """
        if index >= len(self._node_embeddings):
            raise ValueError(
                f"The node embedding computed with the {self._embedding_method_name} method "
                f"are {len(self._node_embeddings)}, but you requested the embedding "
                f"in position {index}."
            )
        return self._node_embeddings[index]

    def get_edge_embedding_from_index(self, index: int) -> Union[pd.DataFrame, np.ndarray]:
        """Return a computed edge embedding curresponding to the provided index.

        Parameters
        ----------------
        index: int
            The index of the edge embedding to return.

        Raises
        ----------------
        IndexError
            If the provided index is higher than the number of available embeddings.
        """
        if index >= len(self._edge_embeddings):
            raise ValueError(
                f"The edge embedding computed with the {self._embedding_method_name} method "
                f"are {len(self._edge_embeddings)}, but you requested the embedding "
                f"in position {index}."
            )
        return self._edge_embeddings[index]

    def get_node_type_embedding_from_index(self, index: int) -> Union[pd.DataFrame, np.ndarray]:
        """Return a computed node type embedding curresponding to the provided index.

        Parameters
        ----------------
        index: int
            The index of the node type embedding to return.

        Raises
        ----------------
        IndexError
            If the provided index is higher than the number of available embeddings.
        """
        node_types_embedding = self.get_all_node_type_embeddings()
        if index >= len(node_types_embedding):
            raise ValueError(
                f"The node type embedding computed with the {self._embedding_method_name} method "
                f"are {len(node_types_embedding)}, but you requested the embedding "
                f"in position {index}."
            )
        return node_types_embedding[index]

    def get_edge_type_embedding_from_index(self, index: int) -> Union[pd.DataFrame, np.ndarray]:
        """Return a computed edge type embedding curresponding to the provided index.

        Parameters
        ----------------
        index: int
            The index of the edge type embedding to return.

        Raises
        ----------------
        IndexError
            If the provided index is higher than the number of available embeddings.
        """
        edge_types_embedding = self.get_all_edge_type_embeddings()
        if index >= len(edge_types_embedding):
            raise ValueError(
                f"The edge type embedding computed with the {self._embedding_method_name} method "
                f"are {len(edge_types_embedding)}, but you requested the embedding "
                f"in position {index}."
            )
        return edge_types_embedding[index]
    
    @property
    def embedding_method_name(self) -> str:
        """Returns the name of the method used for this embedding."""
        return self._embedding_method_name

    @staticmethod
    def load(cached_embedding_result: Dict[str, Union[str, List[Union[np.ndarray, pd.DataFrame]]]]) -> "EmbeddingResult":
        """Return restored embedding result."""
        return EmbeddingResult(**cached_embedding_result)

    def dump(self) -> Dict[str, Union["CachableList", "CachableValue"]]:
        """Method to cache the embedding result object."""
        return {
            "embedding_method_name": self._embedding_method_name,
            "node_embeddings": self._node_embeddings,
            "edge_embeddings": self._edge_embeddings,
            "node_type_embeddings": self._node_type_embeddings,
            "edge_type_embeddings": self._edge_type_embeddings,
        }
