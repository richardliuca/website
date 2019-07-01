from flask import current_app
from werkzeug.utils import secure_filename
import os, uuid
import os.path as path
from PIL import Image as Pillow_Image
from functools import reduce

def allowed_file(filename):

    if '.' in filename:
        name, ext = path.splitext(filename)
        return ext[1:].lower() in current_app.config['ALLOWED_EXTENSIONS']
    return False

def file_upload_handler(file_object, upload_path):

    if file_object and allowed_file(file_object.filename):
        filename, ext = path.splitext(secure_filename(file_object.filename))
        unique_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, filename))
        file_path = path.join(current_app.instance_path,
                            upload_path,
                            unique_name + ext)
        return file_path
    else:
        return False

multiply = lambda a, b: a*b

def euclid_algorithm(num1, num2):
    if num1 == num2:
        return num1
    elif num1 > num2:
        return euclid_algorithm(num2, num1 - num2)
    else:
        return euclid_algorithm(num1, num2 - num1)

def largest_cut(current_size, limit):
    next_size = tuple(map(lambda num: num*2, current_size))
    if reduce(multiply, next_size) > reduce(multiply, limit):
        return current_size
    return largest_cut(next_size, limit)

def image_resize(image, max_size):
    image = Pillow_Image.open(image)
    current_size = image.size
    if reduce(multiply, current_size) > reduce(multiply, max_size):
        gcd = euclid_algorithm(max_size[0], max_size[1])
        target_ratio = tuple(map(lambda num: num/gcd, max_size))
        trim_size = largest_cut(target_ratio, current_size)

        x_diff = (current_size[0] - trim_size[0])/2
        y_diff = (current_size[1] - trim_size[1])/2
        boundary = (0+x_diff, 0+y_diff,
                    current_size[0]-x_diff, current_size[1]-y_diff)
        image = image.crop(boundary)
        return image.resize(max_size)
    return image
