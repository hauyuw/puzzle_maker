import os
import stl_tools
from pylab import imread
import numpy as np
from scipy.ndimage import gaussian_filter

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

HOME_DIRECTORY = '/home/hauyuw/puzzle_maker/' #include directory path for your webserver here
STATIC_FOLDER = HOME_DIRECTORY+'/static/img/'
UPLOAD_FOLDER = HOME_DIRECTORY+'/uploads/'
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():        
    return render_template('index.html')

@app.route('/home')
def home():        
    return render_template('index.html')

@app.route('/puzzle', methods=['GET','POST'])
def gallery():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            noextension = os.path.splitext(filename)[0]
            return redirect(url_for('make_puzzle_from_img',
                                    filename=noextension))
        else: return "file not allowed"
        
    return render_template('puzzle.html')

@app.route('/make_gallery_puzzle/<filename>')
def make_puzzle_from_gallery(filename):
    HEIGHT_MULTIPLER = 512
    HEIGHT_BASE = 128
    new_img = STATIC_FOLDER+str(filename)+'.png'

    # load the user image as a MxNx4 (rgba) numpy array
    user_img = imread(new_img)
    user_img = gaussian_filter(user_img, 2)  # smoothing
    # use the red and blue channels with equal weight to make greyscale levels
    user_img_grey = (0.5*user_img[:,:,2]) + (0.5*user_img[:,:,0])
    # invert the greyscale values so white is lowest height
    user_img_ones = np.ones( (len(user_img), len(user_img[0])) )
    user_img_inv = user_img_ones - user_img_grey
    # convert 0.0-1.0 float levels to 8-bit 0-255 levels
    # also add a fixed offset so we always have a base piece
    user_img_8bit = (HEIGHT_MULTIPLER * user_img_inv) + HEIGHT_BASE

    # load a mask for the puzzle pieces where black zeros the surface height
    mask_img = imread(STATIC_FOLDER+'fitted4x4template-500x500.png')
    mask_img_grey = (0.5*mask_img[:,:,2]) + (0.5*mask_img[:,:,0])

    C = user_img_8bit * mask_img_grey

    finalname = filename+'.stl'
    stl_tools.numpy2stl(C, finalname, scale=0.05, mask_val=5., max_width=100, max_depth=100, max_height=130, solid=True)
    return render_template('puzzle_done.html', filename=filename)

@app.route('/make_puzzle/<filename>')
def make_puzzle_from_img(filename):
    HEIGHT_MULTIPLER = 512
    HEIGHT_BASE = 128
    new_img = UPLOAD_FOLDER+str(filename)+'.png'

    # load the user image as a MxNx4 (rgba) numpy array
    user_img = imread(new_img)
    user_img = gaussian_filter(user_img, 2)  # smoothing
    # use the red and blue channels with equal weight to make greyscale levels
    user_img_grey = (0.5*user_img[:,:,2]) + (0.5*user_img[:,:,0])
    # invert the greyscale values so white is lowest height
    user_img_ones = np.ones( (len(user_img), len(user_img[0])) )
    user_img_inv = user_img_ones - user_img_grey
    # convert 0.0-1.0 float levels to 8-bit 0-255 levels
    # also add a fixed offset so we always have a base piece
    user_img_8bit = (HEIGHT_MULTIPLER * user_img_inv) + HEIGHT_BASE

    # load a mask for the puzzle pieces where black zeros the surface height
    mask_img = imread(STATIC_FOLDER+'fitted4x4template-500x500.png')
    mask_img_grey = (0.5*mask_img[:,:,2]) + (0.5*mask_img[:,:,0])

    C = user_img_8bit * mask_img_grey

    finalname = filename+'.stl'
    stl_tools.numpy2stl(C, finalname, scale=0.05, mask_val=5., max_width=100, max_depth=100, max_height=130, solid=True)
    return render_template('puzzle_done.html', filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(debug=True)
