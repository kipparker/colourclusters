import logging
import typing

from sklearn.cluster import KMeans
from PIL import Image
import numpy as np

import models


def get_pixels(fp: typing.BinaryIO):
    """Get a numpy array of an image"""
    image = Image.open(fp, "r")
    width, height = image.size
    smaller_width = 600
    smaller_height = int(smaller_width * (height / width))
    print((smaller_width, smaller_height))
    image = image.resize((smaller_width, smaller_height))
    raw_values = list(image.getdata())
    if image.mode == "RGB":
        channels = 3
    elif image.mode == "L":
        channels = 1
    else:
        logging.info("Unknown mode: %s" % image.mode)
        return None
    return np.array(raw_values).reshape((smaller_width * smaller_height, channels))


def get_colour_values(pixels: list, clusters: int = 5) -> list[dict[str, int]]:
    cluster = KMeans(n_clusters=clusters).fit(pixels)
    # Get the number of different clusters, create histogram, and normalize
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins=labels)
    hist = hist.astype("float")
    hist /= hist.sum()
    # Create frequency rect and iterate through each cluster's colour and percentage
    colours = sorted(
        [
            {"percentage": percent, "colour": [int(c) for c in colour]}
            for (percent, colour) in zip(hist, cluster.cluster_centers_)
        ],
        key=lambda d: d["percentage"],
        reverse=True,
    )
    return colours
