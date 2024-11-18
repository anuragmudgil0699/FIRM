import google.generativeai as genai
from openai import OpenAI

from constants import GEMINI_API_KEY, GPT_API_KEY, MODEL


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

client = OpenAI(api_key=GPT_API_KEY)

def GeminiCall(prompt):
    prediction = model.generate_content(prompt)
    return prediction


def ChatGPTCall(prompt):
    # Not complete. Once we decide whether or not to use it for our project
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": prompt
        }
    ]
)
    print(completion.choices[0].message.content)

def call_llm(prompt):
    if MODEL == 'GEMINI':
        return GeminiCall(prompt)
    return ChatGPTCall(prompt)