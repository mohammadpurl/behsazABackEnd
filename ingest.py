from dotenv import load_dotenv

load_dotenv()

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import Chroma

loader = PyPDFLoader("documents/mydoc.pdf")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)
emb = OpenAIEmbeddings()
db = Chroma.from_documents(chunks, emb)
db.persist("my_chroma_db")
