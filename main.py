from bs4 import BeautifulSoup
import requests
import os
from tabulate import tabulate
import time

## Notes ##
# If there is a space before typing that is a comment for explaination
#print("If there isn't a space before, that is commented out code")
# you can read the commented out code but most of it is just for debugging errors and other stuff

###############################

# LOGIN INFO GOES HERE

username = ""
password = ""

################################
# Username & Password (remove when giving to other people)


if username == "":
    print("you gotta fill in your login!")
    time.sleep(10000)

if password == "":
    print("you gotta fill in your login!")
    time.sleep(10000)


tabulate.PRESERVE_WHITESPACE = True

session = requests.Session()

# Handles Cookies for logging in and persistance

url = "https://homeaccess.beth.k12.pa.us/HomeAccess/Account/LogOn/index.html"

r = session.get(url)
# setting the website url to 'r'

soup = BeautifulSoup(r.text, features="html.parser")
# extracting the raw website data into 'soup' 
#print(soup, end="\n \n \n \n")
# Printing out the website data for debugging
usrName = soup.find("input", {"type":"password"})
psswd = soup.find("input", {"type":"text"})
# Wat?

VerificationToken = soup.find("input", {"name":"__RequestVerificationToken"}).get("value")
# This grabs the Verification code for the signin. No idea why this is now a thing but cool ig

#print(VerificationToken)

#exit()

payload = {
    "__RequestVerificationToken" : VerificationToken,
    "ReturnUrl" : "/HomeAccess/Classes/Classwork",
    "SCKTY00328510CustomEnabled" : False,
    "Database" : 10,
    "LogOnDetails.UserName" : username,
    "LogOnDetails.Password" : password
          }

# Payload Information to send for login

GradeLogin = session.post(url = "https://homeaccess.beth.k12.pa.us/HomeAccess/Account/LogOn/index.html?ReturnUrl=%2fhomeaccess", data = payload)

# Sending to Payload to the website for login

soup = BeautifulSoup(GradeLogin.text, features="html.parser")

# Parsing the response from the payload

assignments = soup.find("iframe")

#print(soup)

#exit()

# Finding the Location of the Grades

#print(assignments.get("src"), end="\n \n \n \n")

# Debug Print out link

link_get_source = "https://homeaccess.beth.k12.pa.us" + assignments.get("src")

# Generates Link for the Extraction

#print(link_get_source, end="\n \n \n \n")

# Prints out link

GradesLocation = session.post(url = link_get_source, data = payload)

# grabs grades location

soup = BeautifulSoup(GradesLocation.text, features="html.parser")

# Applies grades code to the variable 'soup' 



classes = soup.find_all("a", {"class":"sg-header-heading"})
# Finds Classes Names

averages = soup.find_all("span", {"class":"sg-header-heading sg-right"})
# Finds Grades for the class

mixed = []
# initialize the array for the mixed classname/grades

for i, j in zip(classes, averages):
    _temp_ = [i.text.strip(), j.text]
    mixed.append(_temp_)

# initiates a loop for every class in the list to find the grades for the class and put them in an array

print('\n')
print(username, "'s grades:")

print(tabulate(mixed, headers=["class", "grade"], tablefmt="pretty", colalign=("left",)))
# Prints out a nice table full of your data! Now I will sell it to facebook!

#print(mixed)
# prints out the raw array of information sent through tabulate

#time.sleep(10000)
## So the window doesnt dissappear right away
# We editing this now so that it will exit after you press enter
H = input("Press Enter To Quit: ")
exit()
