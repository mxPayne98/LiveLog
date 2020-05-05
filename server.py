from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO

from tail import Tail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret'
socket_io = SocketIO(app)

tf = Tail("data.log", socket_io)  # Path of log file to tail


@app.route("/log")
def render():
    return render_template('index.html')


@socket_io.on('connected')
def handle_log(json):
    print('received msg: ' + str(json))
    tf.tail()
    thread = Thread(target=tf.follow)
    thread.start()


if __name__ == '__main__':
    socket_io.run(app, port=5000)
