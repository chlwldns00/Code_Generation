
import openai
import os

openai.api_key = "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"
def generate_questions(user_query: str) -> list[str]:
    system_message = '''
    You are given with Postgres table with the following columns.

    city_name, population, country, reviews.

    Your task is to decompose the given question into the following two questions.

    1. Question in natural language that needs to be asked to retrieve results from the table.
    2. Question that needs to be asked on the top of the result from the first question to provide the final answer.

    Example:

    Input:
    How is the culture of countries whose population is more than 5000000

    Output:
    1. Get the reviews of countries whose population is more than 5000000
    2. Provide the culture of countries
    '''

    # 사용자의 질문과 시스템 메시지를 하나의 대화로 구성
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_query},
    ]

    # OpenAI ChatCompletion을 사용하여 답변 생성
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    # 생성된 답변을 반환
    generated_response = response['choices'][0]['message']['content']

    return generated_response



#main

print(generate_questions("give me informations about newjeans"))
print("hello")