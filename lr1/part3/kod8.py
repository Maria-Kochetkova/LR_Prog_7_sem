import os
import threading
import concurrent.futures

def search_files(file_list, target, found_event):
    for file in file_list:
        # Если другой поток уже нашел файл, немедленно остановка
        if found_event.is_set():
            return

        if target in file:
            print(f"Найдено: {file}")
            found_event.set()  # Остановка потоков
            return

def main():
    directory = "."
    target = "data.txt"
    all_files = os.listdir(directory)

    mid = len(all_files) // 2
    chunks = [all_files[:mid], all_files[mid:]]

    stop_signal = threading.Event()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(search_files, chunk, target, stop_signal) for chunk in chunks]
        concurrent.futures.wait(futures)


if __name__ == "__main__":
    main()