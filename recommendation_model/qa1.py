from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from langchain.vectorstores.pinecone import Pinecone
import  pinecone
import pymongo

from recommendation_model.yt_recommendation import video_keywords

index_name = "recommendation"

os.environ["OPENAI_API_KEY"]=""
# initialize pinecone
pinecone.init(
    api_key="",
    environment=""
)
client = pymongo.MongoClient("")
db = client.pgrkam
collection = db.register
# if you already have an index, you can load it like this
docsearch = Pinecone.from_existing_index(index_name,OpenAIEmbeddings())
llm=ChatOpenAI(temperature=0.9,model_name='gpt-3.5-turbo')

qa_with_sources = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever())


def recommend_with_sources(query,useremail):
    keywords_for_courses = ["course", "tutorial", "lecture", "educational", "learning", "study", "training"]
    skills=''
    chat_history_documents = collection.find({'email': useremail},
                                             {'Education Qualification': 1, 'courses': 1, 'domain': 1, 'skills': 1,
                                              'chatHistory': 1})

    history = ''
    userPreference = ''
    # Iterate over each document and print the "chatHistory" field value
    for document in chat_history_documents:
        chat_history = document.get("chatHistory")
        if chat_history is not None:
            history += f"Chat History: {chat_history}"
        # Add a separator line between documents
        history += ("\n---\n")
        userPreference += document.get("Education Qualification", " ") + " "
        userPreference += document.get("courses", " ") + " "
        userPreference += document.get("domain", " ") + " "
        userPreference += document.get("skills", " ") + " "
        skills=document.get("skills")
    print(history)
    print(userPreference)
    print(skills)
    system_role = "Friendly AI assistant for PGRKAM Website and you are given with the job posts details as contexts , provide job recommendation using following chat history ," + history + " and user preference " + userPreference + " of the user.If any job doesn't match say your skillset doesn't match any jobs in the website.By analyzing and detecting language of the query respond to the query using the detetcted language precise and crisp example if the detetcted language is in hindi respond in hindi words, if the detetcted language is in english respond in english words and similarly make it for all languages."
    try:
        if any(keyword in query.lower() for keyword in keywords_for_courses):
            return video_keywords(skills)
        result = qa_with_sources(f"{system_role}: {query}")['result']
        return result
    except Exception as e:
         return str(e)

