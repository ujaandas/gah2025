import os
import sys
import inspect
import importlib.util
from langgraph.graph.state import CompiledStateGraph


def get_graph(compiled_graph: CompiledStateGraph):
    """ """
    stack = inspect.stack()
    ctx = next(ctx for ctx in stack if ctx.filename != __file__)
    fp = ctx.filename
    print(fp)

    mod_name = os.path.basename(fp).removesuffix(".py")

    spec = importlib.util.spec_from_file_location(mod_name, fp)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)

    graph = compiled_graph.get_graph()
    print(type(graph))
    print(graph)
    print(graph.draw_ascii())
    state = {}
    state = mod.step1(state)
    print(mod.step2(state))
