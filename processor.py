from langchain_community.vectorstores import FAISS
from langchain_unstructured import UnstructuredLoader
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.text_splitter import CharacterTextSplitter


def process_file(file_path):
    loader = UnstructuredLoader(file_path)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    return FAISS.from_documents(chunks, embeddings)