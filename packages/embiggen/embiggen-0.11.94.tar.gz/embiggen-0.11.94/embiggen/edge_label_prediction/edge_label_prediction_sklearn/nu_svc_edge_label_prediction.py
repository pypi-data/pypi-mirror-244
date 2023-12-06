"""Submodule wrapping Nu Support Vector Machine for Edge-label prediction."""
from typing import Dict, Any, Union, List
from sklearn.svm import NuSVC
from embiggen.node_label_prediction.node_label_prediction_sklearn.sklearn_node_label_prediction_adapter import (
    SklearnNodeLabelPredictionAdapter,
)
from embiggen.utils import normalize_kwargs


class NuSVCEdgeLabelPrediction(SklearnNodeLabelPredictionAdapter):
    """Create wrapper over Sklearn Nu Support Vector Machine classifier for Edge-label prediction."""

    def __init__(
        self,
        nu: float = 0.1,
        kernel: str = "rbf",
        degree: int = 3,
        gamma: str = "scale",
        coef0: float = 0.0,
        shrinking: bool = True,
        probability: bool = False,
        tol: float = 1e-3,
        cache_size: int = 200,
        class_weight: Union[Dict, str] = "balanced",
        verbose: bool = False,
        max_iter: int = -1,
        decision_function_shape: str = "ovr",
        break_ties: bool = False,
        edge_embedding_methods: Union[List[str], str] = "Concatenate",
        use_edge_metrics: bool = False,
        random_state: int = 42,
    ):
        """Create the Nu SVC for Edge-label prediction."""
        self._kwargs = normalize_kwargs(
            self,
            dict(
                nu=nu,
                kernel=kernel,
                degree=degree,
                gamma=gamma,
                coef0=coef0,
                shrinking=shrinking,
                probability=probability,
                tol=tol,
                cache_size=cache_size,
                class_weight=class_weight,
                verbose=verbose,
                max_iter=max_iter,
                decision_function_shape=decision_function_shape,
                break_ties=break_ties,
            )
        )

        super().__init__(
            NuSVC(**self._kwargs, random_state=random_state),
            edge_embedding_methods=edge_embedding_methods,
            use_edge_metrics=use_edge_metrics,
            random_state=random_state,
        )

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters used for this model."""
        return {**super().parameters(), **self._kwargs}
    
    @classmethod
    def smoke_test_parameters(cls) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        return dict(max_iter=1)

    @classmethod
    def model_name(cls) -> str:
        return "Nu Support Vector Classifier"
