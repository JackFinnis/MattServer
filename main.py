import requests, datetime, firebase_admin, bs4
from firebase_admin import messaging, db, credentials
from firebase_admin.messaging import Message, Notification, APNSConfig, APNSPayload, Aps

def detect_new_cartoon(event, context):
    cred = credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://testing-54a06-default-rtdb.europe-west1.firebasedatabase.app'
    })

    response = requests.get("https://www.telegraph.co.uk")
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    cartoon = soup.select("img[alt='Matt cartoon']")[0]
    url = cartoon["src"].split("?")[0]

    old_url = db.reference('url').get()
    db.reference('url').set(url)

    if url != old_url:
        db.reference('urls').push({
            'url': url,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        topic = "new_cartoon"
        title = "New Cartoon!"
        body = "View today's Matt Cartoon"
        headers = { "apns-collapse-id": topic }
        apns = APNSConfig(payload=APNSPayload(aps=Aps(badge=1)), headers=headers)
        notification = Notification(title=title, body=body)
        message = Message(notification=notification, topic=topic, apns=apns)
        messaging.send(message)

if __name__ == '__main__':
    detect_new_cartoon(None, None)