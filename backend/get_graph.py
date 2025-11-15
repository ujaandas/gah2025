import os
import sys
import inspect
import importlib.util


def get_graph():
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
    print(mod.A.hi())
