import numpy as np
from PIL import Image, ImageFilter
import random

def splatting(width, height, num_splats=30, splat_radius_lower=3, splat_radius_upper=6, blur_radius=3):
    image = np.ones((height, width, 3), dtype=np.uint8) * 255

    for _ in range(num_splats):
        cx = random.randint(0, width - 1)
        cy = random.randint(0, height - 1)
        radius = splat_radius_lower + random.random() * (splat_radius_upper - splat_radius_lower)

        for dy in range(int(-radius) - 1, int(radius + 1) + 1):
            for dx in range(int(-radius) - 1, int(radius + 1) + 1):
                if dx**2 + dy**2 <= radius**2:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        image[ny, nx] = [0, 0, 0]

    img = Image.fromarray(image)

    blurred = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    blurred.show()

random.seed()
splatting(width=64, height=64, num_splats=45, splat_radius_lower=3, splat_radius_upper=8, blur_radius=4)
