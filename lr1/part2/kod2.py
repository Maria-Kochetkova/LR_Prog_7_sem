import threading
import requests

def download_file(url, filename):
    try:
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Файл {filename} успешно скачан.")
    except Exception as e:
        print(f"Ошибка при скачивании {filename}: {e}")

urls = {
    "https://i.pinimg.com/1200x/b6/2c/de/b62cdeb40361bc5669f86647ea717625.jpg": "img1.jpg",
    "https://i.pinimg.com/1200x/61/52/37/615237464427270c2e9425a6f571f497.jpg": "img2.jpg",
    "https://i.pinimg.com/736x/4e/f5/cf/4ef5cffc9c405ff23a151034a2685b70.jpg": "img3.jpg"
}

threads = []
for url, name in urls.items():
    t = threading.Thread(target=download_file, args=(url, name))
    threads.append(t)
    t.start()

for t in threads:
    t.join()