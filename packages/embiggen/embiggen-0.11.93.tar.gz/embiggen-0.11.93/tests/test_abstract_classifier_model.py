import pytest
from embiggen.utils import AbstractClassifierModel
from unittest import TestCase


class ClassForTestAbstractClassifierModelNonStocastic(AbstractClassifierModel):

    def __init__(self):
        super().__init__()

    @classmethod
    def is_stocastic(cls) -> bool:
        return False

    @classmethod
    def requires_edge_weights(cls) -> bool:
        return True

    @classmethod
    def requires_node_types(cls) -> bool:
        return True

    @classmethod
    def requires_edge_types(cls) -> bool:
        return True
    
    @classmethod
    def model_name(cls) -> str:
        return "test_method_name"
    
    @classmethod
    def library_name(cls) -> str:
        return "Embiggen"
    
    @classmethod
    def task_name(cls) -> str:
        return "test_task_name"
    
    @classmethod
    def can_use_edge_type_features(cls) -> bool:
        return False
    
    @classmethod
    def can_use_edge_features(cls) -> bool:
        return False


class TestAbstractClassifierModel(TestCase):

    def setUp(self):
        pass

    def test_not_implemented_methods(self):
        
        non_stocastic = ClassForTestAbstractClassifierModelNonStocastic()

        for method_name, params in (
            ("_fit", (None,)),
            ("_predict", (None,)),
            ("_predict_proba", (None,)),
            ("is_binary_prediction_task", ()),
            ("is_multilabel_prediction_task", ()),
            ("get_available_evaluation_schemas", ()),
            ("_evaluate", (None, None, None)),
            ("_prepare_evaluation", (None, None, None)),
        ):
            with pytest.raises(NotImplementedError):
                non_stocastic.__getattribute__(method_name)(*params)
