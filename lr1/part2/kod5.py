import threading
import random

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    if len(arr) < 1000:
        return quick_sort(left) + middle + quick_sort(right)

    results = {}

    def sorted_part(part, key):
        results[key] = quick_sort(part)

    t1 = threading.Thread(target=sorted_part, args=(left, 'left'))
    t2 = threading.Thread(target=sorted_part, args=(right, 'right'))

    t1.start();
    t2.start()
    t1.join();
    t2.join()

    return results['left'] + middle + results['right']


data = [random.randint(0, 100) for _ in range(10)]
print(f"Изначальный набор: {data}")
print(f"Отсортировано: {quick_sort(data)}")