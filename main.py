import speech_recognition as sr # now we can access the speech recognition by typing sr rather than its full name
import webbrowser # this will be used to open web browser when we will say so (it is an in-built module)
import pyttsx3 # this will help for text to speech
import musicLibrary# this is our library which contains a dictionary of music and their links
import requests #this will allow us to use our newsapi key
import requests# this is for the working of aiprocess function
import json# this is for the working of aiprocess function




recognizer = sr.Recognizer() # We are making an object of the class Recognizer named as recognizer which will help JARVIS to recognize our voice
engine = pyttsx3.init() #this will initialize pyttsx engine
newsAPi = your api key #This is my api key from the newsapi website to get the latest news

def processComand(c):
    if "open google" in c.lower():# .lower function will convert our command to lowercase
        webbrowser.open("https://google.com") #this command will open google website in the web browser
    
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com") 
    
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com") 
    
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com") 
    
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1] #This part of the program will break our command which starts with play using " " and split it in 2 words:- for example: "play"" ""skyfall" and here play is on the index 0 of the list and skyfall is on the index 1 of the list so it will choose skyfall 
        link = musicLibrary.music[song]# now we are choosing the 'music' dictionary from the musicLibrary file and finding the link associated with the key song and storing it in the variable 
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey=1a5ffeecb470438eb3f77eaa4cca2886")# this will the latest headlines for us
        data = r.json()

        # Extract the headlines
        if data["status"] == "ok":  # Check if the request was successful
            articles = data["articles"]
            
            # Loop through the articles and print the titles
            for article in articles:
                speak(article["title"])

    else:
        #let openAI handle the request
        output = aiprocess(c)#this will give what we speak as an input to the aiprocess function
        speak(output) #this function will allow jarvis to speak the output 
    

def aiprocess(command): #This function will handle any requests or questions by sending it to gemini
        # Your API key
    API_KEY = your api key

    # URL for the Gemini API
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}'

    # Payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": command
                    }
                ]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json'
    }

    # Sending the request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response
        data = response.json()
        
        # Extract and print the content before the breakdown
        content = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No content found.")
        
        # Split the content based on "Here's a breakdown:"
        part_before_breakdown = content.split("Here's a breakdown:")[0]
        
        # Print the result
        return part_before_breakdown
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}, Error: {response.text}")



def speak(text):# this function will recieve the text and speak it
    engine.say(text) #this is taken from the pyttsx documentation on website
    engine.runAndWait() #this is necessary(idk why?)

if __name__ == "__main__":
    speak("Initializing Jarvis......") # we are calling the speak function and giving it the text input
    while True: #This will help us to always listen for the wake word jarvis
        # Listen for the wake word jarvis
        # obtain audio from the microphone
        r = sr.Recognizer()
        # recognize speech using Google 

        try:
            with sr.Microphone() as source: 
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1) #timeout is the function which allows the program to determine how long the program will be listening 
                # phrase_time_limit sets the time limit of how lonfg the user can pause befor giving a command
                print("Recognizing....") #to print this message during the wait time
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):# this will be our wakeup word 
                speak("Ya") # whent the program hears the wakeup word it will respond with this
                with sr.Microphone() as source: 
                    print("Jarvis Active....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio) #Now command will store whatever we speak

                    processComand(command) #This function will process our command

            command = r.recognize_google(audio) #we use google for better accuracy 
            print(command) #this will print whatever the system is listening
        except Exception as e:
            print("Error; {0}".format(e))
