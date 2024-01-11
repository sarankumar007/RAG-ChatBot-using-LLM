from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from langchain.vectorstores.pinecone import Pinecone
import  pinecone

index_name = "pgrkam"

os.environ["OPENAI_API_KEY"]=""
# initialize pinecone
pinecone.init(
    api_key=" ",
    environment=" "
)


# if you already have an index, you can load it like this
docsearch = Pinecone.from_existing_index(index_name,OpenAIEmbeddings())
llm=ChatOpenAI(temperature=0.9,model_name='gpt-3.5-turbo')

qa_with_sources = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())
system_role = "Friendly AI assistant for PGRKAM Website and try to give as much as information possible and by analyzing and detecting language of the query respond to the query using the detetcted language precise , example if the detetcted language is in hindi respond in hindi words, if the detetcted language is in english respond in english words and similarly make it for all languages."
def ask_question_with_sources(query):
    try:
        result = qa_with_sources(f"{system_role}: {query}")['result']
        return result
    except Exception :
        return "Looks like our code is doing yoga, taking a deep breath. Join in and try again in a few seconds!"


