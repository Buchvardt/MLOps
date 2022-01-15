import requests
import time
for i in range(30):
    resp = requests.post(
        'http://localhost:8000/api/comment/new',
        json={"email":"email@email.com","comment":f"Post number {i}","content_id":i}
    )
    print(f"Message number: {i}")
    time.sleep(0.5)