from langchain.chat_models import ChatOpenAI
from langchain_core.vectorstores import Chroma
from langchain.chains import RetrievalQA

db = Chroma(persist_directory="my_chroma_db", embedding_function=OpenAIEmbeddings())
llm = ChatOpenAI(model_name="gpt-4")
qa = RetrievalQA(llm=llm, retriever=db.as_retriever())


def answer(question: str):
    return qa.run(question)


print(answer("شرح موضوع X چیست؟"))
