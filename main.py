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

KEY = open("keys.enc","r").read()
KEY=bytes(KEY.split("'")[1],"utf-8")
cipher_suite = Fernet(KEY)

while True:
    platform_name = os.name
    platform_flag=None
    if platform_name=="nt":
        platform="Windows machine"
        platform_flag=1
    else:
        platform="Linux/Mac machine"
        platform_flag=0
    print("-----------Working on {}------------".format(platform))

    # Initial user inputs
    n=input("1.Login           2.Signup            3.Exit\n")

    if platform_flag==0:
        os.system("clear")
    else:
        os.system("cls")

    email=""
    password=""
    data_dict={}

    try:
        n=int(n)
    except:
        print("[Warning] Wrong Input")
        time.sleep(1)
        if platform_flag==0:
            os.system("clear")
        else:
            os.system("cls")
        continue
    
    if int(n)==1:
        email=input("Email:-  ")
        password=getpass("Password:-    ")

        if password=="":
            print("[Error] Please enter a valid password")
            time.sleep(1)
            if platform_flag==0:
                os.system("clear")
            else:
                os.system("cls")
            continue
        if "@" not in email and "." not in email:
            print("[Error] Please enter a valid email")
            time.sleep(1)
            if platform_flag==0:
                os.system("clear")
            else:
                os.system("cls")
            continue

    elif int(n)==2:
        username=input("Enter username:-    ")
        email=input("Enter Email:-  ")
        password=getpass("Enter Password:-    ")
        time.sleep(1)

        if password=="":
            print("[Error] Please enter a valid password")
            time.sleep(1)
            if platform_flag==0:
                os.system("clear")
            else:
                os.system("cls")
            continue

        if "@" not in email and "." not in email:
            print("[Error] Please enter a valid email")
            time.sleep(1)
            if platform_flag==0:
                os.system("clear")
            else:
                os.system("cls")
            continue

        try:
            user_path = "users"
            if user_path not in os.listdir("./"):
                os.mkdir(user_path)
        except Exception as err:
            print ("[info] Directory Already Exists" % user_path)
        
        user_id="0"
        user_data=""
        try:
            if os.listdir("users"):
                userfile = open(user_path+"/users.enc","r").read().split("'")[1]
                if userfile:
                    rfl = cipher_suite.decrypt(bytes(userfile,"utf-8"))
                    rfl=str(rfl).split("'")[1]
                    user_data = json.loads(rfl)
                    if len(user_data)>=10:
                        print("[Info] Maximum users limit exceeded")
                        time.sleep(1)
                        if platform_flag==0:
                            os.system("clear")
                        else:
                            os.system("cls")
                        continue
                    user_id=str(len(user_data))
            else:
                with open(user_path+"/users.enc","w") as file:
                    initial_userdata = cipher_suite.encrypt(bytes(json.dumps([]),"utf-8"))
                    file.write(str(initial_userdata))
                print("[Info] Created Users directory successfully!")

        except Exception as err:
            print(err)
            print("[Error] Users file missing")
            sys.exit()

        usr_flag=None
        for user in user_data:
            if user["email"]==email:
                usr_flag=1
                print("[Info] User already exists with this email address")
                time.sleep(1)
                break
        if usr_flag:
            if platform_flag==0:
                os.system("clear")
            else:
                os.system("cls")
            continue
        user_dict = {
            "username":username,
            "email":email,
            "password":password,
            "data_path":"data/"+user_id+".enc",
            "journal_entries":[],
            "journals":[]
        }

        user_list=[user_dict]
        if user_data:
            user_data.extend(user_list)
            encrypted_userdata = cipher_suite.encrypt(bytes(json.dumps(user_data),"utf-8"))
            with open(user_path+"/users.enc","w") as file:
                file.write(str(encrypted_userdata))
            print("[Info] Created user successfully..")
        else:
            encrypted_userdata = cipher_suite.encrypt(bytes(json.dumps(user_list),"utf-8"))
            with open(user_path+"/users.enc","w") as file:
                file.write(str(encrypted_userdata))
            print("[Info] Created user successfully.")
    elif int(n)==3:
        print("[Info] Exiting ...")
        time.sleep(1)
        if platform_flag==0:
            os.system("clear")
        else:
            os.system("cls")
        sys.exit()
    else:
        print("[Warning] Wrong Input")
        time.sleep(1)
        if platform_flag==0:
            os.system("clear")
        else:
            os.system("cls")
        sys.exit()

    time.sleep(1)
    if platform_flag==0:
        os.system("clear")
    else:
        os.system("cls")
    user_file=None
    try:
        user_file = open("users/users.enc","r")
    except:
        print("[Info] Signup first")
        time.sleep(1)
        if platform_flag==0:
            os.system("clear")
        else:
            os.system("cls")
        continue

    user_data=None
    user_data_index=None
    all_user_data = user_file.read().split("'")[1]
    all_user_data = str(cipher_suite.decrypt(bytes(all_user_data,"utf-8"))).split("'")[1]
    all_user_data = json.loads(all_user_data)

    if all_user_data:
        for x in range(len(all_user_data)):
            if all_user_data[x]["email"]==email and all_user_data[x]["password"]==password:
                user_data=all_user_data
                user_data_index=x
    if user_data is None and n==1:
        print("[Warning] No User exists with this Email or Password")
        continue
    while True:
        input_entries = input("1.Show all Entries               2.Create new Entry                   3.Logout                 4.Exit\n")

        journal_count = len(user_data[user_data_index]["journal_entries"])
        user_file.close()
        try:
            input_entries=int(input_entries)
        except:
            print("[Warning] Wrong Input")
            time.sleep(1)
            if platform_flag==0:
                os.system("clear")
            else:
                os.system("cls")
            continue
        if int(input_entries)==1:
            rf = user_data[user_data_index]
            if rf["journals"]:
                for count,jour in enumerate(rf["journal_entries"]):
                    print("{}. {}".format(count,jour))
                journal_no=input("[Info] Enter a journal index value\n")
                try:
                    journal_data = rf["journals"][int(journal_no)]
                    print(journal_data)
                    time.sleep(1)
                except:
                    print("[Warning] Wrong input")
                    print("[Info] Press Enter to exit")
                if input()==False:
                    continue
                    if platform_flag==0:
                        os.system("clear")
                    else:
                        os.system("cls")
            else:
                print("[Info] No Journals entries")
                time.sleep(1)
            if platform_flag==0:
                os.system("clear")
            else:
                os.system("cls")
            continue

        elif int(input_entries)==2:
            print("[Info] Write Journal data here")
            print("[Info] Press ENTER twice to save")
            journal_text = []
            while True:
                line=input()
                if line:
                    journal_text.append(line)
                else:
                    break
            journal_text = "\n".join(journal_text)
            rf=user_data[user_data_index]
            rf["journals"].insert(0,journal_text)
            user_data[user_data_index]["journal_entries"].insert(0,str(time.strftime('%a, %d %b %H:%M %p',time.gmtime())) +"  "+journal_text[:50])
            if journal_count==50:
                user_data[user_data_index]["journals"].pop()
                user_data[user_data_index]["journal_entries"].pop()
            with open("users/users.enc","r") as encfile:
                encfile.read()
                encrypted_userinfo = cipher_suite.encrypt(bytes(json.dumps(user_data),"utf-8"))
                with open("users/users.enc","w") as file:
                    file.write(str(encrypted_userinfo))
            if platform_flag==0:
                os.system("clear")
            else:
                os.system("cls")
            continue

        elif int(input_entries)==3:
            print("[Info] Logging out ...")
            time.sleep(1)
            if platform_flag==0:
                os.system("clear")
            else:
                os.system("cls")
            break

        elif int(input_entries)==4:
            print("[Info] Exiting ...")
            time.sleep(1)
            if platform_flag==0:
                os.system("clear")
            else:
                os.system("cls")
            sys.exit()

        else:
            print("[Warning] Wrong Input")
            print("[Info] press Enter to exit")
            time.sleep(1)
            if platform_flag==0:
                os.system("clear")
            else:
                os.system("cls")
            continue

print("Thanks for using the App")