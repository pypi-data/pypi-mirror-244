"""Module providing WalkletsGloVe model implementation."""
from typing import Optional, Dict, Any
from embiggen.embedders.ensmallen_embedders.walklets import WalkletsEnsmallen


class WalkletsGloVeEnsmallen(WalkletsEnsmallen):
    """Class providing WalkletsGloVe implemeted in Rust from Ensmallen."""

    def __init__(
        self,
        embedding_size: int = 100,
        epochs: int = 100,
        walk_length: int = 512,
        window_size: int = 4,
        return_weight: float = 1.0,
        explore_weight: float = 1.0,
        max_neighbours: Optional[int] = 100,
        learning_rate: float = 0.05,
        learning_rate_decay: float = 0.9,
        central_nodes_embedding_path: Optional[str] = None,
        contextual_nodes_embedding_path: Optional[str] = None,
        alpha: float = 0.75,
        normalize_by_degree: bool = False,
        stochastic_downsample_by_degree: Optional[bool] = False,
        normalize_learning_rate_by_degree: Optional[bool] = False,
        use_scale_free_distribution: Optional[bool] = True,
        random_state: int = 42,
        dtype: str = "f32",
        ring_bell: bool = False,
        enable_cache: bool = False
    ):
        """Create new abstract Node2Vec method.

        Parameters
        --------------------------
        embedding_size: int = 100
            Dimension of the embedding.
        epochs: int = 100
            Number of epochs to train the model for.
        walk_length: int = 128
            Maximal length of the walks.
        window_size: int = 4
            Window size for the local context.
            On the borders the window size is trimmed.
        return_weight: float = 1.0
            Weight on the probability of returning to the same node the walk just came from
            Having this higher tends the walks to be
            more like a Breadth-First Search.
            Having this very high  (> 2) makes search very local.
            Equal to the inverse of p in the Node2Vec paper.
        explore_weight: float = 1.0
            Weight on the probability of visiting a neighbor node
            to the one we're coming from in the random walk
            Having this higher tends the walks to be
            more like a Depth-First Search.
            Having this very high makes search more outward.
            Having this very low makes search very local.
            Equal to the inverse of q in the Node2Vec paper.
        max_neighbours: Optional[int] = 100
            Number of maximum neighbours to consider when using approximated walks.
            By default, None, we execute exact random walks.
            This is mainly useful for graphs containing nodes with high degrees.
        learning_rate: float = 0.001
            The learning rate to use to train the Node2Vec model. By default 0.01.
        learning_rate_decay: float = 0.9
            Factor to reduce the learning rate for at each epoch. By default 0.9.
        central_nodes_embedding_path: Optional[str] = None
            Path where to mmap and store the central nodes embedding.
            If provided, we expect the path to contain the substring `{window_size}` which
            will be replaced with the i-th window size embedding that is being computed.
            This is necessary to embed large graphs whose embedding will not
            fit into the available main memory.
        contextual_nodes_embedding_path: Optional[str] = None
            Path where to mmap and store the central nodes embedding.
            If provided, we expect the path to contain the substring `{window_size}` which
            will be replaced with the i-th window size embedding that is being computed.
            This is necessary to embed large graphs whose embedding will not
            fit into the available main memory.
        alpha: float = 0.75
            Alpha parameter for GloVe's loss.
        normalize_by_degree: bool = False
            Whether to normalize the random walk by the node degree
            of the destination node degrees.
        stochastic_downsample_by_degree: Optional[bool] = False
            Randomly skip samples with probability proportional to the degree of the central node. By default false.
        normalize_learning_rate_by_degree: Optional[bool] = False
            Divide the learning rate by the degree of the central node. By default false.
        use_scale_free_distribution: Optional[bool] = True
            Sample negatives proportionally to their degree. By default true.
        dtype: str = "f32"
            The data type to be employed, by default f32.
        random_state: int = 42
            The random state to reproduce the training sequence.
        ring_bell: bool = False,
            Whether to play a sound when embedding completes.
        enable_cache: bool = False
            Whether to enable the cache, that is to
            store the computed embedding.
        """
        super().__init__(
            embedding_size=embedding_size,
            epochs=epochs,
            alpha=alpha,
            walk_length=walk_length,
            iterations=1,
            window_size=window_size,
            return_weight=return_weight,
            explore_weight=explore_weight,
            max_neighbours=max_neighbours,
            learning_rate=learning_rate,
            learning_rate_decay=learning_rate_decay,
            central_nodes_embedding_path=central_nodes_embedding_path,
            contextual_nodes_embedding_path=contextual_nodes_embedding_path,
            normalize_by_degree=normalize_by_degree,
            stochastic_downsample_by_degree=stochastic_downsample_by_degree,
            normalize_learning_rate_by_degree=normalize_learning_rate_by_degree,
            use_scale_free_distribution=use_scale_free_distribution,
            dtype=dtype,
            random_state=random_state,
            ring_bell=ring_bell,
            enable_cache=enable_cache
        )

    @classmethod
    def model_name(cls) -> str:
        """Returns name of the model."""
        return "Walklets GloVe"

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        removed = [
            "number_of_negative_samples",
            "clipping_value",
            "iterations"
        ]
        return dict(
            **{
                key: value
                for key, value in super().parameters().items()
                if key not in removed
            }
        )