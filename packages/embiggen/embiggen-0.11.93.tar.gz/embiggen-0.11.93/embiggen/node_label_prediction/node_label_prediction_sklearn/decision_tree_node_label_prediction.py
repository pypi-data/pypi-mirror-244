"""Submodule wrapping Decision Tree for Node-label prediction."""
from typing import Dict, Any
from sklearn.tree import DecisionTreeClassifier
from embiggen.node_label_prediction.node_label_prediction_sklearn.sklearn_node_label_prediction_adapter import SklearnNodeLabelPredictionAdapter


class DecisionTreeNodeLabelPrediction(SklearnNodeLabelPredictionAdapter):
    """Create wrapper over Sklearn Random Forest classifier for Node-label prediction."""

    def __init__(
        self,
        criterion="gini",
        splitter="best",
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1,
        min_weight_fraction_leaf=0.,
        max_features="sqrt",
        max_leaf_nodes=None,
        min_impurity_decrease=0.,
        class_weight="balanced",
        ccp_alpha=0.0,
        random_state: int = 42
    ):
        """Create the Decision Tree for Node-label prediction."""
        self._criterion = criterion
        self._splitter = splitter
        self._max_depth = max_depth
        self._min_samples_split = min_samples_split
        self._min_samples_leaf = min_samples_leaf
        self._min_weight_fraction_leaf = min_weight_fraction_leaf
        self._max_features = max_features
        self._max_leaf_nodes = max_leaf_nodes
        self._min_impurity_decrease = min_impurity_decrease
        self._random_state = random_state
        self._class_weight = class_weight
        self._ccp_alpha = ccp_alpha

        super().__init__(
            DecisionTreeClassifier(
                criterion=criterion,
                splitter=splitter,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                min_weight_fraction_leaf=min_weight_fraction_leaf,
                max_features=max_features,
                max_leaf_nodes=max_leaf_nodes,
                min_impurity_decrease=min_impurity_decrease,
                random_state=random_state,
                class_weight=class_weight,
                ccp_alpha=ccp_alpha,
            ),
            random_state
        )

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters used for this model."""
        return {
            **super().parameters(),
            **dict(
                criterion=self._criterion,
                splitter=self._splitter,
                max_depth=self._max_depth,
                min_samples_split=self._min_samples_split,
                min_samples_leaf=self._min_samples_leaf,
                min_weight_fraction_leaf=self._min_weight_fraction_leaf,
                max_features=self._max_features,
                max_leaf_nodes=self._max_leaf_nodes,
                min_impurity_decrease=self._min_impurity_decrease,
                random_state=self._random_state,
                class_weight=self._class_weight,
                ccp_alpha=self._ccp_alpha,
            )
        }

    @classmethod
    def smoke_test_parameters(cls) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        return dict(
            max_depth=1,
        )

    @classmethod
    def model_name(cls) -> str:
        return "Decision Tree Classifier"

    @classmethod
    def supports_multilabel_prediction(cls) -> bool:
        """Returns whether the model supports multilabel prediction."""
        return True