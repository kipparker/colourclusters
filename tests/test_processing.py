import io

from PIL import Image, ImageDraw
import numpy as np
import processing


def two_colour_image(colour1=(255, 0, 0), colour2=(0, 255, 0), width=20, height=10):
    img = Image.new("RGB", (width, height), color=colour1)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, width / 2, height), fill=colour2)
    bytes_like = io.BytesIO()
    img.save(bytes_like, format="png")
    return bytes_like


def test_get_pixels():
    width = 600
    height = 300
    colour1 = (255, 0, 0)
    colour2 = (0, 255, 0)
    im = two_colour_image(colour1, colour2, width=width, height=height)
    result = processing.get_pixels(im)
    expected_size = (
        600 * (600 * (height / width)) * 3
    )  # resizes and splits into three channels
    assert result.size == expected_size
    colours = np.unique(result, axis=0, return_counts=True)
    assert tuple(colours[0][0]) == colour2
    assert tuple(colours[0][1]) == colour1


def test_get_colour_values():
    test_clusters = [
        [0, 0, 0],
        [255, 255, 0],
        [255, 255, 0],
        [255, 255, 0],
        [255, 255, 0],
    ]
    result = processing.get_colour_values(np.array(test_clusters))
    assert result[0]["percentage"] == 0.8
    assert result[1]["percentage"] == 0.2
