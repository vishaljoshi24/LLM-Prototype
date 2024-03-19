from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from huggingface_hub import login

DATA_PATH = '../files/tabletopresources'
DB_FAISS_PATH = '../vectorstore/db_faiss'


# Create vector database
def create_vector_db():
    login(token="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", add_to_git_credential=True)
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    # model_kwargs={'device': 'mps'})

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)


if __name__ == "__main__":
    create_vector_db()
