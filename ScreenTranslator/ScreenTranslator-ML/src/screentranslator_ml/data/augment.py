from __future__ import annotations
import io
import random
from typing import Callable
import numpy as np
from PIL import Image, ImageFilter


class RecognizerAugment:

    def __init__(self, seed: int | None = None, jpeg_prob: float = 0.3, blur_prob: float = 0.25):
        self.rng = random.Random(seed)
        self.jpeg_prob = jpeg_prob
        self.blur_prob = blur_prob

    def __call__(self, img: Image.Image) -> Image.Image:
        if self.rng.random() < self.blur_prob:
            img = img.filter(ImageFilter.GaussianBlur(radius=self.rng.uniform(0.3, 1.0)))
        if self.rng.random() < self.jpeg_prob:
            buf = io.BytesIO()
            img.convert("RGB").save(buf, format="JPEG", quality=self.rng.randint(65, 95))
            buf.seek(0)
            img = Image.open(buf).convert("L")
        return img


class DetectorAugment:

    def __init__(self, seed: int | None = None, rot_deg: float = 5.0, crop_frac: float = 0.9):
        self.rng = random.Random(seed)
        self.rot_deg = rot_deg
        self.crop_frac = crop_frac

    def __call__(self, img: Image.Image, polys: list[list[list[float]]]) -> tuple[Image.Image, list[list[list[float]]]]:
        if self.rng.random() < 0.5:
            angle = self.rng.uniform(-self.rot_deg, self.rot_deg)
            img = img.rotate(angle, resample=Image.BILINEAR, expand=False, fillcolor=(230, 230, 230))
            cx, cy = img.size[0] / 2, img.size[1] / 2
            rad = np.deg2rad(-angle)
            cos_a, sin_a = np.cos(rad), np.sin(rad)
            new_polys = []
            for poly in polys:
                new_poly = []
                for x, y in poly:
                    dx, dy = x - cx, y - cy
                    nx = cx + dx * cos_a - dy * sin_a
                    ny = cy + dx * sin_a + dy * cos_a
                    new_poly.append([nx, ny])
                new_polys.append(new_poly)
            polys = new_polys
        return img, polys
