import threading
import time

class SafeQueue:
    def __init__(self):
        self._queue = []
        self._lock = threading.RLock()

    def add(self, item):
        """Добавляет элемент в конец очереди."""
        with self._lock:
            self._queue.append(item)
            print(f"[+] Добавлено: {item}. Текущий размер: {len(self._queue)}")

    def remove(self):
        """Удаляет и возвращает первый элемент из очереди."""
        with self._lock:
            if not self._queue:
                print("[-] Очередь пуста.")
                return None
            item = self._queue.pop(0)
            print(f"[-] Удалено: {item}. Осталось элементов: {len(self._queue)}")
            return item

    def clear_all(self):
        """Пример метода, вызывающего другие методы под защитой RLock."""
        with self._lock:
            print("[!] Очистка всей очереди...")
            while self.remove() is not None:
                pass

def producer(q):
    for i in range(5):
        q.add(f"Данные_{i}")
        time.sleep(0.1)

def consumer(q):
    for _ in range(5):
        q.remove()
        time.sleep(0.15)


if __name__ == "__main__":
    my_queue = SafeQueue()

    t1 = threading.Thread(target=producer, args=(my_queue,))
    t2 = threading.Thread(target=consumer, args=(my_queue,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    my_queue.add("Последний элемент")
    my_queue.clear_all()