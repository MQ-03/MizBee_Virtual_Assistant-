from statistics import mode
from getpass4 import getpass
import smtplib, main
from pymongo import MongoClient
from PIL import Image
import io

#database variables
client = MongoClient("mongodb://localhost:27017/") #change the connection string of the mongoDB.
mydb = client["mizbee"] #change the db name
col = mydb["user"] # change the collection name of normal users
scol = mydb["su_users"] # change the collection name of normal super users

#database variables
host = "smtp.gmail.com"
port = 587
from_mail = "mizbee.ai.info@gmail.com"
password = "fjxp zbvb ztth zawp"
#mail status and SMTP responses
try:
    smtp = smtplib.SMTP(host, port)
    status_code, response = smtp.ehlo()
    status_code, response = smtp.starttls()
    status_code, response = smtp.login(from_mail, password)
except Exception as e:
    main.speak(e)
#Confirmation mail once user created
def mail_send(mail):

    usr = col.find_one({"mail_id": mail}) # find mail id's from database
    
    if usr:
        fname = usr["fname"]
        lname = usr["lname"]
    else:
        usr1 = scol.find_one({"mail_id": mail})
        fname = usr1["fname"]
        lname = usr1["lname"]
   
    SUBJECT = f"Hello {fname}! Welcome to MizBee's AI World..!"
    TEXT = f"Hi, {fname} {lname}!\n\n We are welcomes you to Mizbee's AI wolrd..!\n Your now a MizBee AI User. You can access MizBee AI lite services seamlessly.\n\n\n Thanks..!\nMizBee's Team."
    msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    
    print(f"[*] Echoing the server: {status_code} {response}")
    print(f"[*] Starting TLS connection : {status_code} {response}")
    print(f"[*] Logging in : {status_code} {response}")
    smtp.sendmail(from_mail, mail , msg)
    print("Confirmation Mail Sent Successfully! Please check your inbox.")
    main.speak("Confirmation Mail Sent Successfully! Please check your inbox.")
    smtp.quit()

#user details updated confirmation mail
def upmail(uname, pswd):

    usr = col.find_one({"uname": uname})
    if usr:
        uname = usr["uname"]
        pswd = usr["pswd"]
        fname = usr["fname"]
        lname = usr["lname"]
        mail = usr["mail_id"]

    SUBJECT = f"Hello {fname}! Your Account Credentials updated."
    TEXT = f"Hi, {fname} {lname}!\n\n We are welcomes you to Mizbee's AI wolrd..!\n Your MizBee's account credentials updated.Please find the credentials below.\n\n Usernmae: {uname}\n Password: {pswd}\n\n\nThanks..!\nMizBee's Team."
    msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    smtp.sendmail(from_mail, mail, msg)
    print("Confirmation Mail Sent Successfully! Please check your inbox.")
    main.speak("Confirmation Mail Sent Successfully! Please check your inbox.")
    smtp.quit()