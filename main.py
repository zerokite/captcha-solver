from ast import arg
from flask import Flask 
from flask_restful import Api, Resource, reqparse
import cv2
from paddleocr import PaddleOCR
ocr = PaddleOCR(lang='en')

app = Flask(__name__)
api = Api(app)

url_post_args = reqparse.RequestParser()
url_post_args.add_argument("url", type=str, help="Expecting a string")


def captcha_recognition(url):
    gif = cv2.VideoCapture(url)
    ret, frame = gif.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gif.release()
    captcha = ocr.ocr(gray, det=False, cls=False)
    return captcha[0][0][:4]

class Solver(Resource):
    def get(self):
        return {"data":"Hello World"}

    def post(self):
        args = url_post_args.parse_args()
        return captcha_recognition(args['url'])

api.add_resource(Solver, "/captchasolve")

if __name__ == "__main__":
    app.run(debug=True)

