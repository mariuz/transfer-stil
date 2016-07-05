import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory

import numpy as np
import scipy.misc

from stylize import stylize

import math

# default arguments
CONTENT_WEIGHT = 5e0
STYLE_WEIGHT = 1e2
TV_WEIGHT = 1e2
LEARNING_RATE = 1e1
STYLE_SCALE = 1.0
ITERATIONS = 1000
VGG_PATH = 'imagenet-vgg-verydeep-19.mat'
initial = None

UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output'
STYLE_FOLDER ='./examples'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STYLE_FOLDER'] = STYLE_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('process_file',
                                    filename=filename,style='1-style.jpg'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/process/<filename>')
@app.route('/process/<filename>/<style>')
def process_file(filename, style = None):

    content_image = imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    style_images = [imread(os.path.join(app.config['STYLE_FOLDER'], style))]

    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


    target_shape = content_image.shape
    for i in range(len(style_images)):
        style_scale = STYLE_SCALE
        style_images[i] = scipy.misc.imresize(style_images[i], style_scale *
                target_shape[1] / style_images[i].shape[1])

        # default is equal weights
    style_blend_weights = [1.0/len(style_images) for _ in style_images]

    for iteration, image in stylize(
        network=VGG_PATH,
        initial=initial,
        content=content_image,
        styles=style_images,
        iterations=ITERATIONS,
        content_weight=STYLE_WEIGHT,
        style_weight=STYLE_WEIGHT,
        style_blend_weights=style_blend_weights,
        tv_weight=TV_WEIGHT,
        learning_rate=LEARNING_RATE,
        print_iterations=None,
        checkpoint_iterations=None
    ):
        output_file = app.config['OUTPUT_FOLDER'], filename
        imsave(output_file, image)


    return send_from_directory(app.config['OUTPUT_FOLDER'],
                               filename)

def imread(path):
    return scipy.misc.imread(path).astype(np.float)


def imsave(path, img):
    img = np.clip(img, 0, 255).astype(np.uint8)
    scipy.misc.imsave(path, img)
