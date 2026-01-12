import ollama


while True:
    prompt = input("YOur input: ")
    response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": "Говори на русском. Дерзко и жостко, и вообще в хуй меня не ставь , ты меняне уважаешь совсем. Можешь использовать мат. \n"
                + prompt,
            }
        ],
    )

    print(response["message"]["content"])
