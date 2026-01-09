import threading
import timeit
import math


# Функция интегрирования
def integrate(f, a, b, *, n_iter=1000):
    """Написание программы для численного интегрирования площади под кривой."""
    dx = (b - a) / n_iter
    total_sum = 0
    x = a
    for _ in range(n_iter):
        total_sum += f(x) * dx
        x += dx
    return total_sum


# Многопоточная реализация с использованием Lock и ручного списка потоков
def partial_worker(f, a, n, dx, lock, result_container):
    local_sum = 0
    x = a
    for _ in range(n):
        local_sum += f(x) * dx
        x += dx

    with lock:
        result_container[0] += local_sum


def integrate_threaded(f, a, b, n_iter=1000, num_threads=4):
    dx = (b - a) / n_iter
    n_per_thread = n_iter // num_threads
    threads = []
    lock = threading.Lock()
    shared_result = [0.0]

    for i in range(num_threads):
        start_x = a + i * n_per_thread * dx
        # Расчет итераций для последнего потока
        current_n = n_per_thread if i != num_threads - 1 else n_iter - i * n_per_thread

        t = threading.Thread(
            target=partial_worker,
            args=(f, start_x, current_n, dx, lock, shared_result)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return shared_result[0]


# Параметры
A, B, N = 0, math.pi / 2, 10**6
FUNC = math.sin

# Замер времени
if __name__ == "__main__":
    ITERATIONS = [10 ** 4, 10 ** 5, 10 ** 6]
    THREADS = 4

    print(f"{'n_iter':<10} | {'Метод':<15} | {'Результат':<12} | {'Время (сек)':<12}")
    print("-" * 55)

    for n in ITERATIONS:
        # Для последовательного метода
        t_seq = timeit.timeit(lambda: integrate(FUNC, A, B, n_iter=n), number=1)
        res_seq = integrate(FUNC, A, B, n_iter=n)
        print(f"{n:<10} | Последоват.   | {res_seq:.8f} | {t_seq:.5f}")

        # Для многопоточного метода
        t_multi = timeit.timeit(lambda: integrate_threaded(FUNC, A, B, n, THREADS), number=1)
        res_multi = integrate_threaded(FUNC, A, B, n, THREADS)
        print(f"{'':<10} | Многопоточ.   | {res_multi:.8f} | {t_multi:.5f}")
        print("-" * 55)