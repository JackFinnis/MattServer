import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import messaging
from firebase_admin.credentials import Certificate
from firebase_admin.messaging import Message, Notification, APNSConfig, APNSPayload, Aps

credential = Certificate("credential.json")
app = firebase_admin.initialize_app(credential)

telegraph = "https://www.telegraph.co.uk"
response = requests.get(telegraph)
html = response.text
soup = BeautifulSoup(html, "html.parser")
cartoon = soup.select("img[alt='Matt cartoon']")[0]
url = cartoon["src"].split("?")[0]

with open("url.txt", "r") as file:
    old_url = file.read()
with open("url.txt", "w") as file:
    file.write(url)

if url != old_url:
    with open("urls.txt", "a") as file:
        file.write(url + '\n')
    
    topic = "new_cartoon"
    title = "New Cartoon!"
    body = "View today's Matt Cartoon"
    headers = { "apns-collapse-id": topic }
    apns = APNSConfig(payload=APNSPayload(aps=Aps(badge=1)), headers=headers)
    notification = Notification(title=title, body=body)
    message = Message(notification=notification, topic=topic, apns=apns)
    messaging.send(message)