from flask import Flask
app = Flask(__name__)

@app.route ("/")
def hello_w():
    return ("Hello najlaa! you are awesome .. yay")

if __name__ == "__main__":
    app.run(host= '0.0.0.0', debug=True)



