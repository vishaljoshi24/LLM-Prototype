from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from huggingface_hub import login
import os
import glob

DATA_PATH = "../tabletopresources/"
DB_FAISS_PATH = "../vectorstore/db_faiss"

def get_all_pdf_files(directory):
    return [y for x in os.walk(directory) for y in glob.glob(os.path.join(x[0], '*.pdf'))]

# Create vector database
def create_vector_db():
    login(token="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", add_to_git_credential=True)

    # Get all PDF files from the directory and its subdirectories
    pdf_files = get_all_pdf_files(DATA_PATH)
    print(f"Found {len(pdf_files)} PDF files")

    # Load documents
    documents = []
    for pdf_file in pdf_files:
        loader = PyPDFLoader(pdf_file)
        documents.extend(loader.load())
    print(f"Loaded {len(documents)} documents")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"Created {len(texts)} text chunks")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'mps'}
    )

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    create_vector_db()
