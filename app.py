from flask import Flask, render_template, request, send_file
import img2pdf
import os
import glob
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/PDF', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            file.save(f"images/{file.filename}")
    converter()
    return render_template('download.html')


@app.route('/download')
def downloadFile():
    dir = os.path.abspath(os.curdir)
    path = f"{dir}/output.pdf"
    return send_file(path, as_attachment=True)


def converter():
    dirname = 'images'
    with open("output.pdf", "wb") as f:
        imgs = []
        for fname in os.listdir(dirname):
            if not fname.endswith(".jpg"):
                continue
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                continue
            imgs.append(path)
        f.write(img2pdf.convert(imgs))
    delete_images()


def delete_images():
    files = glob.glob('images/*.jpg')
    for f in files:
        os.remove(f)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
