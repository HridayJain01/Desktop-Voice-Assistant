sqlu = "root"
sqlp = "password"
import pyttsx3
import requests
import streamlit as st
import speech_recognition as sr
import os
import webbrowser
import datetime
import mysql.connector
import time
import random
import urllib.parse

from bs4 import BeautifulSoup
from googlesearch import search
from youtube_search import YoutubeSearch
from GoogleNews import GoogleNews
import subprocess


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=sqlu,
            password=sqlp,
            database="queries"
        )
        print("Connected to database")
        return connection
    except mysql.connector.Error as e:
        print("Error connecting to database:", e)
        return None


def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                query_number INT AUTO_INCREMENT PRIMARY KEY,
                query_text varchar(200)
            )
        """)
        print("Table 'queries' created successfully")
        cursor.close()
    except mysql.connector.Error as e:
        print("Error creating table:", e)


def create_todo(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todo (
                task_number INT AUTO_INCREMENT PRIMARY KEY,
                task_text varchar(200)
            )
        """)
        print("Table 'todo' created successfully")
        cursor.close()
    except mysql.connector.Error as e:
        print("Error creating table:", e)



def insert_query(connection, query_text):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO queries (query_text) VALUES (%s)
        """, (query_text,))
        connection.commit()
        print("Query inserted successfully")
        cursor.close()
    except mysql.connector.Error as e:
        print("Error inserting query:", e)


def insert_todo(connection, query_text):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO todo(task_text) VALUES (%s)
        """, (query_text,))
        connection.commit()
        print("task inserted successfully")
        cursor.close()
    except mysql.connector.Error as e:
        print("Error inserting task:", e)


