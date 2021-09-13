from app import app
from flask import request, render_template, url_for
import os
import cv2
import numpy as np
from PIL import Image
import random
import string
import pytesseract

app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        full_filename = 'images/white_bg.jpg'
        return render_template("index.html", full_filename=full_filename)

    if request.method == "POST":
        image_upload = request.files['image_upload']
        imagename = image_upload.filename
        image = Image.open(image_upload)

        image_arr = np.array(image.convert('RGB'))
        gray_img_arr = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
        tresh = cv2.threshold(gray_img_arr, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        image = Image.fromarray(tresh)

        letters = string.ascii_lowercase
        name = ''.join(random.choice(letters) for i in range(10)) + '.png'
        full_filename = 'uploads/' + name

        custom_config = r'-l eng --oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)

        characters_to_remove = "!()@—*“”>+-/\,'|£#%¥$&^_~©?"
        new_string = text
        for character in characters_to_remove:
            new_string = new_string.replace(character, "")

        new_string = new_string.split("\n")

        img = Image.fromarray(image_arr, 'RGB')
        img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))
        return render_template('index.html', full_filename=full_filename, text=new_string)


if __name__ == '__main__':
    app.run(debug=True)
