from langchain.document_loaders import DirectoryLoader
from langchain.llms import OpenAI

import os

from langchain.vectorstores.faiss import FAISS


os.environ["OPENAI_API_KEY"]=""

import pinecone

# initialize pinecone
pinecone.init(
    api_key="",
    environment=""
)

loaders = DirectoryLoader('./', glob='data.txt')
docs = loaders.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap  = 50
)

docs_chunks = text_splitter.split_documents(docs)

from langchain.embeddings.openai import OpenAIEmbeddings
#
embeddings = OpenAIEmbeddings()
# docsearch = FAISS.from_documents(docs_chunks, embeddings)

from langchain.vectorstores import Pinecone

index_name = "pgrkam"


docsearch = Pinecone.from_documents(docs_chunks, embeddings, index_name=index_name)

# if you already have an index, you can load it like this
#docsearch = Pinecone.from_existing_index(index_name, embeddings)




