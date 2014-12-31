from flask import Flask, request, make_response
from tempfile import NamedTemporaryFile
from wkhtmltopdf import wkhtmltopdf
import os

ip, port = "0.0.0.0", 8080

app = Flask(__name__)
app.debug = False

@app.route("/ping", methods=["GET"])
def ping():
    return "PONG!"


@app.route("/makepdf", methods=["POST"])
def make_pdf():

    if not request.data:
        return make_response("Bad Request", 400)

    orientation = "portrait"
    if request.args.get("orientation") in ["landscape", "portrait"]:
        orientation = request.args.get("orientation")

    html_temp = create_temp_file(".html", request.data)
    pdf_temp = create_temp_file(".pdf")

    try:
        wkhtmltopdf(html_temp.name, pdf_temp.name, dpi=100, orientation=str(orientation.capitalize()),)
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
