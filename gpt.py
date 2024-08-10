import os
import openai
import chainlit as cl
from pyngrok import ngrok

# Load OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

# Define the model and parameters
MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.7
MAX_TOKENS = 150
TOP_P = 0.95
TOP_K = 50

# Function to call OpenAI API
def openai_call(prompt):
    response = openai.Completion.create(
        engine=MODEL,
        prompt=prompt,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

# Define the prompt for QA
def set_qa_prompt(context, question):
    custom_prompt_text = f"""
    You are a DnD assistant tool. Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep answers concise.
    Do not answer questions about specific campaigns.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """
    return custom_prompt_text

# Chainlit code
@cl.on_chat_start
async def start():
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to the DnD Chatbot. What is your query?"
    await msg.update()

@cl.on_message
async def main(message: cl.Message):
    user_query = message.content
    context = ""  # Replace with actual context if needed
    prompt = set_qa_prompt(context, user_query)
    
    # Get response from OpenAI
    answer = openai_call(prompt)
    
    await cl.Message(content=answer).send()

if __name__ == "__main__":
    # Start ngrok tunnel
    http_tunnel = ngrok.connect(8000)  # Chainlit app runs on port 8000 by default
    print(f"ngrok tunnel \"{http_tunnel.public_url}\" -> \"http://127.0.0.1:8000\"")

    # Start Chainlit app
    cl.run()
