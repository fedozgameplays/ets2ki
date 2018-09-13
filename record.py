import numpy as np
import cv2
from grab_screen import grabscreen
from get_keys import key_check
import os
import time

startpoint = 1

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nokey = [0,0,0,0,0,0,0,0,1]

# window width
width = 1280
# window height
height = 720
# Neural Network width
nn_width = 480
# Neural Network height
nn_height = 270


while True:
    # specify filename with startpoint
    filename = "trainingsdaten-{}.npy".format(startpoint)
    # check if file exists
    if os.path.isfile(filename):
        print("Trainingsdaten existieren bereits, lade vorhandene Daten... (%s)" % (str(startpoint)))
        # file exists, increase startpoint by 1
        startpoint = int(startpoint)+1
    else:
        # file does not exist, moving along
        print("Keine Trainingsdaten existieren.")
        break

def key_output(keys):
        #[W,A,S,D,WA,WD,SA,SD,nokey]
        # output array
        output = [0,0,0,0,0,0,0,0,0]
        if "W" in keys and "A" in keys:
            output = wa
        elif "W" in keys and "D" in keys:
            output = wd
        elif "S" in keys and "A" in keys:
            output = sa
        elif "S" in keys and "D" in keys:
            output = sd
        elif "W" in keys:
            output = w
        elif "S" in keys:
            output = s
        elif "A" in keys:
            output = a
        elif "D" in keys:
            output = d
        else:
            output = nokey

        return output


def main(filename, startpoint):
    filename = filename
    startpoint = startpoint
    # clear training data
    training_data = []

    # timer for program start
    for i in list(range(6))[::-1]:
        print(i+1)
        time.sleep(1)

    # program paused or not
    paused = False

    while(True):
        if not paused:
            # record screen
            screen = grabscreen(region=(0,30,int(width), int(height)+26))
            # resize screen to Neural Network width and height
            screen = cv2.resize(screen, (int(nn_width), int(nn_height)))
            # convert color from BGR to RGB
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            
            # check which keys are being pressed
            keys = key_check()
            # return output of pressed keys
            output = key_output(keys)
            # add image and pressed keys to data
            training_data.append([screen, output])

            if len(training_data) % 100 == 0:
                # print length of training data
                print("Länge der Trainingsdaten: "+str(len(training_data)))

                if len(training_data) == 500:
                    # save training data to file
                    print("Länge: "+str(len(training_data)) + ", speichere...")
                    np.save(filename, training_data)
                    # clear training data
                    training_data = []
                    # increase startpoint by 1
                    startpoint = int(startpoint) + 1
                    # modify filename with changed startpoint
                    filename = "trainingsdaten-{}.npy".format(startpoint)

        # check which keys are being pressed           
        keys=key_check()

        # check if t is being pressed
        if 'T' in keys:
            if paused:
                # if paused, unpause
                paused = False
                time.sleep(1)
            else:
                # if running, pause
                paused = True
                time.sleep(1)

# call main function
main(filename, startpoint)
                

