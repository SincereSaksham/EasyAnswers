from bs4 import BeautifulSoup
import requests
from pprint import pprint

#Enter the url for the google forms
URL = input("Enter the URL : ")

# fetching the url of the form
response = requests.get(url=URL)
response.raise_for_status()
content = response.text

# creating soup object
span = None
question_list = []
answer_list= []
try:
    soup = BeautifulSoup(content, 'html.parser')
    question_answer = soup.find_all(name="div", class_="Qr7Oae")
    for question in question_answer:
        question_list.append(question.find(class_="M7eMe").text)  #scrarping the qeustion done 
        try:
            answer_list.append(question.find_all(class_= "aDTYNe snByac OvPDhc OIC90c").get_text())  #this line is not working, cant scrape the answers after scraping the question block div.
        except:
            answer_list.append([""])
except:
    print("error in scraping the site or url")

print(question_list)
print(answer_list)

