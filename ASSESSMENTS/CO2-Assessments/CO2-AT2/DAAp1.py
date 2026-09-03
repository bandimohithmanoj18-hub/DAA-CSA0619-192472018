import math

points = [
    (2, 3),
    (5, 8),
    (9, 4),
    (1, 7),
    (6, 1)
]

max_distance = 0
farthest_pair = ()

for i in range(len(points)):
    for j in range(i + 1, len(points)):
        x1, y1 = points[i]
        x2, y2 = points[j]

        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        if distance > max_distance:
            max_distance = distance
            farthest_pair = (points[i], points[j])

print("Farthest Pair :", farthest_pair)
print("Maximum Distance :", round(max_distance, 2))