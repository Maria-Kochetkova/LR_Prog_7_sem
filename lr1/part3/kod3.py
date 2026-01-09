import concurrent.futures
import threading
import requests
import os

# Ограничение количества одновременных загрузок до 2
semaphore = threading.Semaphore(2)

def download_image(url, filename):
    """Функция для скачивания изображения с использованием семафора."""
    # Семафор гарантирует, что не более 2 потоков будут выполнять requests.get одновременно
    with semaphore:
        try:
            print(f"Начало загрузки: {filename}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            with open(filename, 'wb') as f:
                f.write(response.content)

            return f"Успешно: {filename}"
        except Exception as e:
            return f"Ошибка при загрузке {filename}: {e}"


def main():
    urls = [
        "https://i.pinimg.com/1200x/49/63/9c/49639c2c990049ffc1710b6e1db6e96d.jpg",
        "https://i.pinimg.com/1200x/f8/a5/3b/f8a53b51e3cca9831cb69746fa54f822.jpg",
        "https://i.pinimg.com/1200x/c7/3d/d8/c73dd826f423e807f7b5a915d52ac6e2.jpg",
        "https://i.pinimg.com/736x/a0/c5/da/a0c5da9f1703fa92ba8e9b77dd85c785.jpg"
    ]

    # Создание папки для сохранения, если её нет
    os.makedirs("downloads", exist_ok=True)

    # ThreadPoolExecutor для управления потоками
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []

        for i, url in enumerate(urls):
            filename = f"downloads/image_{i + 1}.jpg"
            future = executor.submit(download_image, url, filename)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            print(future.result())


if __name__ == "__main__":
    main()