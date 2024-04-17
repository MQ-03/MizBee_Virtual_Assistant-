from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import main, send_mail
from datetime import datetime
import random
import pwinput
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import io
import re
import speech_recognition as sr

# Globel variable for date & time.
date_time = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
#uri and credential for mongoDB connection
uri = "mongodb+srv://mubu3:vpFSyhIjXVVmW7je@mizbee.xhbvmay.mongodb.net/?retryWrites=true&w=majority"

ServerApi.api_key = "vald4rbw3znOY606doQPa3azYXyzwmE2w9X4eFeJ35uZhyrziBOxJhX5n5O2sio3" 

# Create a new client and connect to the server
#myclient = MongoClient(uri, server_api=ServerApi('1'))
local_client = MongoClient("mongodb://localhost:27017/")
#mydb = myclient["MizBee"]
ldb = local_client["mizbee"]

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("MizBee: Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("MizBee: Recognizing...")
        query = recognizer.recognize_google(audio)
        insert_qry(query)
        return query
    except sr.UnknownValueError as uve:
        print("MizBee: Sorry, I did not hear your request. Please try again.")
        return ""
    except sr.RequestError as e:
        print(f"MizBee: Could not request results from Google Speech Recognition service; {e}")
        return ""
    

def validate_mail(mail):
    if re.match(r"[^@]+@[^@]+\.[^@]+", mail):
        return True
    return False
def validate_uname(uname):
    if re.match(r"^[a-zA-Z](_(?!(\.|_))|(?!(_|\.))|[a-zA-Z]){4,6}[a-zA-Z]$", uname):
        return True
    return False
def database():
        # Send a ping to confirm a successful connection
    try:
        #myclient.admin.command('ping')
        local_client.admin.command('ping')
        print("MizBee: Pinged your deployment. You successfully connected to Atlas and Local MongoDB!")
        main.speak(f"Pinged your deployment. You successfully connected to Atlas and Local  MongoDB")
    except Exception as e:
        print(e)
        main.speak(e)

#Fetch the document data's
def fetch_data():

    mydb = local_client["mizbee"]
    print("Please say your collection name")
    main.speak("Please say your collection name")
    col_name = listen()
    mycol = mydb[col_name]

    if mycol == mydb["users"]:
        print("Please say your name")
        main.speak("Please say your name")
        name = listen()
        udata = mycol.find_one({"fname":name})
        if udata:
            fname = udata["fname"]
            lname = udata["lname"]
            dob = udata["dob"]
            place = udata["place"]
            mail = udata["mail_id"]
            phone = udata["phone"]
            result0 = (f"Name: {fname} {lname},\nDate of Birth: {dob},\nPlace: {place},\nPhone Numer: {phone},\nMail Id: {mail}\n")
            image_fetch(fname)
            print(result0)
            main.speak(result0)
        else:
            print("Data not found..!")
    elif mycol == mydb["queries"]:
        for x in mycol.find({},{"_id": 0, "query": 1, "date": 1}):
            query = f"Query: {x['query']}"
            date = f"Date: {x['date']}"
            result1 = (f"{query}, {date}\n")
            print(result1)
            main.speak(result1)
    elif mycol == mydb["gpt"]:
        for x in mycol.find({},{"_id": 0, "response": 1, "date": 1}):
            response = f"GPT Response: {x['response']}"
            date = f"Date: {x['date']}"
            result2 = (f"{response}, {date}\n")
            print(result2)
            main.speak(result2)
    else:
        print("You want to enter manualy.")
        main.speak("You want to enter manualy.")
        resp = listen().lower()
        if resp in ["yes", "s", "Yes"]:
            ask = input("Please enter collection name.")
            return fetch_data(col_name = ask)
        else:
            return fetch_data()

def image_fetch(fname):
    col = ldb["user"]
    image_doc = col.find_one({"fname": fname})

    if image_doc:

        if "no data added" == image_doc["image_data"]:
            print("Image not found in the database")
        else:
            # Get the image data from the document
            image_data = image_doc['image_data']
            # Convert the binary image data to a PIL Image object
            image = Image.open(io.BytesIO(image_data))
            # Display the image
            image.show()
    else:
        print("Image not found in the database")
        main.speak("Image not found in the database")

#Edit the databse document
def edit():

    main.speak("Please select your usermode")

    usrmode = main.listen()

    if usrmode in ["super user", "superuser"]:
   
        mycol = ldb["su_users"]
        main.speak("Please say the Field1 value")
        field0 = main.listen()
        main.speak("Please say the new value for Value1")
        value0 = main.listen()
    
        main.speak("Please say the Field2 value")
        field1 = main.listen()
        main.speak("Please say the new value for Value2")
        value1 = main.listen()

        myquery = { field0 : value0 }
        newvalue = { "$set" : { field1 : value1 }}

        x = mycol.update_one(myquery,newvalue)
        print(x.modified_count,"Document Updated..!")
        main.speak(x.modified_count,"Document Updated..!")
    elif usrmode == "user":
        mycol = ldb["user"]

        main.speak("Please say the Field1 value")
        field0 = main.listen()
        main.speak("Please say the new value for Value1")
        value0 = main.listen()
    
        main.speak("Please say the Field2 value")
        field1 = main.listen()
        main.speak("Please say the new value for Value2")
        value1 = main.listen()

        myquery = { field0 : value0 }
        newvalue = { "$set" : { field1 : value1 }}

        x = mycol.update_one(myquery,newvalue)
        print(x.modified_count,"Document Updated..!")
        main.speak(x.modified_count,"Document Updated..!")

def insert_qry(query):

    col = ldb["queries"]

    date_time = datetime.now().strftime("%d/%m/%Y - %I:%M:%S %p")
    try:
        qry = col.find_one({"query": query})
        dtbase = qry["query"]

        if query == dtbase:
            col.update_one({"query":query},{"$set": {"query":query, "date":date_time}})
    except TypeError as e:
        add = {"query" : query, "date": date_time }
        col.insert_one(add)

def insert_gpt(response, query):

    col = ldb["gpt"]

    date_time = datetime.now().strftime("%d/%m/%Y - %I:%M:%S %p")
    add = {"response" : response, "date": date_time, "query": query }
    col.insert_one(add)

def joke():

    mycol = ldb['jokes']

    joke_documents = mycol.find({}, {"joke": 1})  # Fetch all joke documents
    jokes = [doc['joke'] for doc in joke_documents]  # Extract jokes from documents

    random_joke = random.choice(jokes)
    print(f"MizBee: {random_joke}")
    main.speak(random_joke)

def greet():

    mycol = ldb['greetings']

    greet_documents = mycol.find({}, {"greet": 1})  # Fetch all joke documents
    greets = [doc['greet'] for doc in greet_documents]  # Extract jokes from documents

    random_greet = random.choice(greets) 
    print(f"MizBee: {random_greet}")
    main.speak(random_greet)

def auth():

    # collection define.
    col = ldb["auth_user"]
    su_col = ldb["su_users"]
    print("Please select you user mode.\n\nSuper User or User")
    main.speak("Please select you user mode.\n")
    # User mode selection input
    inpt = listen()
    print(inpt)
    if inpt == "super user": # user selceted super user mode
    # first name from user for search in DB.
        print(main.Fore.RED + "What is your name?")
        main.speak("What is your name?")
        user = listen()
        print(user)
        try:
            su = su_col.find_one({"fname": user}) #get user details from db.
    # super user checking
            if user == su["fname"]: # matching the credentials
                print(f"\nHi {user} Boss! Happy to meet you again.")
                main.speak(f"Hi {user} Boss! Happy to meet you again.")
                return main.ai_assistant() # goto mixbee chat field
            else:
                print("Please type valid username and password.")
                main.speak("Please type valid username and password.")
                return auth() # recalling the auth function again.
        except TypeError as e:
            print(f"Error: {e}. Please type valid Name")
            main.speak(f"Error: {e}. Please type valid Name")
            return auth()
    elif inpt == "user": # if user select normal user
        print(main.Fore.GREEN + "\nPlease say your username.\n")
        main.speak("Please say your username.")
        try:
            uname = listen()
            print(f"You said: {uname}")
            # Find the user by name
            f = col.find_one({ "username": uname })
            # Check if user exists
            if f:
            # Get the user from the result
                fname = f["first_name"]
                lname = f["last_name"]
                if uname == fname:
                    print(f"\nWelcome {fname} {lname} to MizBee's AI world..!")
                    main.speak(f"Welcome {fname} {lname} to MizBee's AI world..!")
                    return main.user_ai()
        # asking to unknow user to join.        
            else:
                main.speak("Sorry! You don't have authorization for access me.")
                main.speak("your not a user! Need to join with us?")
                respns = listen()
                res = ["y", "Y", "yes", "YES"]
                if respns in res:
                    create()
                else:
                    main.speak("GoodBye see you again..!")
                    return auth()
        except TypeError as e:
            print(f"Error: {e}. Please type valid credentials.")
            main.speak(f"Error: {e}. Please type valid credentials.")
            return auth()
    else:
        print("Please Select One of the user mode from the given list..!")
        main.speak("Please Select One of the user mode from the given list..!")
        return auth()

def user_creation():

    col = ldb["user"]

# User Checking    
    uname = listen().islower()
    name = input("First Name: ")
    qry = col.find_one({"uname": uname})
    try:

        if qry :

            if uname == qry["uname"] and name == qry["fname"]:
                ask = input("Username already exist.! Do you want to reset your password? ")
                res = ["y", "Y", "yes", "YES", "Yes"]
                if ask in res:    
                    uname_edit()
            else:
                auth()
        else:
            ask = input("User not found! Do you want to create?: ")
            res = ["y", "Y", "yes", "YES"]
            if ask in res:
                create()
            else:
                auth()
    except KeyError as k:
        print(f"Error: {k}")
        main.speak(f"Error: {k}")
    except TypeError as t:
        print(f"Error: {t}")
        main.speak(f"Error: {t}")
        
def create():
    col = ldb["user"]
    scol = ldb["su_users"]
    print("Please provide details below.")
    main.speak("Please provide details below.")
    fname = input("First Name: ")
    lname = input("Last Name:")
    mail = input("Email: ")
    if validate_mail(mail):
        x = col.find_one({"mail_id": mail})
        if x:
            u_mail = x["mail_id"]
            if mail == u_mail:
                print("Mail ID already exist.!")
                main.speak("Mail ID already exist.!")
                return auth()
    else:
        print("Please enter valid mail id")
        main.speak("Please enter valid mail id")
        return create()
    phone = input("Phone: ")
    dob = input("DOB: ")
    place = input("Place: ")
    uname = input("User Name: ")
    if validate_uname(uname):
        x = col.find_one({"uname": uname})
        if x:
            u_name = x["uname"]
            if uname == u_name:
                print("Username already exist.!")
                main.speak("Username already exist.!")
                return auth()
    else:
        print("Please enter valid Username")
        main.speak("Please enter valid Username")
        return create()
    pswd = pwinput.pwinput("Password: ")
    c_pswd = pwinput.pwinput("Confirm Password: ")
    if pswd != c_pswd:
        print("Provided password not match")
        main.speak("Provided password not match")
        create()
    ask = input("Want to add profilr pic now?: ")
    res = ["y", "Y", "yes", "YES"]
    if ask in res:
        # Create a Tkinter window
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        # Prompt the user to select an image file
        file_path = filedialog.askopenfilename(filetypes=[])
        # Read the image file
        with open(file_path, 'rb') as f:
            image_data = f.read()
            print("Image added.\n")
    else:
        image_data = "no data added"    
    print("SuperUser: su\nUser: usr\n")
    usermode = input("Usermode: ")
    add = {"fname" : fname, "lname": lname, "mail_id":mail, "phone": phone, "dob":dob, "place":place, "pswd": pswd, "uname":uname, "date": date_time, "image_data": image_data }
    if usermode == "su":
        user = input(main.Fore.RED + "Type existing superuser name:")
        try:
            su = scol.find_one({"fname": user}) #get user details from db.
            su_uname = input("Superuser Username: ")
            su_pswd = pwinput.pwinput("Superuser Password: ")
            # super user checking
            if su_uname == su["uname"] and su_pswd == su["pswd"]: # matching the credentials
                scol.insert_one(add)
                print("User details Added..!")
                main.speak("User details Added..!")
                send_mail.mail_send(mail)
                auth()
            else:
                print("Please type valid SuperUser username and password.")
                main.speak("Please type valid SuperUser username and password.")
                return auth() # recalling the auth function again.
        except TypeError as e:
            print(f"Error: {e}. Please type valid Name")
            main.speak(f"Error: {e}. Please type valid Name")
            return auth()
    elif usermode == "usr":
        col.insert_one(add)
        print("User details Added..!")
        main.speak("User details Added..!")
        send_mail.mail_send(mail)
        auth()
    else:
        print("Please Enter valid usermode")
        main.speak("Please Enter valid usermode")
        create()

def uname_edit():
    col = ldb["user"]

    fname = input("First Name:")
    uname = input("Enter new username: ")
    pswd = pwinput.pwinput("New password: ")
    cpswd = pwinput.pwinput("Confirm password: ")
    if pswd != cpswd:
        print("Password entered not matching")
        main.speak("Password entered not matching")
    ask = input("Want to add profilr pic now?: ")
    res = ["y", "Y", "yes", "YES"]
    if ask in res:
     # Create a Tkinter window
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        # Prompt the user to select an image file
        file_path = filedialog.askopenfilename(filetypes=[])
        # Read the image file
        with open(file_path, 'rb') as f:
            image_data = f.read()
    else:
        image_data = "no data added"

    f = col.find_one({"fname": fname})
    if f:
        name = f["fname"]
        if pswd == cpswd and fname == name:
            col.update_one({"fname":name},{"$set": {"uname":uname, "pswd": pswd, "image_data": image_data, "date":date_time}})
            print("User details Updated.")
            main.speak("User details Updated.")
            send_mail.upmail(uname, pswd)
            auth()
        else:
            print("Please provide valid credentials")
            uname_edit()
    else:
        print("Please provide valid credentials")
        uname_edit()