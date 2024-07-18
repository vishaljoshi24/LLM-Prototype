import chainlit as cl
from llama2local import qa_bot
from pyngrok import ngrok

# Start ngrok tunnel
#http_tunnel = ngrok.connect(8000)  # Chainlit app runs on port 8000 by default
#print(f"ngrok tunnel \"{http_tunnel.public_url}\" -> \"http://127.0.0.1:8000\"")

# output function
def final_result(query):
    qa_result = qa_bot()
    response = qa_result({"query": query})
    return response


# chainlit code
@cl.on_chat_start
async def start():
    chain = qa_bot()
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to the DnD Chatbot. What is your query?"
    await msg.update()

    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.ainvoke(message.content, callbacks=[cb])
    answer = res["result"]
    # sources = res["source_documents"]

    # if sources:
    #    answer += f"\nSources:" + str(sources)
    # else:
    #    answer += "\nNo sources found"

    await cl.Message(content=answer).send()
