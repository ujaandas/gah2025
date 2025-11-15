from langgraph.graph.state import CompiledStateGraph
from graph_helper import LangGraphCtxHelper


def build_callable_graph(compiled_graph: CompiledStateGraph) -> None:
    helper = LangGraphCtxHelper(compiled_graph)
    print(helper.module.step1({}))
    # print(helper.lc_graph)
    # graph = CallableGraph(helper.lc_graph)
    # print(f"{graph.to_dict()}\n\n")
    # print(graph.nodes)
    # print(graph.edges)
