import concurrent.futures
import time

def write_to_file(filename, data):
    """Поток для записи данных."""
    print(f"Начало записи в {filename}...")
    time.sleep(2)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    print("Запись завершена.")
    return True

def read_from_file(filename, write_future):
    """Поток для чтения данных."""
    print("Ожидание завершения записи...")
    if write_future.result():
        print(f"Файл готов. Чтение из {filename}:")
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content

def main():
    file_name = "data.txt"
    text_to_save = "Написан очень важный текст!"

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Запуск записывающего потока
        write_future = executor.submit(write_to_file, file_name, text_to_save)
        # Запуск прочитывающего потока с передачей объекта Future
        read_future = executor.submit(read_from_file, file_name, write_future)
        # Вывод финального результата
        print(f"\nРезультат чтения: {read_future.result()}")


if __name__ == "__main__":
    main()