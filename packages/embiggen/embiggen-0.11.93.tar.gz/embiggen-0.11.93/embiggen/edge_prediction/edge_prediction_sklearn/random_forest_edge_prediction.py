"""Submodule wrapping Random Forest for edge prediction."""
from typing import Dict, Any, Union, List
from sklearn.ensemble import RandomForestClassifier
from embiggen.edge_prediction.edge_prediction_sklearn.decision_tree_edge_prediction import DecisionTreeEdgePrediction
from embiggen.edge_prediction.edge_prediction_sklearn.sklearn_edge_prediction_adapter import SklearnEdgePredictionAdapter
from embiggen.utils.normalize_kwargs import normalize_kwargs


class RandomForestEdgePrediction(SklearnEdgePredictionAdapter):
    """Create wrapper over Sklearn Random Forest classifier for edge prediction."""

    def __init__(
        self,
        n_estimators: int = 1000,
        criterion: str = "gini",
        max_depth: int = 10,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        min_weight_fraction_leaf: float = 0.,
        max_features="sqrt",
        max_leaf_nodes=None,
        min_impurity_decrease=0.,
        bootstrap=True,
        oob_score=False,
        n_jobs=-1,
        verbose=0,
        warm_start=False,
        ccp_alpha=0.0,
        max_samples=None,
        edge_embedding_methods: Union[List[str], str] = "Concatenate",
        training_unbalance_rate: float = 1.0,
        use_edge_metrics: bool = False,
        use_scale_free_distribution: bool = True,
        prediction_batch_size: int = 2**12,
        random_state: int = 42
    ):
        """Create the Random Forest for Edge  Prediction."""
        self._random_forest_kwargs = normalize_kwargs(
            self,
            {
                "n_estimators": n_estimators,
                "criterion": criterion,
                "max_depth": max_depth,
                "min_samples_split": min_samples_split,
                "min_samples_leaf": min_samples_leaf,
                "min_weight_fraction_leaf": min_weight_fraction_leaf,
                "max_features": max_features,
                "max_leaf_nodes": max_leaf_nodes,
                "min_impurity_decrease": min_impurity_decrease,
                "bootstrap": bootstrap,
                "oob_score": oob_score,
                "n_jobs": n_jobs,
                "random_state": random_state,
                "verbose": verbose,
                "warm_start": warm_start,
                "ccp_alpha": ccp_alpha,
                "max_samples": max_samples,
            }
        )

        super().__init__(
            RandomForestClassifier(
                **self._random_forest_kwargs
            ),
            edge_embedding_methods=edge_embedding_methods,
            training_unbalance_rate=training_unbalance_rate,
            use_edge_metrics=use_edge_metrics,
            use_scale_free_distribution=use_scale_free_distribution,
            
            prediction_batch_size=prediction_batch_size,
            random_state=random_state
        )

    @classmethod
    def smoke_test_parameters(cls) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        return dict(
            **DecisionTreeEdgePrediction.smoke_test_parameters(),
            n_estimators=1
        )

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters used for this model."""
        return {
            **super().parameters(),
            **self._random_forest_kwargs
        }

    @classmethod
    def model_name(cls) -> str:
        return "Random Forest Classifier"
