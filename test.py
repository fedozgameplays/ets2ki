import numpy as np
import cv2
import time
from grab_screen import grabscreen
from get_keys import key_check
from inception_v3 import inception3
import directions
import os
import random


# window width
width = 960
# window height
height = 540
# Neural Network width
nn_width = 480
# Neural Network height
nn_height = 270
# learning rate of Neural Network (don't touch)
learning_rate = 1E-3
# output size of Neural Network
output_size = 9
# number of epochs for Neural Network (higher number=better, slower)
epochs = 5
# id of model, change if you want multiple
model_id = 1
# model name with id, learning rate and number of epochs
model_name = "model{}-{}_lr-{}_epochs".format(str(model_id),float(learning_rate), str(epochs))

# creating model with inception v3
model = inception3(int(nn_width), int(nn_height), float(learning_rate), output=int(output_size))
# load model
model.load(model_name)

# timer
for i in list(range(6))[::-1]:
    print(i+1)
    time.sleep(1)

# program paused or not
paused = False

while(True):
    if not paused:
        # record screen
        screen = grabscreen(region(0,30,int(width), int(height)+26))
        # resize screen to Neural Network width and height
        screen = cv2.resize(screen, (int(nn_width), int(nn_height)))
        # convert color from BGR to RGB
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        prediction = model.predict([screen.reshape(int(nn_width), int(nn_height), 3)])[0]
        prediction = np.array(prediction)
        choice = np.argmax(prediction)

        if choice == 0:
            directions.straight()
            choice_picked = "Geradeaus"
        elif choice == 1:
            directions.reverse()
            choice_picked = "Zurücksetzen"
        elif choice == 2:
            directions.left()
            choice_picked = "Links"
        elif choice == 3:
            directions.right()
            choice_picked = "Rechts"
        elif choice == 4:
            directions.straight_left()
            choice_picked = "Geradeaus + Links"
        elif choice == 5:
            directions.straight_right()
            choice_picked = "Geradeaus + Rechts"
        elif choice == 6:
            directions.reverse_left()
            choice_picked = "Zurücksetzen + Links"
        elif choice == 7:
            directions.reverse_right()
            choice_picked = "Zurücksetzen + Rechts"
        elif choice == 8:
            directions.release()
            choice_picked = "Nichts"

        print(choice_picked)

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
                directions.release()
                time.sleep(1)
        







