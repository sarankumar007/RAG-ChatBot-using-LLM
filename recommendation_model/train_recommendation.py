from langchain.document_loaders import DirectoryLoader
from langchain.llms import OpenAI
import pymongo

import os

from langchain.vectorstores.faiss import FAISS

os.environ["OPENAI_API_KEY"]=""

import pinecone

# initialize pinecone
pinecone.init(
    api_key="",
    environment=""
)

client = pymongo.MongoClient("")
db = client.pgrkam
collection = db.jobposts

# Retrieve all documents from the collection
documents = collection.find()

# Create or open the dataset.txt file in write mode

with open("dataset.txt", "w") as file:
    # Iterate over each document
    for document in documents:
        # Iterate over each field and its value in the document
        for field, value in document.items():
            # Write the field and value to the file
            file.write(f"{field}: {value}\n")
        # Add a separator line between documents
        file.write("\n---\n")
loaders = DirectoryLoader('./', glob='dataset.txt')
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

index_name = "recommendation"


Pinecone.from_documents(docs_chunks, embeddings, index_name=index_name)

# if you already have an index, you can load it like this
#docsearch = Pinecone.from_existing_index(index_name, embeddings)




