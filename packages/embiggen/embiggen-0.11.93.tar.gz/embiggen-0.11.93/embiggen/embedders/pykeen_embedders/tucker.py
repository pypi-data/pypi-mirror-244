"""Submodule providing wrapper for PyKEEN's TuckER model."""
from typing import Union, Type, Dict, Any, Optional
from pykeen.training import TrainingLoop
from pykeen.models import TuckER
from embiggen.embedders.pykeen_embedders.entity_relation_embedding_model_pykeen import EntityRelationEmbeddingModelPyKEEN
from pykeen.triples import CoreTriplesFactory


class TuckERPyKEEN(EntityRelationEmbeddingModelPyKEEN):

    def __init__(
        self,
        embedding_size: int = 200,
        relation_dim: Optional[int] = None,
        dropout_0: float = 0.3,
        dropout_1: float = 0.4,
        dropout_2: float = 0.5,
        apply_batch_normalization: bool = True,
        epochs: int = 100,
        batch_size: int = 2**10,
        training_loop: Union[str, Type[TrainingLoop]
                             ] = "Stochastic Local Closed World Assumption",
        verbose: bool = False,
        random_state: int = 42,
        ring_bell: bool = False,
        enable_cache: bool = False
    ):
        """Create new PyKEEN TuckER model.
        
        Details
        -------------------------
        This is a wrapper of the TuckER implementation from the
        PyKEEN library. Please refer to the PyKEEN library documentation
        for details and posssible errors regarding this model.

        Parameters
        -------------------------
        embedding_size: int = 200
            The dimension of the embedding to compute.
        relation_dim: Optional[int] = None
            The relation embedding dimension. Defaults to `embedding_dim`.
        dropout_0: float = 0.3
            The first dropout, cf. formula
        dropout_1: float = 0.4
            The second dropout, cf. formula
        dropout_2: float = 0.5
            The third dropout, cf. formula
        apply_batch_normalization: bool = True
            Whether to apply batch normalization
        epochs: int = 100
            The number of epochs to use to train the model for.
        batch_size: int = 2**10
            Size of the training batch.
        device: str = "auto"
            The devide to use to train the model.
            Can either be cpu or cuda.
        training_loop: Union[str, Type[TrainingLoop]
                             ] = "Stochastic Local Closed World Assumption"
            The training loop to use to train the model.
            Can either be:
            - Stochastic Local Closed World Assumption
            - Local Closed World Assumption
        verbose: bool = False
            Whether to show loading bars.
        random_state: int = 42
            Random seed to use while training the model
        ring_bell: bool = False,
            Whether to play a sound when embedding completes.
        enable_cache: bool = False
            Whether to enable the cache, that is to
            store the computed embedding.
        """
        self._relation_dim=relation_dim
        self._dropout_0=dropout_0
        self._dropout_1=dropout_1
        self._dropout_2=dropout_2
        self._apply_batch_normalization=apply_batch_normalization
        super().__init__(
            embedding_size=embedding_size,
            epochs=epochs,
            batch_size=batch_size,
            training_loop=training_loop,
            verbose=verbose,
            random_state=random_state,
            ring_bell=ring_bell,
            enable_cache=enable_cache
        )

    def parameters(self) -> Dict[str, Any]:
        return dict(
            **super().parameters(),
            **dict(
                relation_dim=self._relation_dim,
                dropout_0=self._dropout_0,
                dropout_1=self._dropout_1,
                dropout_2=self._dropout_2,
                apply_batch_normalization=self._apply_batch_normalization
            )
        )

    @classmethod
    def model_name(cls) -> str:
        """Return name of the model."""
        return "TuckER"

    def _build_model(
        self,
        triples_factory: CoreTriplesFactory
    ) -> TuckER:
        """Build new TuckER model for embedding.

        Parameters
        ------------------
        graph: Graph
            The graph to build the model for.
        """
        return TuckER(
            triples_factory=triples_factory,
            embedding_dim=self._embedding_size,
            relation_dim=self._relation_dim,
            dropout_0=self._dropout_0,
            dropout_1=self._dropout_1,
            dropout_2=self._dropout_2,
            apply_batch_normalization=self._apply_batch_normalization,
            random_seed=self._random_state
        )
