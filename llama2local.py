from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA

DB_FAISS_PATH = './vectorstore/db_faiss'


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
        config={
            'max_new_tokens': max_length,
            'temperature': temperature,
            'context_length': 2048,
            'top_p': top_p,
            'top_k': top_k,
            'repetition_penalty': repetition
        }
    )
    return llm


def set_custom_prompt():
    custom_prompt_text = """
    You are a DnD assistant tool. Use the following pieces of information to answer the user's question. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """
    prompt = PromptTemplate(template=custom_prompt_text,
                            input_variables=['context', 'question'])
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
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    llm = load_llm(model, temperature, top_p, top_k, repetition, max_length)
    qa_prompt = set_custom_prompt()
    qa_chain = retrieval_qa_chain(llm, qa_prompt, db)
    return qa_chain


# output function
def chatbot_response(query, chatbot=qa_bot()):
    response = chatbot({'query': query})
    return response


if __name__ == "__main__":
    print(chatbot_response("What is my Armor Class?"))
