from ollama import chat


def generate_response(prompt: str) -> str:
    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.message.content
