from personal_ai.llm import generate_response
from personal_ai.graph import run_graph


def main() -> None:
	request = input("You: ")
	
	response = run_graph(request)
	#response = generate_response("Explain in one sentence what a local LLM is.")
	
	print("\nPersonal AI: ")
	print(response)


if __name__ == "__main__":
    main()
