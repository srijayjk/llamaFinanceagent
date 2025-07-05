from langgraph.graph import StateGraph
from langgraph_pipeline import node_functions as fn

def build_graph():
    builder = StateGraph()

    builder.add_node("Forecast", fn.forecast_node)
    builder.add_node("Sentiment", fn.sentiment_node)
    builder.add_node("LLMExplain", fn.llm_node)

    builder.set_entry_point("Forecast")
    builder.add_edge("Forecast", "Sentiment")
    builder.add_edge("Sentiment", "LLMExplain")
    builder.set_finish_point("LLMExplain")

    return builder.compile()


graph = build_graph()