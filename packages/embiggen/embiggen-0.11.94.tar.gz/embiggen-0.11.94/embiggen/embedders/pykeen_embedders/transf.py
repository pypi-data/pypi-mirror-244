"""Submodule providing wrapper for PyKEEN's TransF model."""
from typing import Union, Type, Dict, Any
from pykeen.training import TrainingLoop
from pykeen.models import TransF
from embiggen.embedders.pykeen_embedders.entity_relation_embedding_model_pykeen import EntityRelationEmbeddingModelPyKEEN
from pykeen.triples import CoreTriplesFactory


class TransFPyKEEN(EntityRelationEmbeddingModelPyKEEN):

    @classmethod
    def model_name(cls) -> str:
        """Return name of the model."""
        return "TransF"

    def _build_model(
        self,
        triples_factory: CoreTriplesFactory
    ) -> TransF:
        """Build new TransF model for embedding.

        Parameters
        ------------------
        graph: Graph
            The graph to build the model for.
        """
        return TransF(
            triples_factory=triples_factory,
            embedding_dim=self._embedding_size,
            random_seed=self._random_state
        )
