from flask import Flask, request, make_response
from tempfile import NamedTemporaryFile
import subprocess
import os

ip, port = "0.0.0.0", 8080

app = Flask(__name__)
app.debug = False

@app.route("/makepdf", methods=["POST"])
def make_pdf():

    if not request.data:
        return make_response("Bad Request", 400)

    orientation = "portrait"
    if request.args.get("orientation") in ["landscape", "portrait"]:
        orientation = request.args.get("orientation")

    html_temp = create_temp_file(".html", request.data)
    pdf_temp = create_temp_file(".pdf")

    cmd = ["wkhtmltopdf"]
    cmd.append("--dpi")
    cmd.append("100")
    cmd.append("--orientation")
    cmd.append(orientation.capitalize())
    cmd.append(html_temp.name)
    cmd.append(pdf_temp.name)

    try:
        process = subprocess.Popen(cmd)
        process.communicate()
    except Exception as e:
        return make_response("Error: %s" % (e.message), 500)

    response = make_response(pdf_temp.read(), 200)
    response.headers["Content-Type"] = "application/pdf"

    os.unlink(html_temp.name)
    os.unlink(pdf_temp.name)

    return response


def create_temp_file(file_suffix, html=None):
    tmp_file = NamedTemporaryFile(delete=False, suffix=file_suffix)
    if None != html:
        tmp_file.write(html)
        tmp_file.flush()
    return tmp_file


if __name__ == "__main__":
    app.run(ip, port)
