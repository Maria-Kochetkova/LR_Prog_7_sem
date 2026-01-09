import threading
import time

def setter_thread(event):
    """Первый поток: устанавливает событие через 3 секунды."""
    print("[Поток 1] Запущен. Установит событие через 3 секунды...")
    for i in range(3):
        time.sleep(1)
        print(f"[Поток 1] Прошло секунд: {i + 1}")

    event.set()
    print("[Поток 1] Событие установлено!")

def waiter_thread(event):
    """Второй поток: ждет наступления события."""
    print("[Поток 2] Ожидание события...")
    event.wait()
    print("[Поток 2] Событие произошло!")


def checker_thread(event):
    """Третий поток: проверяет событие, пока оно не наступит."""
    print("[Поток 3] Проверка запущена...")
    while not event.is_set():
        print("[Поток 3] Событие не произошло")
        time.sleep(1)
    print("[Поток 3] Событие произошло, поток остановлен.")


def main():
    shared_event = threading.Event()

    t1 = threading.Thread(target=setter_thread, args=(shared_event,))
    t2 = threading.Thread(target=waiter_thread, args=(shared_event,))
    t3 = threading.Thread(target=checker_thread, args=(shared_event,))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
    print("Программа завершена.")


if __name__ == "__main__":
    main()