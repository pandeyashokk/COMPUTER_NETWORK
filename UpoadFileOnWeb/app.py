from flask import Flask, request, render_template_string

app = Flask(__name__)

upload_form = '''
<!doctype html>
<title>Upload File</title>
<h1>Upload a file (minimum size 10MB)</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and len(file.read()) >= 10 * 1024 * 1024:
            return 'File successfully uploaded'
        else:
            return 'File too small, please upload a file larger than 10MB'
    return render_template_string(upload_form)

if __name__ == '__main__':
    app.run(debug=True)
