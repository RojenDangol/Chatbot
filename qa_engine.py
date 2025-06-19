from langchain.chains import RetrievalQA
from langchain_community.llms.ollama import Ollama
from langchain_ollama import OllamaLLM


def get_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever()
    llm = Ollama(model="llama3")
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)