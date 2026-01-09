import threading
import multiprocessing
import timeit
import math

# Базовая функция
def integrate(f, a, b, *, n_iter=1000):
    dx = (b - a) / n_iter
    total_sum = 0
    x = a
    for _ in range(n_iter):
        total_sum += f(x) * dx
        x += dx
    return total_sum

# Многопоточность (Threads)
def thread_worker(f, a, n, dx, lock, container):
    local_sum = sum(f(a + i * dx) * dx for i in range(n))
    with lock:
        container[0] += local_sum

def run_threads(f, a, b, n_iter, num_workers):
    dx = (b - a) / n_iter
    n_per_w = n_iter // num_workers
    lock = threading.Lock()
    res = [0.0]
    threads = []
    for i in range(num_workers):
        t = threading.Thread(target=thread_worker, args=(f, a + i * n_per_w * dx, n_per_w, dx, lock, res))
        threads.append(t)
        t.start()
    for t in threads: t.join()
    return res[0]

# Многопроцессность (Processes)
def process_worker(f, a, n, dx):
    return sum(f(a + i * dx) * dx for i in range(n))

def run_processes(f, a, b, n_iter, num_workers):
    dx = (b - a) / n_iter
    n_per_w = n_iter // num_workers
    # Pool для удобного распределения задач
    with multiprocessing.Pool(num_workers) as pool:
        args = [(f, a + i * n_per_w * dx, n_per_w, dx) for i in range(num_workers)]
        results = pool.starmap(process_worker, args)
    return sum(results)


if __name__ == "__main__":
    A, B = 0, math.pi / 2
    N = 10 ** 6
    FUNC = math.atan
    WORKERS = [2, 4, 6]
    REPEATS = 100

    print(f"Тест: integrate(math.atan, 0, pi/2, n_iter=10^6), Повторов: {REPEATS}\n")
    print(f"{'Тип':<12} | {'Потоков/Проц':<15} | {'Время (msec)':<15}")
    print("-" * 45)

    # 1. Последовательно
    t_seq = timeit.timeit(lambda: integrate(FUNC, A, B, n_iter=N), number=REPEATS)
    print(f"{'Последоват.':<12} | {'1':<15} | {(t_seq / REPEATS) * 1000:>12.3f}")

    # 2. Сравнение
    for count in WORKERS:
        t_thr = timeit.timeit(lambda: run_threads(FUNC, A, B, N, count), number=REPEATS)
        print(f"{'Многопоточ.':<12} | {count:<15} | {(t_thr / REPEATS) * 1000:>12.3f}")

        t_proc = timeit.timeit(lambda: run_processes(FUNC, A, B, N, count), number=REPEATS)
        print(f"{'Многопроц.':<12} | {count:<15} | {(t_proc / REPEATS) * 1000:>12.3f}")
        print("-" * 45)