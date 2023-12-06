#! /usr/bin/env python3
# vim:fenc=utf-8
import numpy as np
from PIL import Image


def to_img(x, scale_up=10):
    x = np.uint8(x / x.max() * 255)

    img = np.empty((x.shape[0], x.shape[1] * scale_up, x.shape[2] * scale_up), dtype=np.uint8)

    for color in range(x.shape[0]):
        for row in range(x.shape[1]):
            for col in range(x.shape[2]):
                pixel = x[color][row][col]
                new_row = row * scale_up
                new_col = col * scale_up
                img[
                    color, 
                    new_row : new_row + scale_up, 
                    new_col : new_col + scale_up
                ] = pixel
    return Image.fromarray(img.squeeze())
