"""Submodule providing classification evaluation pipeline."""
from typing import Callable, Union, List, Optional, Iterator, Type, Dict, Any
from ensmallen import Graph
from ensmallen.datasets import get_dataset
import pandas as pd
import numpy as np
from tqdm.auto import tqdm
from embiggen.utils.abstract_edge_feature import AbstractEdgeFeature
from embiggen.utils.abstract_models import AbstractClassifierModel, AbstractEmbeddingModel, AbstractFeaturePreprocessor


def iterate_graphs(
    graphs: Union[Graph, List[Graph]],
    repositories: Optional[Union[str, List[str]]] = None,
    versions: Optional[Union[str, List[str]]] = None,
    graph_callback: Optional[Callable[[Graph], Graph]] = None,
) -> Iterator[Graph]:
    """Returns iterator over provided graphs.

    Parameters
    ------------------
    graphs: Union[Graph, List[Graph]]
        The graph or graphs to iterate on.
    repositories: Optional[Union[str, List[str]]] = None
        The repositories from where to retrieve these graphs.
        This only applies for the graph names that are available
        from the ensmallen automatic retrieval.
    versions: Optional[Union[str, List[str]]] = None
        The versions of the graphs to be retrieved.
        When this is left to none, the retrieved version will be
        the one that has been indicated to be the most recent one.
        This only applies for the graph names that are available
        from the ensmallen automatic retrieval.
    graph_callback: Optional[Callable[[Graph], Graph]] = None
        Callback to use for graph normalization and sanitization, must be
        a function that receives and returns a graph object.
        For instance this may be used for filtering the uncertain edges
        in graphs such as STRING PPIs.
    """
    if not isinstance(graphs, (list, tuple)):
        graphs = [graphs]

    for graph in graphs:
        if not isinstance(graph, (str, Graph)):
            raise ValueError(
                "The graph objects should either be strings when "
                "they are graphs to be automatically retrieved or "
                "alternatively graph object instances, but you "
                f"provided an object of type {type(graph)}."
            )

    number_of_graphs = len(graphs)

    if number_of_graphs == 0:
        raise ValueError(
            "An empty list of graphs was provided."
        )

    if not isinstance(repositories, (list, tuple)):
        repositories = [repositories] * number_of_graphs

    number_of_repositories = len(repositories)

    if number_of_graphs != number_of_repositories:
        raise ValueError(
            f"The number of provided graphs `{number_of_graphs}` does not match "
            f"the number of provided repositories `{number_of_repositories}`."
        )

    if not isinstance(versions, (list, tuple)):
        versions = [versions] * number_of_graphs

    number_of_versions = len(versions)

    if number_of_graphs != number_of_versions:
        raise ValueError(
            f"The number of provided graphs `{number_of_graphs}` does not match "
            f"the number of provided versions `{number_of_versions}`."
        )

    for graph in graphs:
        if not isinstance(graph, (str, Graph)):
            raise ValueError(
                "The provided classifier graph is expected to be "
                "either an Ensmallen graph object or a string with the graph name "
                f"but an object of type {type(graph)} was provided."
            )

    for graph, version, repository in tqdm(
        zip(graphs, versions, repositories),
        desc="Graphs",
        total=number_of_graphs,
        disable=number_of_graphs == 1,
        dynamic_ncols=True,
        leave=False
    ):
        if isinstance(graph, str):
            graph = get_dataset(
                graph_name=graph,
                repository=repository,
                version=version
            )()
        if graph_callback is not None:
            graph = graph_callback(graph)
        yield graph


