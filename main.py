import os
import sys

from getpass import getpass
from cryptography.fernet import Fernet

if "keys." not in os.walk("./"):
    key = Fernet.generate_key()
    print(key)
    with open("keys.","w") as file:
        file.write(str(key))
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")
    print(cipher_text)
    plain_text = cipher_suite.decrypt(cipher_text)
    print(plain_text)

# platform_name = os.name
# if platform_name=="nt":
#     platform="Windows machine"
#     platform_flag=1
#     print("-----------Working on {}------------".format(platform))
#     print("[Error] This Application is intended for Linux/Mac Machine only")
#     sys.exit()
# else:
#     platform="Linux/Mac machine"
#     platform_flag=0
#     print("-----------Working on {}------------".format(platform))


# n=int(input("1.Login           2.Signup\n"))

# if platform_flag==0:
#     os.system("clear")
# else:
#     os.system("cls")

# if n==1:
#     while True:
#         username=input("Username:-  ")
#         password=getpass("Password:-    ")


# elif n==2:
#     username=input("Enter Username:-    ")
#     email=input("Enter Email:-  ")
#     password=getpass("Enter Password:-    ")

# if platform_flag==0:
#     os.system("clear")
# else:
#     os.system("cls")
# print("Hurray!")