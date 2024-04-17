from pymongo import MongoClient
import main, database


client = MongoClient("mongodb://localhost:27017/")
mydb = client["mizbee"]
su_col = mydb["su_users"]
def su_create():
    print("Please provide details below.")
    main.speak("Please provide details below.")

    fname = input("First Name: ")
    lname = input("Last Name:")
    mail = input("Email: ")
    x = su_col.find_one({"mail_id": mail})
    if x:
        u_mail = x["mail_id"]
        if mail == u_mail:
            print("Mail ID already exist.!")
            main.speak("Mail ID already exist.!")
            return su_create()
    phone = input("Phone: ")
    dob = input("DOB: ")
    place = input("Place: ")
    uname = input("User Name: ")
    x = su_col.find_one({"uname": uname})
    if x:
        u_name = x["uname"]
        if uname == u_name:
            print("Username already exist.!")
            main.speak("Username already exist.!")
            return su_create()
    pswd = input("Password: ")
    c_pswd = input("Confirm Password: ")

    ask = input("Want to add profilr pic now?: ")
    res = ["y", "Y", "yes", "YES"]
    if ask in res:
        # Create a Tkinter window
        root = database.tk.Tk()
        root.withdraw()  # Hide the root window

        # Prompt the user to select an image file
        file_path = database.filedialog.askopenfilename(filetypes=[])

        # Read the image file
        with open(file_path, 'rb') as f:
            image_data = f.read()
    else:
        image_data = "no data added"    
        
    if pswd == c_pswd:
        add = {"fname" : fname, "lname": lname, "mail_id":mail, "phone": phone, "dob":dob, "place":place, "pswd": pswd, "uname":uname, "date": database.date_time, "image_data": image_data }
        su_col.insert_one(add)
        print("User details Added..!")
        main.speak("User details Added..!")
    else:
        print("Enter the valid password credential..!")
        main.speak("Enter the valid password credential..!")
        