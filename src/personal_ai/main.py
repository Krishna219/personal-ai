from personal_ai.llm import generate_response


def main() -> None:
    response = generate_response(
        "Explain in one sentence what a local LLM is."
    )

    print(response)


if __name__ == "__main__":
    main()
