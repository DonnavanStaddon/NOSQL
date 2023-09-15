import os
import pymongo
if os.path.exists("env.py"):
    import env


MONGO_URI =os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


def show_menu():
    print("")
    print("1. Add a record")
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit")

    option = input("Enter option: ")
    return option

# GETS ALL THE RECORDS IN DB = THIS FUCNTION WILL BE CALLED IN DELETE/UPDATE FUNCTIONS
def get_record():
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")

    try:
        doc = coll.find_one({"first": first.lower(), "last": last.lower()})
    except:
        print("Error accessing the database")

    if not doc:
        print("")
        print("Error! No results found.")

    return doc


# INSERT DATA INTO DB
def add_record():
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")
    dob = input("Enter date of birth > ")
    gender = input("Enter gender > ")
    hair_color = input("Enter hair color > ")
    occupation = input("Enter occupation > ")
    nationality = input("Enter nationality > ")

    # Dictionary to insert into DB from add_record function
    new_doc = {
        "first": first.lower(),
        "last": last.lower(),
        "dob": dob,
        "gender": gender,
        "hair_color": hair_color,
        "occupation": occupation,
        "nationality": nationality
    }

    try:
        coll.insert_one(new_doc)
        print("")
        print("Documents inserted")
    except:
        print("Error accessing the database")

#FIND RECORD IN DB
def find_record():
    doc = get_record() # CALLING THE GET RECORDS FUCTION ABOVE
    if doc:
        print("")
        for k,v in doc.items(): # Iterating thoo the keys and values inside the .doc-item method with a for loop
            if k != "_id": # Filter out id field because we dont want to edit it
                print(k.capitalize() + ": " + v.capitalize()) # print First Name and Last Name from DB


# EDIT RECORD
def edit_record():
    doc = get_record()
    if doc:
        #Empty Dictionary Values will be added to it from the for loop below
        update_doc = {}
        print("")
        for k,v in doc.items(): # Iterating over key value pairs in doc
            if k != "_id": # Filter out id field because we dont want to edit it
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")#FOR EACH ITERATION PROVIDE THE KEY FOR UPDATE DOC DICTIONARY AND SET IT EQUAL TO A USER INPUT PROMPT THE VALUE FOR THE INPUT WILL DISPLAY THE CURRENT KEY CAPITALIZED INSIDE SQUARE BRACKETS SHOW THE VALUE WE EDITING

                if update_doc[k] == "": #Check if input was left blank or empty
                    update_doc[k] = v #If input was blank leave it the same as before

    try:
        coll.update_one(doc, {"$set": update_doc})# Update doc with new info
        print("")
        print("Document updated")
    except:
        print("Error accessing the database")


def delete_record():
    doc = get_record()
    if doc:
        print("")
        for k,v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())

    print("")
    confirmation = input("Is this the document you want to delete?\nY or N > ")
    print("")

    if confirmation.lower() == "y":
        try:
            coll.delete_one(doc)
            print("Document delete!")
        except:
            print("Error accessing the database")
    else:
        print("Documnet not deleted")



def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()# calling add_record function
        elif option == "2":
            find_record()# calling find record function
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid option")
            print("")


# Connect to DB and Collect from DB
conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
# Continue to show menu and dispay proccess
main_loop()