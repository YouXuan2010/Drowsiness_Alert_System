from threading import Thread
import keyboard,serial
import cv2
from keras.models import load_model
import numpy as np
from pygame import mixer


def controller():
    global drowsy
    drowsy=0
    ser = serial.Serial('COM8', 9600)
    while True:
        if drowsy==1:
            ser.write(b'x')
        elif keyboard.is_pressed('w'):
            ser.write(b'f')
        elif keyboard.is_pressed("s"):
            ser.write(b'b')
        elif keyboard.is_pressed("d"):
            ser.write(b'r')
        elif keyboard.is_pressed("a"):
            ser.write(b'l')
        else:
            ser.write(b's')

def cam():
    global drowsy
    drowsy=0
    threshold = 0.4

    mixer.init()
    # Load audio file
    mixer.music.load('alarm.wav')
    # Set preferred volume
    # mixer.music.set_volume(0.2)

    face = cv2.CascadeClassifier('haar cascade files\haarcascade_frontalface_alt.xml')
    leye = cv2.CascadeClassifier('haar cascade files\haarcascade_lefteye_2splits.xml')
    reye = cv2.CascadeClassifier('haar cascade files\haarcascade_righteye_2splits.xml')

    model = load_model('models/cnncat2.h5')
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    count = 0
    rpred = [[0,1]]
    lpred = [[0,1]]
    while (True):

        ret, frame = cap.read()
        height, width = frame.shape[:2]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face.detectMultiScale(gray, minNeighbors=5, scaleFactor=1.1, minSize=(25, 25))
        left_eye = leye.detectMultiScale(gray)
        right_eye = reye.detectMultiScale(gray)

        cv2.rectangle(frame, (0, height - 50), (200, height), (0, 0, 0), thickness=cv2.FILLED)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (100, 100, 100), 1)

        for (x, y, w, h) in right_eye:
            r_eye = frame[y:y + h, x:x + w]
            count = count + 1
            r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
            r_eye = cv2.resize(r_eye, (24, 24))
            r_eye = r_eye / 255
            r_eye = r_eye.reshape(24, 24, -1)
            r_eye = np.expand_dims(r_eye, axis=0)
            rpred = model.predict(r_eye)
            if (rpred[0][1] > threshold):
                lbl = 'Open'
            else:
                lbl = 'Closed'
            break

        for (x, y, w, h) in left_eye:
            l_eye = frame[y:y + h, x:x + w]
            count = count + 1
            l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
            l_eye = cv2.resize(l_eye, (24, 24))
            l_eye = l_eye / 255
            l_eye = l_eye.reshape(24, 24, -1)
            l_eye = np.expand_dims(l_eye, axis=0)
            lpred = model.predict(l_eye)
            if (lpred[0][1] > threshold):
                lbl = 'Open'
            else:
                lbl = 'Closed'
            break

        if (lpred[0][1] > threshold and rpred[0][1] > threshold):
            cv2.putText(frame, "Open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            count = 0
            mixer.music.stop()
        else:
            cv2.putText(frame, "Closed", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            if count >= 8:
                drowsy=1
                try:
                    mixer.music.play()
                except:  # isplaying = False
                    pass
            else:
                drowsy=0

        cv2.imshow('frame', frame)
        #print(count)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":

    p1 = Thread(target=controller)
    p2 = Thread(target=cam)
    p1.start()
    p2.start()


