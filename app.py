from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA, LLMChain
from langchain.memory import ConversationBufferMemory
from utils import default_model
import streamlit as st

DB_FAISS_PATH = "./vectorstore/db_faiss"


def load_llm(model, temperature, top_p, top_k, repetition, max_length):
    if model == "LLaMa2-7B-Chat":
        model = "TheBloke/Llama-2-7B-Chat-GGUF"
    elif model == "LLaMa2-13B-Chat":
        model = "TheBloke/Llama-2-13B-Chat-GGUF"
    elif model == "TinyLlama-1.1B-Chat":
        model = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
    else:
        return "Error with model selection"
    # Load the locally downloaded model here
    # Documentation for parameters https://github.com/marella/ctransformers#config
    llm = CTransformers(
        model=model,
        model_type="llama",
        config={
            "max_new_tokens": max_length,
            "temperature": temperature,
            "context_length": 2048,
            "top_p": top_p,
            "top_k": top_k,
            "repetition_penalty": repetition,
            "gpu_layers": 20
        },
        
    )
    return llm


def set_qa_prompt():
    custom_prompt_text = """
    You are a DnD assistant tool. Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep answers concise.
    Do not answer questions about specific campaigns.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """
    prompt = PromptTemplate(
        template=custom_prompt_text, input_variables=["context", "question"]
    )
    return prompt


def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return qa_chain


def qa_bot(
    model=default_model.MODEL,
    temperature=default_model.TEMPERATURE,
    top_p=default_model.TOP_P,
    top_k=default_model.TOP_K,
    repetition=default_model.REPETITION,
    max_length=default_model.MAX_LENGTH,
):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
    db = FAISS.load_local(
        DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True
    )
    llm = load_llm(model, temperature, top_p, top_k, repetition, max_length)
    qa_prompt = set_qa_prompt()
    qa_chain = retrieval_qa_chain(llm, qa_prompt, db)
    return qa_chain


def get_prompt(instruction, new_system_prompt):
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
    return prompt_template


def set_non_qa_prompt():
    custom_prompt_text = (
        "You are a DnD assistant tool. Only answer as Chatbot and only answer once."
    )
    instruction = "Chat History:\n\n{chat_history} \n\nUser: {user_input}\n\nChatbot:"
    template = get_prompt(instruction, custom_prompt_text)
    prompt = PromptTemplate(
        input_variables=["chat_history", "user_input"], template=template
    )
    return prompt


def non_qa_bot(
    model=default_model.MODEL,
    temperature=default_model.TEMPERATURE,
    top_p=default_model.TOP_P,
    top_k=default_model.TOP_K,
    repetition=default_model.REPETITION,
    max_length=default_model.MAX_LENGTH,
):
    llm = load_llm(model, temperature, top_p, top_k, repetition, max_length, mod)
    non_qa_prompt = set_non_qa_prompt()
    non_qa_chain = LLMChain(
        llm=llm,
        prompt=non_qa_prompt,
        memory=ConversationBufferMemory(memory_key="chat_history"),
    )
    return non_qa_chain


# output function
def chatbot_response(query, chatbot=qa_bot()):
    return chatbot({"query": query})


if __name__ == "__main__":
    print(chatbot_response("What is my Armor Class?"))




# Streamlit app
st.title("DnD Assistant")

# Load the QA bot
qa_chain = qa_bot()

def chatbot_response(query, chatbot=qa_chain):
    return chatbot({"query": query})

query = st.text_input("Ask your question:")
if st.button("Submit"):
    response = chatbot_response(query)
    st.write(response["result"])