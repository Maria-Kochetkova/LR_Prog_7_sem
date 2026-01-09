import threading
import time

def server_task(barrier1, barrier2):
    print("[Поток-сервер] Запуск и настройка систем...")
    time.sleep(2)
    print("[Поток-сервер] Готов к приему соединений. Ожидание...")
    barrier1.wait()

    barrier2.wait()
    print("[Поток-сервер] Получен запрос от клиента! Обработка...")
    time.sleep(1)
    print("[Поток-сервер] Запрос обработан успешно.")

def client_task(barrier1, barrier2):
    """Поток клиента: ждет сервер, прежде чем отправить данные."""
    print("[Поток-клиент] Поток запущен. Ожидание готовности сервера...")
    barrier1.wait()

    barrier2.wait()
    print("[Поток-клиент] Сервер доступен! Отправка запроса...")


def main():
    barrier1 = threading.Barrier(2)
    barrier2 = threading.Barrier(2)

    t_server = threading.Thread(target=server_task, args=(barrier1, barrier2,))
    t_client = threading.Thread(target=client_task, args=(barrier1, barrier2,))

    t_server.start()
    t_client.start()

    t_server.join()
    t_client.join()
    print("Взаимодействие завершено.")

if __name__ == "__main__":
    main()