from langgraph.graph import StateGraph, START, END
from get_graph import get_graph

graph = StateGraph(dict)


def step1(state):
    return {"foo": "bar"}


def step2(state):
    return {"baz": state["foo"]}


# add nodes
graph.add_node("step1", step1)
graph.add_node("step2", step2)

# simple linear graph
graph.add_edge(START, "step1")  # START -> step1
graph.add_edge("step1", "step2")  # step1 -> step2
graph.add_edge("step2", END)  # step2 -> END


def build():
    sg = graph.compile()
    get_graph(sg)  # this CANNOT be raw, ie; like the code above, in "script" form


if __name__ == "__main__":
    build()
