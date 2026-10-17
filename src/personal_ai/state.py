from typing import TypedDict

class AgentState(TypedDict):
	user_request: str
	request_type: str
	response: str
