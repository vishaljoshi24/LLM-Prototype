from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA

DB_FAISS_PATH = '../vectorstore/db_faiss'


def load_llm(model, temperature, top_p, top_k, repetition, max_length):
    if model == 'LLaMa2-7B-Chat':
        model = "TheBloke/Llama-2-7B-Chat-GGUF"
    elif model == 'LLaMa2-13B-Chat':
        model = "TheBloke/Llama-2-13B-Chat-GGUF"
    else:
        return 'Error with model selection'
    # Load the locally downloaded model here
    # Documentation for parameters https://github.com/marella/ctransformers#config
    llm = CTransformers(
        model=model,
        model_type="llama",
        max_new_tokens=max_length,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        repetition_penalty=repetition
    )
    return llm


def set_custom_prompt():
    custom_prompt_text = """
    [INST] <<SYS>>
    You are a DnD assistant tool, and answer questions provided to you by User. 
    Your role is Chatbot.
    <</SYS>>
    Current conversation: 
    {chat_history}
    Chatbot: 
    """
    prompt = PromptTemplate(template=custom_prompt_text,
                            input_variables=['chat_history'])
    return prompt


def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type='stuff',
                                           retriever=db.as_retriever(search_kwargs={'k': 2}),
                                           return_source_documents=True,
                                           chain_type_kwargs={'prompt': prompt}
                                           )
    return qa_chain


def qa_bot(model='LLaMa2-7B-Chat', temperature=0.72, top_p=0.73, top_k=0, repetition=1.1, max_length=512):
    print("embeddings")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("db")
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    print("llm")
    llm = load_llm(model, temperature, top_p, top_k, repetition, max_length)
    print("prompt")
    qa_prompt = set_custom_prompt()
    print("qa chain")
    qa_chain = retrieval_qa_chain(llm, qa_prompt, db)
    return qa_chain


# output function
def final_result(query):
    qa_result = qa_bot()
    response = qa_result({'query': query})
    return response


if __name__ == "__main__":
    final_result("User: What is my Armor Class?")
