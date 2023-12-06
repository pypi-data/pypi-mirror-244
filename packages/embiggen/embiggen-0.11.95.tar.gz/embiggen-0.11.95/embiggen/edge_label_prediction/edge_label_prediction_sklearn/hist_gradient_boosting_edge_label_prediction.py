"""Submodule wrapping Hist Gradient Boosting for edge label prediction."""
from typing import Dict, Any, Union, List
from sklearn.ensemble import HistGradientBoostingClassifier
from embiggen.edge_label_prediction.edge_label_prediction_sklearn.sklearn_edge_label_prediction_adapter import SklearnEdgeLabelPredictionAdapter
from embiggen.utils.normalize_kwargs import normalize_kwargs


class HistGradientBoostingEdgeLabelPrediction(SklearnEdgeLabelPredictionAdapter):
    """Create wrapper over Sklearn Hist Gradient Boosting classifier for edge label prediction."""

    def __init__(
        self,
        loss='log_loss',
        learning_rate=0.1,
        max_iter: int = 100,
        max_leaf_nodes: int = 31,
        max_depth: int = 3,
        min_samples_leaf: int = 20,
        l2_regularization: float = 0.,
        max_bins: int = 255,
        categorical_features=None,
        monotonic_cst=None,
        interaction_cst=None,
        warm_start=False,
        early_stopping="auto",
        scoring="loss",
        validation_fraction=0.1,
        n_iter_no_change=10,
        tol=1e-7,
        verbose=0,
        class_weight=None,
        edge_embedding_methods: Union[List[str], str] = "Concatenate",
        use_edge_metrics: bool = False,
        random_state: int = 42
    ):
        """Create the Hist Gradient Boosting for Edge Label Prediction."""

        self._kwargs = normalize_kwargs(self, dict(
            loss=loss,
            learning_rate=learning_rate,
            max_iter=max_iter,
            max_leaf_nodes=max_leaf_nodes,
            max_depth=max_depth,
            min_samples_leaf=min_samples_leaf,
            l2_regularization=l2_regularization,
            max_bins=max_bins,
            categorical_features=categorical_features,
            monotonic_cst=monotonic_cst,
            interaction_cst=interaction_cst,
            warm_start=warm_start,
            early_stopping=early_stopping,
            scoring=scoring,
            validation_fraction=validation_fraction,
            n_iter_no_change=n_iter_no_change,
            tol=tol,
            verbose=verbose,
            class_weight=class_weight,
        ))

        super().__init__(
            HistGradientBoostingClassifier(
                **self._kwargs,
                random_state=random_state
            ),
            edge_embedding_methods=edge_embedding_methods,
            use_edge_metrics=use_edge_metrics,
            random_state=random_state
        )

    @classmethod
    def smoke_test_parameters(cls) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        return dict(
            max_depth=1,
            max_iter=2
        )

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters used for this model."""
        return {
            **super().parameters(),
            **self._kwargs
        }

    @classmethod
    def model_name(cls) -> str:
        return "Hist Gradient Boosting Classifier"
