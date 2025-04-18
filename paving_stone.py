import math
import numpy as np
from PIL import Image, ImageFilter
import random

def splatting(size, num_splats=30, splat_radius_lower=3, splat_radius_upper=6, blur_radius=3):
    image = np.ones((size, size, 3), dtype=np.uint8) * 255

    for _ in range(num_splats):
        cx = random.randint(0, size - 1)
        cy = random.randint(0, size - 1)
        radius = splat_radius_lower + random.random() * (splat_radius_upper - splat_radius_lower)

        for dy in range(int(-radius) - 1, int(radius + 1) + 1):
            for dx in range(int(-radius) - 1, int(radius + 1) + 1):
                if dx**2 + dy**2 <= radius**2:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < size and 0 <= ny < size:
                        image[ny, nx] = [0, 0, 0]

    img = Image.fromarray(image)

    blurred = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    blurred.show()

def normal_map(img, strength=1.0):
    gray = img.convert("L")
    gray_np = np.asarray(gray, dtype=np.float32)

    gray_np /= 255.0

    dx = np.gradient(gray_np, axis=1)
    dy = np.gradient(gray_np, axis=0)

    normal_x = -dx * strength
    normal_y = -dy * strength
    normal_z = np.ones_like(gray_np)

    length = np.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
    normal_x /= length
    normal_y /= length
    normal_z /= length

    normal_map = np.stack((
        (normal_x * 0.5 + 0.5) * 255,
        (normal_y * 0.5 + 0.5) * 255,
        (normal_z * 0.5 + 0.5) * 255
    ), axis=2).astype(np.uint8)

    return Image.fromarray(normal_map)

def paving_stones(size, num_stones=10, stone_spacing=32, border_range=2):
    image = np.ones((size, size, 3), dtype=np.uint8) * 255
    
    point_list = []
    unfilled_points = []
    for x in range(size):
        for y in range(size):
            unfilled_points.append([x, y])

    for _ in range(num_stones):
        if len(unfilled_points) == 0:
            break
        else:
            cx, cy = random.choice(unfilled_points)
            point_list.append([cx, cy])
            radius = stone_spacing
            
            filled_range = []
            for dy in range(int(-radius) - 1, int(radius + 1) + 1):
                for dx in range(int(-radius) - 1, int(radius + 1) + 1):
                    if dx**2 + dy**2 <= radius**2:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < size and 0 <= ny < size:
                            filled_range.append([nx, ny])
            
            for point in filled_range:
                if point in unfilled_points:
                    unfilled_points.remove(point)

    related_points = [[point] for point in point_list]
    border_points = {i: [point] for i, point in enumerate(point_list)}
    constant_borders = []
    while True:
        i = random.randint(0, len(point_list) - 1)
        borders = border_points[i]
        new_border_points = []
        for (bx, by) in borders:
            for nx, ny in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if 0 <= bx + nx < size and 0 <= by + ny < size:
                    if all([((bx + nx, by + ny) not in pixels_of_point) for pixels_of_point in related_points]):
                        related_points[i].append((bx + nx, by + ny))
                        new_border_points.append((bx + nx, by + ny))
                    elif (bx + nx, by + ny) not in related_points[i]:
                        constant_borders.append((bx + nx, by + ny))
        border_points[i] = new_border_points
        if all([(len(border_points[point_i]) == 0) for point_i in border_points]):
            break
    
    for _ in range(border_range):
        new_borders = []
        for bx, by in constant_borders:
            for nx, ny in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if (bx + nx, by + ny) not in constant_borders and 0 <= bx + nx < size and 0 <= by + ny < size:
                    new_borders.append((bx + nx, by + ny))
        constant_borders.extend(new_borders)
    
    # colors = {i: [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for i in range(len(point_list))}
    for index, point_batch in enumerate(related_points):
        for point in point_batch:
            image[point[0], point[1]] = [0, 0, 0]
    for point in point_list:
            image[point[0], point[1]] = [255, 255, 255]
    for point in constant_borders:
            image[point[0], point[1]] = [255, 255, 255]

    for x in range(size):
        for y in range(size):
            if list(image[x, y]) == [0, 0, 0]:
                color = random.randint(0, 75)
                for nx, ny in ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)):
                    if 0 <= x + nx < size and 0 <= y + ny < size:
                        image[x + nx, y + ny] = [color, color, color]

    img = Image.fromarray(image)
    blurred = img.filter(ImageFilter.GaussianBlur(radius=2))
    return blurred

random.seed()
# splatting(size=64, num_splats=45, splat_radius_lower=3, splat_radius_upper=8, blur_radius=4)
img = paving_stones(size=128, num_stones=20, stone_spacing=32, border_range=2)
normal_img = normal_map(img)
normal_img.show()
img.show()
