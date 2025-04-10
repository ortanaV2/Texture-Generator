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

def paving_stones(size, num_stones=10, stone_radius=3):
    image = np.ones((size, size, 3), dtype=np.uint8) * 255
    cell_amount = round(math.sqrt(num_stones))  # cells per side
    cell_size = round(size / math.sqrt(num_stones), 3)
    point_list = []
    for cell_x in range(cell_amount):
        for cell_y in range(cell_amount):
            image[int(cell_x * cell_size + cell_size) - 1, :] = [255, 0, 0]
            image[:, int(cell_x * cell_size + cell_size) - 1] = [255, 0, 0]
            point = (int(random.uniform(0, cell_size) + cell_x * cell_size), int(random.uniform(0, cell_size) + cell_y * cell_size))
            point_list.append(point)
            image[int(point[0]), int(point[1])] = [0, 0, 0]
    
    related_points = [[point] for _ in point_list]
    border_points = [[point] for point in point_list]
    while True:
        print(border_points)
        for i, borders in enumerate(border_points):
            new_border_points = []
            for (bx, by) in borders:
                for nx, ny in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    if all([((bx + nx, by + ny) not in pixels_of_point) for pixels_of_point in related_points]) and 0 <= bx + nx < size and 0 <= by + ny < size:
                        related_points[i].append((bx + nx, by + ny))
                        new_border_points.append((bx + nx, by + ny))
            border_points[i] = new_border_points
        if all([(len(borders_of_point) == 0) for borders_of_point in border_points]):
            break
    
    print(related_points)

    img = Image.fromarray(image)
    img.show()

random.seed()
# splatting(size=64, num_splats=45, splat_radius_lower=3, splat_radius_upper=8, blur_radius=4)
paving_stones(4, 4)
