import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import pyfirmata

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

board = None
servoCbzaNo = None
servoCbzaSi = None

incrServoCbzaNo = 5
incrServoCbzaSi = 5

milisActual = 0
milisAnterior = 0

intervalo = 250

posServoCbzaNo = 90
posServoCbzaSi = 90

bzoder = False
bzoizq = False

cbz_no = False
cbz_si = False

cmdnvo = 64
cmdant = 64

def vehiculo(a, b, c, d):
    board.digital[10].write(a)
    board.digital[11].write(b)
    board.digital[12].write(c)
    board.digital[13].write(d)

def paro():
    vehiculo(0, 0, 0, 0)
    time.sleep(0.05)

@app.route('/')
def index():
    return render_template('inicio.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('command')
def handle_command(command):
    global bzoder, bzoizq, cbz_no, cbz_si, cmdnvo, cmdant

    if command == 'D':  # Avanza
        if command != cmdant:
            paro()
        vehiculo(1, 0, 1, 0)

    elif command == 'I':  # Reversa
        if command != cmdant:
            paro()
        vehiculo(0, 1, 0, 1)

    elif command == 'R':  # Vuelta a la derecha
        if command != cmdant:
            paro()
        vehiculo(0, 1, 1, 0)

    elif command == 'A':  # Vuelta a la izquierda
        if command != cmdant:
            paro()
        vehiculo(1, 0, 0, 1)

    elif command == 'Z':  # Brazo izquierdo
        time.sleep(0.1)
        if not bzoizq:
            board.digital[9].write(1)
            bzoizq = True
        else:
            board.digital[9].write(0)
            bzoizq = False

    elif command == 'E':  # Brazo derecho
        time.sleep(0.1)
        if not bzoder:
            board.digital[8].write(1)
            bzoder = True
        else:
            board.digital[8].write(0)
            bzoder = False

    elif command == 'S':  # Cabeza SI
        time.sleep(0.1)
        if not cbz_si:
            board.digital[7].write(1)
            cbz_si = True
        else:
            board.digital[7].write(0)
            cbz_si = False

    elif command == 'N':  # Cabeza NO
        time.sleep(0.1)
        board.digital[6].write(1)
        time.sleep(0.1)
        board.digital[6].write(0)

    else:  # Desactivar las salidas
        paro()

    cmdant = cmdnvo

def servo_cbza_no():
    global posServoCbzaNo, incrServoCbzaNo, cbz_no, milisActual, milisAnterior

    if cbz_no:
        milisActual = int(round(time.time() * 1000))
        if milisActual - milisAnterior > intervalo:
            posServoCbzaNo += incrServoCbzaNo
            if posServoCbzaNo == 150 or posServoCbzaNo == 30:
                incrServoCbzaNo *= -1
            servoCbzaNo.write(posServoCbzaNo)
            milisAnterior = milisActual

def servo_cbza_si():
    global posServoCbzaSi, incrServoCbzaSi, cbz_si, milisActual, milisAnterior

    if cbz_si:
        milisActual = int(round(time.time() * 1000))
        if milisActual - milisAnterior > intervalo:
            posServoCbzaSi += incrServoCbzaSi
            if posServoCbzaSi == 150 or posServoCbzaSi == 30:
                incrServoCbzaSi *= -1
            servoCbzaSi.write(posServoCbzaSi)
            milisAnterior = milisActual

def setup():
    global board, servoCbzaNo, servoCbzaSi

    board = pyfirmata.Arduino('COM10')
    iter8 = pyfirmata.util.Iterator(board)
    iter8.start()

    board.digital[6].mode = pyfirmata.SERVO
    board.digital[7].mode = pyfirmata.SERVO
    board.digital[8].mode = pyfirmata.OUTPUT
    board.digital[9].mode = pyfirmata.OUTPUT
    board.digital[10].mode = pyfirmata.OUTPUT
    board.digital[11].mode = pyfirmata.OUTPUT
    board.digital[12].mode = pyfirmata.OUTPUT
    board.digital[13].mode = pyfirmata.OUTPUT

    servoCbzaNo = board.digital[6]
    servoCbzaSi = board.digital[7]

if __name__ == '__main__':
    setup()
    socketio.run(app, host='0.0.0.0', port=5000)