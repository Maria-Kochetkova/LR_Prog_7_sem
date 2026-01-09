import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

# 1. Решение задачи
c = [-8000, -12000]
A_ub = [
    [2, 3],  # Процессорное время
    [4, 6],  # Память
    [1, 2]   # Аккумуляторы
]
b_ub = [240, 480, 150]
bounds = [(0, None), (0, None)]

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

print(f"Статус: {res.message}")
print(f"Смартфоны (x1): {res.x[0]:.2f}")
print(f"Планшеты (x2): {res.x[1]:.2f}")
print(f"Макс. прибыль: {-res.fun:.2f} руб.")

# 2. Визуализация
x1 = np.linspace(0, 150, 400)
x2_1 = (240 - 2*x1) / 3
x2_2 = (480 - 4*x1) / 6
x2_3 = (150 - 1*x1) / 2

plt.figure(figsize=(10, 8))
plt.plot(x1, x2_1, label='Процессорное время (2x1+3x2<=240)')
plt.plot(x1, x2_2, 'r--', label='Память (4x1+6x2<=480)')
plt.plot(x1, x2_3, label='Аккумуляторы (x1+2x2<=150)')

y_min = np.minimum(np.maximum(0, x2_1), np.maximum(0, x2_3))
plt.fill_between(x1, 0, y_min, color='gray', alpha=0.3, label='Допустимая область')
plt.scatter(res.x[0], res.x[1], color='red', s=100, label='Оптимум')

plt.xlim(0, 130); plt.ylim(0, 90)
plt.xlabel('Смартфоны'); plt.ylabel('Планшеты')
plt.legend(); plt.grid(True)
plt.title('Оптимизация производства')
plt.show()