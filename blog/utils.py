import math
import random
import re

from django.utils.html import strip_tags


def count_words(html_string):
    """Count the number of words in a blog post."""
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count


def get_read_time(html_string):
    """Calculate the reading time of a blog post."""
    count = count_words(html_string)
    read_time_min = math.ceil(count / 200.0)  # assuming 200wpm reading
    return int(read_time_min)


def generate_rgba_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = random.random()
    return f'rgba({r}, {g}, {b}, {a})'


def generate_rgb_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'rgba({r}, {g}, {b})'


def generate_3_backgrounds_colors():
    colors = []
    for i in range(3):
        colors.append(generate_rgba_color())
    properties = "background: " + colors[0] + "; background: radial-gradient(circle, " + colors[0] + " 0%, " + \
                 colors[1] + " 100%);"
    return properties
