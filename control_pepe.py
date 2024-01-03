import time
import pyfirmata
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

board = None

# Configuración de pines y variables
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

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('command')
def handle_command(cmd):
    global cmdnvo, cmdant, bzoder, bzoizq, cbz_no, cbz_si

    cmdnvo = ord(cmd)

    if cmdnvo != cmdant:
        paro()

    if cmdnvo == ord('D'):  # Avanza
        vehiculo(True, False, True, False)
    elif cmdnvo == ord('I'):  # Reversa
        vehiculo(False, True, False, True)
    elif cmdnvo == ord('R'):  # Vuelta a la derecha
        vehiculo(False, True, True, False)
    elif cmdnvo == ord('A'):  # Vuelta a la izquierda
        vehiculo(True, False, False, True)
    elif cmdnvo == ord('Z'):  # Brazo izquierdo
        toggle_brazo_izquierdo()
    elif cmdnvo == ord('E'):  # Brazo derecho
        toggle_brazo_derecho()
    elif cmdnvo == ord('S'):  # Cabeza SI
        toggle_cabeza_si()
    elif cmdnvo == ord('N'):  # Cabeza NO
        toggle_cabeza_no()
    else:  # Desactivar las salidas
        paro()

    cmdant = cmdnvo

def vehiculo(a, b, c, d):
    board.digital[10].write(a)
    board.digital[11].write(b)
    board.digital[12].write(c)
    board.digital[13].write(d)

def paro():
    vehiculo(False, False, False, False)
    time.sleep(0.05)

def toggle_brazo_izquierdo():
    global bzoizq

    bzoizq = not bzoizq
    board.digital[9].write(bzoizq)

def toggle_brazo_derecho():
    global bzoder

    bzoder = not bzoder
    board.digital[8].write(bzoder)

def toggle_cabeza_si():
    global cbz_si

    cbz_si = not cbz_si
    board.digital[7].write(cbz_si)

def toggle_cabeza_no():
    global cbz_no

    cbz_no = not cbz_no
    if cbz_no:
        servoCbzaNo.write(150)
    else:
        servoCbzaNo.write(30)

def servo_cbza_no():
    global posServoCbzaNo, incrServoCbzaNo, milisActual, milisAnterior

    if cbz_no:
        milisActual = int(round(time.time() * 1000))
        if milisActual - milisAnterior > intervalo:
            posServoCbzaNo += incrServoCbzaNo
            if posServoCbzaNo == 150 or posServoCbzaNo == 30:
                incrServoCbzaNo *= -1
            servoCbzaNo.write(posServoCbzaNo)
            milisAnterior = milisActual

def servo_cbza_si():
    global posServoCbzaSi, incrServoCbzaSi, milisActual, milisAnterior

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

    board = pyfirmata.Arduino('COM10')  # Cambiar 'COM8' según el puerto en el que esté conectado el Arduino

    it = pyfirmata.util.Iterator(board)
    it.start()

    servoCbzaNo = board.get_pin('d:6:s')
    servoCbzaSi = board.get_pin('d:5:s')

if __name__ == '__main__':
    setup()
    socketio.run(app, host='0.0.0.0', port=5000)