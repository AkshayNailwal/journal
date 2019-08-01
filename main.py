import os
import sys
from getpass import getpass
from cryptography.fernet import Fernet
from collections import deque
import json
import time

if "keys.enc" not in os.listdir("./"):
    KEY = Fernet.generate_key()
    # print(key)
    print(str(KEY).encode("latin1"))
    with open("keys.enc","w") as file:
        file.write(str(KEY))
    # cipher_suite = Fernet(key)
    # cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")
    # print(cipher_text)
    # plain_text = cipher_suite.decrypt(cipher_text)
    # print(plain_text)

# Read key from file
KEY = open("keys.enc","r").read()
KEY=bytes(KEY.split("'")[1],"utf-8")
cipher_suite = Fernet(KEY)

platform_name = os.name
if platform_name=="nt":
    platform="Windows machine"
    platform_flag=1
else:
    platform="Linux/Mac machine"
    platform_flag=0
print("-----------Working on {}------------".format(platform))

# Initial user inputs
n=int(input("1.Login           2.Signup            3.Exit\n"))

if platform_flag==0:
    os.system("clear")
else:
    os.system("cls")

username=""
password=""
if n==1:
    while True:
        username=input("Username:-  ")
        password=getpass("Password:-    ")

elif n==2:
    username=input("Enter username:-    ")
    email=input("Enter Email:-  ")
    password=getpass("Enter Password:-    ")

    try:
        data_path = "data"
        if data_path not in os.listdir("./"):
            os.mkdir(data_path)
    except Exception as err:
        print ("Diretory Already Exists" % data_path)

    data_dict = {
        "username":username,
        "email":email,
        "password":password,
        "data_path":data_path+"/"+username+".enc",
        "journal_entries":[],
        "journals":[],
        "entries":0
    }
    try:
        data_path = "users"
        if data_path not in os.listdir("./"):
            os.mkdir(data_path)
    except Exception as err:
        print ("Directory Already Exists" % data_path)
    
    user_dict = {
        "username":username,
        "password":pssword
    }

if platform_flag==0:
    os.system("clear")
else:
    os.system("cls")

input_entries = input("1. Show all Entries               2. Create new Entry                   3.Back\n")

# gonna be a loop
if input_entries==1:
    readfile = open(data_dict["data_path"],"r").read().split("'")[1]
    rf = cipher_suite.decrypt(bytes(readfile,"utf-8"))
    rf = json.loads(rf)
    for (i,j) in enumerate(rf["journal_entries"]):
        print("{}. {}".format(i,j))
    journal_no=int(input("[Info] Enter a integer value"))
    print(rf["journal_entries"][journal_no])

elif input_entries==2:
    print("[Info] Press ENTER twice to save")
    journal_text = []
    while True:
        line=input()
        if line:
            journal_text.append(line)
        else:
            break
    journal_text = "\n".join(journal_text)
    readfile = open(data_dict["data_path"],"r").read().split("'")[1]
    rf = cipher_suite.decrypt(bytes(readfile,"utf-8"))
    rf = json.loads(rf)
    rf["journals"] = journal_text
    rf["journal_entries"] = str(time.ctime(time.time())) + journal_text[:150]
    
    encrypted_userdata = cipher_suite.encrypt(bytes(json.dumps(rf),"utf-8"))
    with open(rf["data_path"],"w") as file:
        file.write(str(encrypted_userdata))

# cipher_suite = Fernet(KEY)
# encrypted_userdata = cipher_suite.encrypt(bytes(json.dumps(data_dict),"utf-8"))
# with open(data_dict["data_path"],"w") as file:
#     file.write(str(encrypted_userdata))

# readfile = open(data_dict["data_path"],"r").read().split("'")[1]
# print(readfile)
# rf = cipher_suite.decrypt(bytes(readfile,"utf-8"))
# print(rf, type(rf))
# rf = json.loads(rf)
# print(rf, type(rf))
# print(dict(rf))



# if platform_flag==0:
#     os.system("clear")
# else:
#     os.system("cls")
print("Hurray!")