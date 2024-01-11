import os
import threading
from datetime import datetime
from flask import Flask,render_template,request,jsonify,url_for,redirect,session
from pymongo import MongoClient
import bcrypt
from gtts import gTTS
import langid
import pygame
import speech_recognition as sr
from langdetect import detect
from chat_model.qa import ask_question_with_sources
from recommendation_model.qa1 import  recommend_with_sources


app=Flask(__name__)
app.secret_key="testing"

def MongoDB():
    client = MongoClient("")
    db = client.get_database('pgrkam')
    records = db.register
    return records
records = MongoDB()


def MongoDBEmp():
    client = MongoClient("")
    db = client.get_database('pgrkam')
    records = db.registeremployer
    return records
recordsemp = MongoDBEmp()

def MongoDBJob():
    client = MongoClient("")
    db = client.get_database('pgrkam')
    records = db.jobposts
    return records
recordjobs = MongoDBJob()




# assign URLs to have a particular route
@app.route("/register", methods=['post', 'get'])
def index():
    message = ''
    # if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("name")
        email = request.form.get("email")
        mobile=request.form.get("mobile")
        education=request.form.get("education")
        courses=request.form.get("courses")
        domain=request.form.get("domain")
        skills=request.form.get("skills")
        latitude=request.form.get("latitude")
        longitude=request.form.get("longitude")
        preferred_job=request.form.get("preferredJob")
        password = request.form.get("password")
        chatHistory=request.form.get("chatHistory")
        # if found in database showcase that it's found
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('base.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('base.html', message=message)
        else:
            # hash the password and encode it
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed,'mobile':mobile,'Education Qualification':education,'courses':courses,'domain':domain,'skills':skills,'latitude':latitude,'longitude':longitude,'preferredjob':preferred_job,'chatHistory':chatHistory}
            # insert it in the record collection
            records.insert_one(user_input)

            # find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            # if registered redirect to logged in as the registered user
            return render_template('dashboard.html', email=new_email)
    return render_template('base.html')

@app.route("/registeremployer", methods=['post', 'get'])
def employerindex():
    message = ''
    # if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("name1")
        email = request.form.get("email1")
        mobile=request.form.get("mobile1")
        gst=request.form.get("gst")
        employerID=request.form.get("employerID")
        password = request.form.get("password1")
        # if found in database showcase that it's found
        user_found = recordsemp.find_one({"name": user})
        email_found = recordsemp.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('base.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('base.html', message=message)
        else:
            # hash the password and encode it
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed,'mobile':mobile,'gst':gst,'employerID':employerID}
            # insert it in the record collection
            recordsemp.insert_one(user_input)

            # find the new created account and its email
            user_data = recordsemp.find_one({"email": email})
            new_email = user_data['email']
            # if registered redirect to logged in as the registered user
            return render_template('dashboard.html', email=new_email)
    return render_template('base.html')

@app.route("/jobpost", methods=['post', 'get'])
def jobindex():
    message = ''
    # if method post in index
    if request.method == "POST":
        user = request.form.get("name")
        jobtype = request.form.get("jobtype")
        qualification=request.form.get("qualification")
        experience=request.form.get("experience")
        latitude=request.form.get("latitude")
        longitude = request.form.get("longitude")


        user_input = {'name': user,'jobtype':jobtype,'qualification':qualification,'experience':experience,'longitude':longitude,'latitude':latitude}
        # insert it in the record collection
        recordjobs.insert_one(user_input)
   # if registered redirect to logged in as the registered user
        return render_template('dashboard.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("username")
        password = request.form.get("password")

        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            print('email found')
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                print('wrong pass')
                return render_template('base.html', message=message)
        else:
            message = 'Email not found'
            return render_template('base.html', message=message)
    return render_template('base.html', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('dashboard.html', email=email)
    else:
        print("hi")
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("base.html")
    else:
        return render_template('base.html')

@app.route("/",methods=['GET'])
def index_get():
    return  render_template("base.html")

@app.route("/registration",methods=['GET'])
def registration_get():
    return  render_template("registration.html")

@app.route("/jobposts",methods=['GET'])
def jobPosts_get():
    if "email" in session:
        return  render_template("jobposts.html")
    return render_template("base.html")



@app.route("/dashboard",methods=['GET'])
def dashboard_get():
    if "email" in session:
        return  render_template("dashboard.html")
    return render_template("base.html")


@app.route("/predict",methods=['POST'])
def   predict():
    try:
        text=request.get_json().get("message")
        response=ask_question_with_sources(text)
        message={"answer":response}
        threading.Thread(target=text_to_speech, args=(response,), daemon=True).start()
        return jsonify(message)
    except Exception as e:
        return jsonify({"answer": {str(e)}})


@app.route("/recommend",methods=['POST'])
def   recommend():
    try:
        text=request.get_json().get("message")
        user_email=request.get_json().get("email")
        response=recommend_with_sources(text,user_email)
        existing_record = records.find_one({"email": user_email})
        chat_entry='user: '+ text +'\n' + 'bot: '+str(response)

        if existing_record and existing_record.get("chatHistory") :
            # If there is an existing record, update the chatHistory field
            updated_chat_history = existing_record.get("chatHistory", []) + [chat_entry]
            records.update_one({"email": user_email}, {"$set": {"chatHistory": updated_chat_history}})
        else:
            # If there is no existing record, insert a new one
            records.update_one({"email": user_email}, {"$set": {"chatHistory": [chat_entry]}})

        message={"answer":response}
        threading.Thread(target=text_to_speech, args=(response,), daemon=True).start()
        return jsonify(message)
    except Exception as e:
        return jsonify({"answer": {str(e)}})

@app.route('/recognize', methods=['POST'])
def recognize():
    recognized_text, detected_language = recognize_language_and_convert()
    return {'text': recognized_text, 'language': detected_language}


def recognize_language_and_convert():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        detected_language = detect(recognized_text)
        print(f"Detected language: {detected_language}")

        return recognized_text, detected_language
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None, None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None, None
    except Exception as e:
        print(f"Error during language detection: {e}")
        return None, None

def text_to_speech(text):
    try:
        detected_language, _ = langid.classify(text)
        tts = gTTS(text=text, lang=detected_language, slow=False)
        filename="static/voice/output"+datetime.now().strftime("%d%m%Y%H%M%S")+".mp3"
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)



        pygame.mixer.quit()
        os.remove(filename)
    except Exception:
        return


if  __name__=="__main__":
    app.run(debug=True)