def classification_evaluation_pipeline(
    evaluation_schema: str,
    holdouts_kwargs: Dict[str, Any],
    graphs: Union[str, Graph, List[Graph], List[str]],
    models: Union[Type[AbstractClassifierModel], List[Type[AbstractClassifierModel]]],
    expected_parent_class: Type[AbstractClassifierModel],
    node_features: Optional[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel], List[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]]]] = None,
    node_type_features: Optional[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel], List[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]]]] = None,
    edge_type_features: Optional[Union[str, Type[AbstractEdgeFeature], pd.DataFrame, np.ndarray, List[Union[str, Type[AbstractEdgeFeature], pd.DataFrame, np.ndarray]]]] = None,
    edge_features: Optional[Union[str, Type[AbstractEdgeFeature], pd.DataFrame, np.ndarray, List[Union[str, Type[AbstractEdgeFeature], pd.DataFrame, np.ndarray]]]] = None,
    node_features_preprocessing_steps: Optional[Union[Type[AbstractFeaturePreprocessor], List[Type[AbstractFeaturePreprocessor]]]] = None,
    library_names: Optional[Union[str, List[str]]] = None,
    graph_callback: Optional[Callable[[Graph], Graph]] = None,
    subgraph_of_interest: Optional[Graph] = None,
    use_subgraph_as_support: bool = False,
    number_of_holdouts: int = 10,
    random_state: int = 42,
    repositories: Optional[Union[str, List[str]]] = None,
    versions: Optional[Union[str, List[str]]] = None,
    enable_cache: bool = False,
    precompute_constant_stocastic_features: bool = False,
    smoke_test: bool = False,
    number_of_slurm_nodes: Optional[int] = None,
    slurm_node_id_variable: str = "SLURM_GRAPE_ID",
    **evaluation_kwargs
) -> pd.DataFrame:
    """Execute classification pipeline for all provided models and graphs.
    
    Parameters
    ---------------------
    evaluation_schema: str
        The evaluation schema to follow.
    holdouts_kwargs: Dict[str, Any]
        The parameters for the selected holdouts method.
    graphs: Union[str, Graph, List[Graph], List[str]]
        The graphs or graph names to run this evaluation on.
    models: Union[Type[AbstractClassifierModel], List[Type[AbstractClassifierModel]]]
        The models to evaluate.
    expected_parent_class: Type[AbstractClassifierModel]
        The expected parent class of the models, necessary to validate that the models are what we expect.
    node_features: Optional[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel], List[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]]]] = None
        The node features to use.
    node_type_features: Optional[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel], List[Union[str, pd.DataFrame, np.ndarray, Type[AbstractEmbeddingModel]]]]] = None
        The node type features to use.
    edge_type_features: Optional[Union[str, Type[AbstractEdgeFeature], pd.DataFrame, np.ndarray, List[Union[str, Type[AbstractEdgeFeature], pd.DataFrame, np.ndarray]]]] = None
        The edge type features to use.
    edge_features: Optional[Union[str, Type[AbstractEdgeFeature], pd.DataFrame, np.ndarray, List[Union[str, Type[AbstractEdgeFeature], pd.DataFrame, np.ndarray]]]] = None
        The edge features to use.
    node_features_preprocessing_steps: Optional[Union[Type[AbstractFeaturePreprocessor], List[Type[AbstractFeaturePreprocessor]]]] = None
        The preprocessing steps to use for the node features.
    library_names: Optional[Union[str, List[str]]] = None
        Library names from where to retrieve the provided model names.
    graph_callback: Optional[Callable[[Graph], Graph]] = None
        Callback to use for graph normalization and sanitization, must be
        a function that receives and returns a graph object.
        For instance this may be used for filtering the uncertain edges
        in graphs such as STRING PPIs.
    subgraph_of_interest: Optional[Graph] = None
        Optional subgraph where to focus the task.
        This is applied to the train and test graph
        after the desired holdout schema is applied.
    use_subgraph_as_support: bool = False
        Whether to use the provided subgraph as support or
        to use the train graph (not filtered by the subgraph).
    number_of_holdouts: int = 10
        The number of holdouts to execute.
    random_state: int = 42
        Random state to reproduce this evaluation.
    repositories: Optional[Union[str, List[str]]] = None
        Repositories from where to retrieve the provided graph names
        from the Ensmallen automatic retrieval.
    versions: Optional[Union[str, List[str]]] = None
        Graph versions to retrieve.
    enable_cache: bool = False
        Whether to enable the cache.
    precompute_constant_stocastic_features: bool = False
        Whether to precompute once the constant automatic stocastic
        features before starting the embedding loop. This means that,
        when left set to false, while the features will be computed
        using the same input data, the random state between runs will
        be different and therefore the experiment performance will
        capture more of the variance derived from the stocastic aspect
        of the considered method. When set to true, they are only computed
        once and therefore the experiment will be overall faster.
    smoke_test: bool = False
        Whether this run should be considered a smoke test
        and therefore use the smoke test configurations for
        the provided model names and feature names.
        This parameter will also turn off the cache.
    number_of_slurm_nodes: Optional[int] = None
        Number of SLURM nodes to consider as available.
        This variable is used to parallelize the holdouts accordingly.
    slurm_node_id_variable: str = "SLURM_GRAPE_ID"
        Name of the system variable to use as SLURM node id.
        It must be set in the slurm bash script.
    **evaluation_kwargs: Dict
        Keyword arguments to forward to evaluation.
    """
    enable_cache = enable_cache and not smoke_test
    return pd.concat([
        expected_parent_class.evaluate(
            models=models,
            library_names=library_names,
            graph=graph,
            evaluation_schema=evaluation_schema,
            holdouts_kwargs=holdouts_kwargs,
            node_features=node_features,
            node_type_features=node_type_features,
            edge_type_features=edge_type_features,
            edge_features=edge_features,
            node_features_preprocessing_steps=node_features_preprocessing_steps,
            subgraph_of_interest=subgraph_of_interest,
            use_subgraph_as_support=use_subgraph_as_support,
            number_of_holdouts=number_of_holdouts,
            random_state=random_state,
            enable_cache=enable_cache,
            # We need this second layer of cache handled separately as 
            # the different SLURM nodes will try to write simultaneously 
            # on the same cache files. We could add as additional cache seeds
            # also the SLURM node ids and avoid this issue, but then the cache
            # would only be valid for that specific cluster and it would
            # not be possible to reuse it in other settings such as during
            # a reproduction using cache on a notebook.
            enable_top_layer_cache=enable_cache and number_of_slurm_nodes is None,
            precompute_constant_stocastic_features=precompute_constant_stocastic_features,
            smoke_test=smoke_test,
            number_of_slurm_nodes=number_of_slurm_nodes,
            slurm_node_id_variable=slurm_node_id_variable,
            **evaluation_kwargs
        )
        for graph in iterate_graphs(
            graphs,
            repositories,
            versions,
            graph_callback=graph_callback
        )
    ])

    