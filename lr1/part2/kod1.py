import threading

def print_name():
    # Получение имени текущего потока
    print(f"Запущен поток: {threading.current_thread().name}")

threads = []
for i in range(5):
    # Создание потока с уникальным именем
    t = threading.Thread(target=print_name, name=f"Поток-{i+1}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()