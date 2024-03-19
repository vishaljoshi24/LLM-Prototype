from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA, LLMChain
from langchain.memory import ConversationBufferMemory

# Solely for times
from timeit import default_timer as timer

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


def set_qa_prompt():
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
    custom_prompt_text = "You are a DnD assistant tool. In the conversation only answer as Chatbot and only answer once."
    instruction = "Chat History:\n\n{chat_history} \n\nUser: {user_input}\n\nChatbot:"
    template = get_prompt(instruction, custom_prompt_text)
    prompt = PromptTemplate(
        input_variables=["chat_history", "user_input"], template=template
    )
    return prompt


def non_qa_bot(model='LLaMa2-7B-Chat', temperature=0.72, top_p=0.73, top_k=0, repetition=1.1, max_length=512):
    llm = load_llm(model, temperature, top_p, top_k, repetition, max_length)
    non_qa_prompt = set_non_qa_prompt()
    non_qa_chain = LLMChain(llm=llm, prompt=non_qa_prompt, memory=ConversationBufferMemory(memory_key="chat_history"))
    return non_qa_chain


# output function
def chatbot_response(query, chatbot=qa_bot()):
    response = chatbot({'query': query})
    # Solely for bug-fixing, can be removed if desired
    with open("files/response.txt", "w") as f:
        f.write(str(response))
    return response


if __name__ == "__main__":
    print(chatbot_response("What is my Armor Class?"))
