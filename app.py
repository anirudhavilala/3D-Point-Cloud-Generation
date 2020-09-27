import os
from flask import Flask, make_response, render_template, flash, request, redirect, url_for, send_from_directory, Request
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "uploads/"
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif' }

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = b'_flklmlfw\n.xwdw/'
PORT=8000


def allowed_file(filename):
        return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

@app.route('/', methods=['GET', 'POST'])
def upload_file():
        ID=0
        if request.method == 'POST':
                # check if the post request has the file part
                if 'files[]' not in request.files:
                        return 'Error: No file is chosen... Please upload a valid file. '

                files = request.files.getlist('files[]')
                outputDir = os.path.join(app.config['UPLOAD_FOLDER'], str(ID))
                outputID = str(ID)
                if not os.path.exists(outputDir):
                        os.mkdir(outputDir)
                        ID+=1
                for file in files:
                        if file and allowed_file(file.filename):
                                filename = secure_filename(file.filename)
                                # save images to file system
                                file.save(os.path.join(outputDir, filename))
                                
                os.system("ls {}".format(outputDir))                
                recon = os.system("python openMVG/openMVG_Build/software/SfM/SfM_GlobalPipeline.py {} {}".format(outputDir, outputDir+"/recon"))
                recon_ply = outputID+"/recon/reconstruction_global/colorized.ply"
                
                return render_template("result.html", image=recon_ply)
                        
        return '''
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>3D Model App</title>
        <body>
        <div class="container">
        <h1 class="display-4">3D Point Cloud Generation Tool</h1>
        <p class="lead">Take a few overlapping images of an object and upload them to get a 3D point cloud using structure from motion </p>
        <p>Accepted file extensions are: <b>jpg, jpeg, png, bmp, tif/tiff</b></p>
        <p><b>Note</b>: It might take a while to run 3D reconstruction on your images, so please be patient and only click upload once :)</p>
        <form method="post" action="/" enctype="multipart/form-data">
        <dl>
        <p>
        <input type="file" name="files[]" multiple="true" autocomplete="off" required>
        </p>
        </dl>
        <p>
        <input type="submit" value="Submit">
        </p>
        </form>
        </div>
        
        </body>
        '''

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=PORT, use_debugger=True)
