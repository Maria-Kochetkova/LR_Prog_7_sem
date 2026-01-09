import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# Переменные: [x11, x12, x13, x21, x22, x23]
c = [8, 6, 10, 9, 7, 5]

# Матрица ограничений-равенств A_eq @ x = b_eq
A_eq = [
    [1, 1, 1, 0, 0, 0],  # Склад 1 (запас 150) [cite: 251]
    [0, 0, 0, 1, 1, 1],  # Склад 2 (запас 250) [cite: 253]
    [1, 0, 0, 1, 0, 0],  # База Альфа (потребность 120) [cite: 255]
    [0, 1, 0, 0, 1, 0],  # База Бета (потребность 180) [cite: 256]
    [0, 0, 1, 0, 0, 1]  # База Гамма (потребность 100) [cite: 257]
]
b_eq = [150, 250, 120, 180, 100]  # [cite: 261]
bounds = [(0, None)] * 6

# Решение
res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
x = res.x

fig, ax = plt.subplots(figsize=(12, 8))

# Координаты узлов [cite: 308, 309]
warehouse_data = {'Склад 1': (2, 8, 150), 'Склад 2': (2, 3, 250)}
base_data = {'Альфа': (10, 9, 120), 'Бета': (10, 5.5, 180), 'Гамма': (10, 2, 100)}

# Отрисовка узлов
# Отрисовка складов с указанием запаса
for name, (nx, ny, val) in warehouse_data.items():
    ax.text(nx, ny, f"{name}\nЗапас: {val} т",
            bbox=dict(facecolor='#AED6F1', boxstyle='round,pad=1'), ha='center', fontweight='bold')

# Отрисовка баз с указанием потребности
for name, (nx, ny, val) in base_data.items():
    ax.text(nx, ny, f"База {name}\nНужно: {val} т",
            bbox=dict(facecolor='#ABEBC6', boxstyle='round,pad=1'), ha='center', fontweight='bold')

# x = [x11, x12, x13, x21, x22, x23]
connections = [
    ('Склад 1', 'Альфа', x[0], c[0]),
    ('Склад 1', 'Бета', x[1], c[1]),
    ('Склад 1', 'Гамма', x[2], c[2]),
    ('Склад 2', 'Альфа', x[3], c[3]),
    ('Склад 2', 'Бета', x[4], c[4]),
    ('Склад 2', 'Гамма', x[5], c[5])
]

for start_node, end_node, volume, cost in connections:
    if volume > 0.1:
        start_coords = warehouse_data[start_node][:2]
        end_coords = base_data[end_node][:2]

        arrow = FancyArrowPatch(start_coords, end_coords,
                                arrowstyle='->', mutation_scale=20,
                                linewidth=volume / 20, color='gray', alpha=0.6)
        ax.add_patch(arrow)

        mid_x, mid_y = (start_coords[0] + end_coords[0]) / 2, (start_coords[1] + end_coords[1]) / 2
        ax.text(mid_x, mid_y + 0.2, f"{volume:.0f} т\n({cost} усл.ед/т)",
                fontsize=9, fontweight='bold', color='darkred', ha='center')

ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.axis('off')
ax.set_title('Оптимальный план снабжения военных баз', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()