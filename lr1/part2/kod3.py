import threading
import requests

def fetch_url(url):
    response = requests.get(url)
    print(f"URL: {url} | Статус: {response.status_code} | Длина: {len(response.text)}")

urls = ["https://google.com", "https://github.com", "https://python.org"]
threads = [threading.Thread(target=fetch_url, args=(u,)) for u in urls]

for t in threads: t.start()
for t in threads: t.join()