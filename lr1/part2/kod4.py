import threading

result = 1
lock = threading.Lock()

def partial_factorial(start, end):
    global result
    local_prod = 1
    for i in range(start, end + 1):
        local_prod *= i
    with lock:
        result *= local_prod

n = 10
mid = n // 2
# Поток 1 считает от 1 до 5, Поток 2 от 6 до 10
t1 = threading.Thread(target=partial_factorial, args=(1, mid))
t2 = threading.Thread(target=partial_factorial, args=(mid + 1, n))

t1.start(); t2.start()
t1.join(); t2.join()

print(f"Факториал {n} равен {result}")