def delete_query_history(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            TRUNCATE queries
        """)
        connection.commit()
        print("Query inserted successfully")
        cursor.close()
    except mysql.connector.Error as e:
        print("Error inserting query:", e)


def delete_task(connection, text):
    try:
        cursor = connection.cursor()
        stringe = f"DELETE FROM todo WHERE task_text LIKE '{text}';"
        cursor.execute(stringe)
        queries = cursor.fetchall()
        cursor.close()
        return queries
    except mysql.connector.Error as e:
        print("Error retrieving queries:", e)
        return None


# Function to retrieve all queries from the table
def retrieve_todo(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM todo")
        queries = cursor.fetchall()
        cursor.close()
        return queries
    except mysql.connector.Error as e:
        print("Error retrieving queries:", e)
        return None



def retrieve_bottom_10_queries(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT query_text FROM (SELECT * FROM queries ORDER BY query_number DESC LIMIT 10) AS bottom_10 ORDER BY query_number ASC")
        queries = cursor.fetchall()
        cursor.close()
        return queries
    except mysql.connector.Error as e:
        print("Error retrieving bottom 10 queries:", e)
        return None


def google_search(query):

    search_results = search(query, num_results=5)
    st.write("Search Results:")
    for i, result in enumerate(search_results, start=1):
        st.write(f"{i}. {result}")


def searchedit(text, keywords):
    text = text.replace(" ", "+")

    for keyword in keywords:
        text = text.replace(keyword, "", 1)

    return text


def ssearchedit(text, keywords):
    text = text.replace(" ", "+")
    for keyword in keywords:
        text = text.replace(keyword, "", 1)
    text = text.replace("+", " ")

    return text

def say(text):
    os.system(f"say {text}")


def reply(text):
    response_label = st.empty()
    response_label.write(f"Jarvis: {text}")
    say(text)



def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            st.write(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand what you said.")
            return "Some Error Occurred. Sorry from Jarvis"
        except sr.RequestError as e:
            st.error(f"Error with the speech recognition service; {e}")
            return "Some Error Occurred. Sorry from Jarvis"


def send_whatsapp_message(pnumber, message):

    encoded_message = urllib.parse.quote(message)
    webbrowser.open("https://wa.me/" + pnumber + "?text=" + encoded_message)

def handle_voice_command(logdat):
    global subprocess
    query = takeCommand()
    if query != "Some Error Occurred. Sorry from Jarvis":
        insert_query(logdat, query)
    response_label = st.empty()

    sites = [
        ["youtube", "https://youtube.com"],
        ["wikipedia", "https://wikipedia.org"],
        ["google", "https://google.com"],
        ["chat", "https://chat.openai.com"],
        ["facebook", "https://facebook.com"],
        ["twitter", "https://twitter.com"],
        ["amazon", "https://amazon.com"],
        ["reddit", "https://reddit.com"],
        ["stackoverflow", "https://stackoverflow.com"],
        ["instagram", "https://instagram.com"],
        ["linkedin", "https://linkedin.com"],
        ["github", "https://github.com"],
        ["netflix", "https://netflix.com"],
        ["apple", "https://apple.com"],
        ["spotify", "https://spotify.com"],
        ["microsoft", "https://microsoft.com"],
        ["pinterest", "https://pinterest.com"],
        ["dropbox", "https://dropbox.com"], ]
    for site in sites:
        if f"open {site[0]}".lower() in query:
            reply(f"Opening {site[0]} Sir...")
            webbrowser.open(site[1])


    if "play" in query:
        deletethese = ["on+youtube+for", "on+youtube", "youtube+for", "play", "youtube"]
        queryedit = searchedit(query, deletethese)
        sayquery = ssearchedit(query, deletethese)
        results = YoutubeSearch(queryedit, max_results=1).to_dict()
        if results:
            top_result = results[0]
            video_url = f"https://www.youtube.com/watch?v={top_result['id']}"
            reply(f"Playing {sayquery}")
            webbrowser.open(video_url)
        else:
            print("No search results found.")
    if "search" in query:
        if "youtube" in query:
            deletethese = ["on+youtube+for", "on+youtube", "youtube+for", "search", "youtube"]
            queryedit = searchedit(query, deletethese)
            sayquery = ssearchedit(query, deletethese)
            reply(f"Searching {sayquery}")
            webbrowser.open("https://www.youtube.com/results?search_query=" + queryedit)
        elif "spotify" in query:
            deletethese = ["on+spotify+for", "on+spotify", "spotify+for", "search", "spotify  "]
            queryedit = searchedit(query, deletethese)
            queryedit = queryedit.replace("+", "%20")
            sayquery = ssearchedit(query, deletethese)
            reply(f"Searching {sayquery}")
            webbrowser.open("https://open.spotify.com/search/" + queryedit)
        else:
            deletethese = ["on+google+for", "on+google", "google+for", "search", "google", "for"]
            queryedit = searchedit(query, deletethese)
            sayquery = ssearchedit(query, deletethese)
            reply(f"Searching {sayquery}")
            webbrowser.open("https://google.com/search?q=" + queryedit)

    if "what is" in query:
        query = query.replace("what is ", "")
        query = query.replace(" + ", " plus ")
        st.write(query)
        deletethese = ["", ""]
        queryedit = searchedit(query, deletethese)
        webbrowser.open("https://google.com/search?q=" + queryedit)

    if "previous queries" in query:
        qlist = retrieve_bottom_10_queries(logdat)
        my_string = ','.join(map(str, qlist))
        response_label.write(qlist)
        say(my_string)

    if "delete" in query:
        if "query history" in query:
            delete_query_history(logdat)

    applications = [
        {"name": "facetime", "path": "/System/Applications/FaceTime.app"},
        {"name": "python", "path": "/Applications/PyCharm.app"},
        {"name": "WhatsApp", "path": "/Applications/WhatsApp.app"},
        {"name": "Word", "path": "/Applications/Microsoft\ Word.app"},
        {"name": "Excel", "path": "/Applications/Microsoft\ Excel.app"},
        {"name": "Photos", "path": "/System/Applications/Photos.app"},
        {"name": "Settings", "path": "/System/Applications/System\ Settings.app"},
        {"name": "Calendar", "path": "/System/Applications/Calendar.app"}
    ]
    for app in applications:
        if f"open {app['name']}".lower() in query:
            reply(f"Opening  {app['name']}")
            os.system(f"open {app['path']}")

    if "time" in query:
        strfTime = datetime.datetime.now().strftime("%H:%M:%S")
        reply(strfTime)

    if "take my photo" in query:
        reply("Opening Photo Booth")
        os.system(f"open /System/Applications/Photo\ Booth.app")

    if "thank you" in query:
        reply("Welcome and bye sir")
        quit()

    if "stop listening" in query:
        reply("Welcome and bye sir")
        quit()


    identity = ["who are you", "what's your name", "what is your name", "what do i call you"]
    for i in identity:
        if i in query:
            reply("Hello I am JARVIS your desktop AI assistant here for all your needs.")

    func = ["what can you do", "what are your functionalities", "what are your features"]
    for j in func:
        if j in query:
            reply(
                "I can do multiple tasks : open websites, tell you the news, play music, create to do lists, open applications, search the internet and many more.")

    if "who is the best" in query:
        reply("Anjali Ma'am")

    if "how are you" in query:
        reply("I'm doing well thank you for asking")

    while "to do list" in query:
        st.write("What do you want to do in to do list: a)View b)Add c)Remove d)exit")
        todo = takeCommand()
        while "add" in todo:
            st.write("Enter the content:")
            message = takeCommand()
            if message != "Some Error Occurred. Sorry from Jarvis":
                insert_todo(logdat, message)
                break
        if "exit" in todo:
            break
        if "remove" in todo:
            tdl = retrieve_todo(logdat)
            st.write(tdl)
            while "remove" in todo:
                st.write("What do you want to remove")
                pr = takeCommand()
                if pr != "Some Error Occurred. Sorry from Jarvis":
                    delete_task(logdat, pr)
                    break
        if "view" in todo:
            tdl = retrieve_todo(logdat)
            st.write(tdl)

    if "news" in query:
        googlenews = GoogleNews()
        googlenews.get_news('Today news')
        googlenews.result()
        a = googlenews.gettext()
        first_five = a[:5]
        my_string = '\n'.join(first_five)
        response_label.write(first_five)
        say(my_string)

    jokes = (
        "Why was the math book sad? Because it had too many problems.",
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call a fake noodle? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What did one plate say to the other plate? Dinner's on me!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "What did one hat say to the other? Stay here, I'm going on ahead!",
        "What do you call an alligator in a vest? An investigator!",
        "Why did the tomato turn red? Because it saw the salad dressing!",
        "Why couldn't the bicycle stand up by itself? It was two-tired!",
        "What do you get when you cross a snowman and a vampire? Frostbite!",
        "Why don't eggs tell jokes? Because they'd crack each other up!",
        "What do you call a belt made out of watches? A waist of time!",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
        "What's orange and sounds like a parrot? A carrot!",
        "What do you call a fish with no eyes? Fsh!",
        "Why was the broom late? It overswept!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the math book look sad? Because it had too many problems!",
        "How does a penguin build its house? Igloos it together!")

    if "tell me a joke" in query:
        joketotell = random.choice(jokes)
        reply(joketotell)

    fun_facts = (
        "Honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
        "A group of flamingos is called a flamboyance.",
        "The original name for the search engine Google was Backrub.",
        "The average person spends 6 months of their lifetime waiting on a red light to turn green.",
        "Bananas are berries, but strawberries aren't.",
        "Octopuses have three hearts.",
        "The Eiffel Tower can be 15 cm taller during the summer, due to thermal expansion of the iron.",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
        "The Great Wall of China is not visible from space with the naked eye.",
        "The world's largest desert is Antarctica.",
        "The human nose can remember 50,000 different scents.",
        "There are more possible iterations of a game of chess than there are atoms in the known universe.",
        "Cows have best friends and can become stressed when they are separated.",
        "The tongue is the only muscle in the human body that is attached at only one end.",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
        "There are more airplanes in the ocean than submarines in the sky.",
        "A single cloud can weigh more than 1 million pounds.",
        "Banging your head against a wall burns 150 calories an hour.",
        "Bananas are berries, but strawberries aren't.")
    if "tell me" in query:
        if "fact" in query:
            random_fact = random.choice(fun_facts)
            reply(random_fact)

    if "send an email" in query:
        reply("Opening Jarvis Quick Send")
        email_script = 'emailq.py'
        subprocess.Popen(['python', email_script])

    contactlist = [
        ["gj", "918291692365"],
        ["garv", "918291692365"],
        ["mango", "919867342059"],
        ["tanisha", "919867740496"],
        ["reshma ma'am", "919769381584"],
        ["reshma mam", "919769381584"],
        ["anjali mam", "919869135271"],
        ["anjali ma'am", "919869135271"],
    ]

    if "send" in query:
        if "whatsapp" in query:
            contactfound = False
            for i in contactlist:

                if i[0] in query:
                    contactfound = True
                    while i[0] in query:
                        st.write("What should message content be:")
                        msg = takeCommand()
                        if msg != "Some Error Occurred. Sorry from Jarvis":
                            pnumber = i[1]
                            send_whatsapp_message(pnumber, msg)
                            break
            if contactfound == False:
                st.write("Choose from contact list")
                st.write(contactlist)
                while contactfound == False:
                    ctact = takeCommand()
                    for i in contactlist:
                        if ctact == i[0]:
                            contactfound = True
                            pnumber = i[1]
                            while ctact == i[0]:
                                st.write("What should message content be:")
                                msg = takeCommand()
                                if msg != "Some Error Occurred. Sorry from Jarvis":
                                    send_whatsapp_message(pnumber, msg)
                                    break

    if "hello" in query:
        reply("Hello Sir")


def main():
    logdat = connect_to_database()
    create_table(logdat)
    create_todo(logdat)

    st.markdown("""
        <h1 style='font-size: 64px; color: #3366ff;text-align: center;'>Voice Desktop Assistant</h1>
    """, unsafe_allow_html=True)
    with st.container() as chat_container:

        st.write("Chat Interface:")


    voice_command_checked = st.toggle("Voice Command")
    while voice_command_checked:
        handle_voice_command(logdat)

    search_query = st.text_input("Enter your search query:")

    if st.button("Search"):
        if search_query:
            google_search(search_query)


if __name__ == "__main__":
    main()
