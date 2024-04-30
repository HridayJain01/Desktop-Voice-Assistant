import pyttsx3
import requests
import streamlit as st
import speech_recognition as sr
import os
import webbrowser
import datetime

from bs4 import BeautifulSoup
from googlesearch import search
from youtube_search import YoutubeSearch
from GoogleNews import GoogleNews
import subprocess


def google_search(query):
    # Perform Google search and retrieve search results
    search_results = search(query, num_results=5)
    st.write("Search Results:")
    for i, result in enumerate(search_results, start=1):
        st.write(f"{i}. {result}")


def extract_snippet(url):
    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the <meta name="description"> tag
        description_tag = soup.find('meta', attrs={'name': 'description'})
        if description_tag:
            # Extract the content attribute of the tag
            snippet = description_tag.get('content')
            return snippet
        else:
            return "Snippet not found on the page."
    else:
        return "Failed to fetch page content."


def google_search_with_snippet(query, num_results=1):
    # Perform a Google search and retrieve search results
    search_results = search(query, num_results=num_results)

    # Print the search results along with snippets
    for i, result in enumerate(search_results, start=1):
        snippet = extract_snippet(result)
        snippettxt = f"{snippet}"

        print(f"{snippet}\n")
        say(snippettxt)


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


def make_transparent(window, alpha):
    # Set the transparency level
    window.attributes("-alpha", alpha)


# Function to speak out text
def say(text):
    os.system(f"say {text}")


def reply(text):
    response_label = st.empty()
    response_label.write(f"Jarvis: {text}")
    say(text)


# Function to recognize voice commands
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


# Function to handle voice commands
def handle_voice_command():
    global subprocess
    query = takeCommand()
    response_label = st.empty()  # Empty placeholder for displaying response

    # Display user command in chat interface

    sites = [["youtube", "https://youtube.com"],
             ["wikipedia", "https://wikipedia.org"],
             ["google", "https://google.com"],
             ["chat", "https://chat.openai.com"]]

    for site in sites:
        if f"open {site[0]}".lower() in query:
            reply(f"Opening {site[0]} Sir...")
            webbrowser.open(site[1])
    if "play" in query:
        if "youtube" in query:
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

    if "tell me" in query:
        deletethese = ["tell me "]
        queryedit = searchedit(query, deletethese)
        google_search_with_snippet(queryedit)

    if "what is" in query:
        deletethese = ["what is "]

        query = query.replace(" + ", " plus ")
        st.write(query)

        queryedit = searchedit(query, deletethese)
        webbrowser.open("https://google.com/search?q=" + queryedit)

    if "play music" in query:
        reply("Playing Music...")
        musicPath = "/Users/hridayjain/Desktop/python/music/Unstoppable(Mr-Jatt1.com).mp3"
        import subprocess, sys

        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, musicPath])

        # add more songs to it
    applications = [
        {"name": "Facetime", "path": "/System/Applications/FaceTime.app"},
        {"name": "PyCharm", "path": "/Applications/PyCharm.app"},
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

    if "the time" in query:
        strfTime = datetime.datetime.now().strftime("%H:%M:%S")
        reply(strfTime)


    if "take my photo" in query:
        reply("Opening Photo Booth")
        os.system(f"open /System/Applications/Photo\ Booth.app")

    if "thank" in query:
        reply("Welcome and bye sir")
        quit()


    if "who is the best" in query:
        reply("Alps")


    if "news" in query:
        googlenews = GoogleNews()
        googlenews.get_news('Today news')
        googlenews.result()
        a = googlenews.gettext()
        first_five = a[:5]
        my_string = '\n'.join(first_five)
        response_label.write(first_five)
        say(my_string)

    if "send an email" in query:
        reply("Opening Jarvis Quick Send")
        email_script = 'emailq.py'
        subprocess.Popen(['python', email_script])

    if "hello" in query:
        reply("Hello Sir")


# Main function to create the Streamlit GUI
def main():
    st.markdown("""
        <h1 style='font-size: 64px; color: #3366ff;text-align: center;'>Voice Desktop Assistant</h1>
    """, unsafe_allow_html=True)
    with st.container() as chat_container:
        # Chat Interface
        st.write("Chat Interface:")
    previous_commands = []

    voice_command_checked = st.checkbox("Voice Command")
    while voice_command_checked:
        handle_voice_command()

    search_query = st.text_input("Enter your search query:")

    if st.button("Search"):
        if search_query:
            google_search(search_query)




if __name__ == "__main__":
    main()