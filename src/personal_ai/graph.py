from typing import Literal
from personal_ai.state import AgentState
from personal_ai.llm import generate_response
from langgraph.graph import StateGraph, START, END

def receive_query(state: AgentState) -> AgentState : #input and output type of AgentState
	print(f"User request: {state['user_request']}")
	return state
	
def generate_reply(state: AgentState) -> AgentState:
	response = generate_response(state["user_request"])
	return {**state, "response": response}
	
def route_request(state: AgentState) -> Literal["general", "calculation"]:
	request = state["user_request"].lower()
	
	if "calculate" in request or "compute" in request or "calculation" in request:
		request_type = "calculation"
	else:
		request_type = "general"
		
	print(f"\nRequest type: {request_type} routing...")
	
	return request_type
	
def build_graph():
	graph = StateGraph(AgentState)
	
	graph.add_node("receive_query", receive_query)
	#graph.add_node("understand_request", understand_request)
	graph.add_node("generate_reply", generate_reply)
	
	graph.add_edge(START, "receive_query")
	#graph.add_edge("receive_query", "generate_reply")
	#graph.add_edge("receive_query", "understand_request")
	
	graph.add_conditional_edges("receive_query", route_request, {"general": "generate_reply", "calculation": "generate_reply"})
	
	graph.add_edge("generate_reply", END)
	
	return graph.compile()
	
def run_graph(user_request: str) -> str:
	graph = build_graph()
	
	initial_state: AgentState = { "user_request": user_request, "response":""}
	
	final_state = graph.invoke(initial_state)
	
	return final_state["response"]
	
	
