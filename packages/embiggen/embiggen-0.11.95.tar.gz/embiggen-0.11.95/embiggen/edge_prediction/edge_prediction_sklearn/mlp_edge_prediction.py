"""Submodule wrapping MLP for edge prediction."""
from typing import Dict, Any, Union, List
from sklearn.neural_network import MLPClassifier
from embiggen.edge_prediction.edge_prediction_sklearn.sklearn_edge_prediction_adapter import SklearnEdgePredictionAdapter
from embiggen.utils.normalize_kwargs import normalize_kwargs


class MLPEdgePrediction(SklearnEdgePredictionAdapter):
    """Create wrapper over Sklearn MLP classifier for edge prediction."""

    def __init__(
        self,
        hidden_layer_sizes=(100,),
        activation="relu",
        solver='adam',
        alpha=0.0001,
        batch_size='auto',
        learning_rate="constant",
        learning_rate_init=0.001,
        power_t=0.5,
        max_iter=200,
        shuffle=True,
        tol=1e-4,
        verbose=False,
        warm_start=False,
        momentum=0.9,
        nesterovs_momentum=True,
        early_stopping=False,
        validation_fraction=0.1,
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-8,
        n_iter_no_change=10,
        max_fun=15000,
        edge_embedding_methods: Union[List[str], str] = "Concatenate",
        training_unbalance_rate: float = 1.0,
        use_edge_metrics: bool = False,
        use_scale_free_distribution: bool = True,
        prediction_batch_size: int = 2**12,
        random_state: int = 42
    ):
        """Create the MLP for Edge Prediction."""

        self._mlp_kwargs = normalize_kwargs(
            self,
            {
            "activation": activation,
            "solver": solver,
            "alpha": alpha,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "learning_rate_init": learning_rate_init,
            "hidden_layer_sizes": hidden_layer_sizes,
            "power_t": power_t,
            "max_iter": max_iter,
            "shuffle": shuffle,
            "tol": tol,
            "verbose": verbose,
            "warm_start": warm_start,
            "momentum": momentum,
            "nesterovs_momentum": nesterovs_momentum,
            "early_stopping": early_stopping,
            "validation_fraction": validation_fraction,
            "beta_1": beta_1,
            "beta_2": beta_2,
            "epsilon": epsilon,
            "n_iter_no_change": n_iter_no_change,
            "max_fun": max_fun,
        })

        super().__init__(
            MLPClassifier(
                **self._mlp_kwargs
            ),
            edge_embedding_methods=edge_embedding_methods,
            training_unbalance_rate=training_unbalance_rate,
            use_edge_metrics=use_edge_metrics,
            use_scale_free_distribution=use_scale_free_distribution,
            
            prediction_batch_size=prediction_batch_size,
            random_state=random_state
        )

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters used for this model."""
        return {
            **super().parameters(),
            **self._mlp_kwargs
        }

    @classmethod
    def smoke_test_parameters(cls) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        return dict(
            hidden_layer_sizes=(1,),
            max_iter=1
        )

    @classmethod
    def model_name(cls) -> str:
        return "MLP Classifier"
