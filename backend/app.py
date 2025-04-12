from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils.loader import load_code_files
from utils.embedder import get_embeddings
from utils.retriever import Retriever
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage


load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load and embed codebase
code_documents = load_code_files('../../minterprise')
code_embeddings = get_embeddings(code_documents)
retriever = Retriever(code_embeddings, code_documents)

# Initialize Groq LLM
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

class Query(BaseModel):
    question: str

@app.post("/query")
async def query_codebase(query: Query):
    query_embedding = get_embeddings([query.question])[0]
    relevant_docs = retriever.retrieve(query_embedding)
    context = "\n\n".join(relevant_docs)
    prompt = f"Context:\n{context}\n\nQuestion: {query.question}"
    response = llm.invoke([HumanMessage(content=prompt)])

    return {"answer": response}
