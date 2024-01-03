from flask import Flask, render_template
from flask_socketio import SocketIO
from pyfirmata import Arduino, util

app = Flask(__name__)
socketio = SocketIO(app)

board = Arduino('COM8')
it = util.Iterator(board)
it.start()

servoCbzaNo_pin = board.get_pin('d:6:s')
servoCbzaSi_pin = board.get_pin('d:5:s')

bzoder_pin = board.get_pin('d:8:o')
bzoizq_pin = board.get_pin('d:9:o')

vehiculo_pins = [board.get_pin('d:10:o'), board.get_pin('d:11:o'), board.get_pin('d:12:o'), board.get_pin('d:13:o')]

intervalo = 0.25
incrServoCbzaNo = 5
incrServoCbzaSi = 5
posServoCbzaNo = 90
posServoCbzaSi = 90
bzoder = 0
bzoizq = 0
cbz_no = 0
cbz_si = 0
cmdnvo = 64
cmdant = 64


@app.route('/')
def index():
    return render_template('mando_spectacular.html')


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('control')
def handle_control(data):
    global bzoder, bzoizq, cbz_no, cbz_si, cmdant

    cmdnvo = data['cmd']

    if cmdnvo != cmdant:
        paro()

    if cmdnvo == 'D':  # Avanza
        vehiculo(1, 0, 1, 0)
    elif cmdnvo == 'I':  # Reversa
        vehiculo(0, 1, 0, 1)
    elif cmdnvo == 'R':  # Vuelta a la derecha
        vehiculo(0, 1, 1, 0)
    elif cmdnvo == 'A':  # Vuelta a la izquierda
        vehiculo(1, 0, 0, 1)
    elif cmdnvo == 'Z':  # Brazo izquierdo
        toggle_brazo_izquierdo()
    elif cmdnvo == 'E':  # Brazo derecho
        toggle_brazo_derecho()
    elif cmdnvo == 'S':  # Cabeza SI
        toggle_cabeza_si()
    elif cmdnvo == 'N':  # Cabeza NO
        toggle_cabeza_no()
    else:
        paro()

    cmdant = cmdnvo


def toggle_brazo_izquierdo():
    global bzoizq

    bzoizq = 1 - bzoizq
    bzoizq_pin.write(bzoizq)


def toggle_brazo_derecho():
    global bzoder

    bzoder = 1 - bzoder
    bzoder_pin.write(bzoder)


def toggle_cabeza_si():
    global cbz_si

    cbz_si = 1 - cbz_si
    servoCbzaSi_pin.write(180 if cbz_si else 0)


def toggle_cabeza_no():
    global cbz_no, posServoCbzaNo, incrServoCbzaNo

    cbz_no = 1 - cbz_no

    if cbz_no:
        incrServoCbzaNo = 5

    posServoCbzaNo += incrServoCbzaNo

    if posServoCbzaNo == 150 or posServoCbzaNo == 30:
        incrServoCbzaNo *= -1

    servoCbzaNo_pin.write(posServoCbzaNo)


def vehiculo(a, b, c, d):
    vehiculo_pins[0].write(a)
    vehiculo_pins[1].write(b)
    vehiculo_pins[2].write(c)
    vehiculo_pins[3].write(d)


def paro():
    vehiculo(0, 0, 0, 0)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
