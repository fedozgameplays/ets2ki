import numpy as np
from inception_v3 import inception3
from random import shuffle
import os

# window width
width = 1280
# window height
height = 720
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
# batch-size of Neural Network
batchsize = 32
# ammount of training files
file_end = 57
# id of model, change if you want multiple
model_id = 1
# model name with id, learning rate and number of epochs
model_name = "model{}-{}_lr-{}_epochs".format(str(model_id),float(learning_rate), str(epochs))

# creating model with inception v3
model = inception3(int(nn_width), int(nn_height), float(learning_rate), output=int(output_size))

for e in range(int(epochs)):
    # order for all training files
    data_order = [i for i in range(1,file_end+1)]
    # shuffleing order of training files
    shuffle(data_order)

    for count, i in enumerate(data_order):
        try:
            # change filename to pass in for loop
            filename = "trainingsdaten-{}.npy".format(i)
            # load training data
            training_data = np.load(filename)
            print("Daten werden geladen: %s, Länge: %s" % (dateiname,str(len(trainingsdaten))))

            # splitting train and test data
            train = training_data[:-50]
            # first 50 test
            test = training_data[-50:]
            print("Länge train: %s" % (len(train)))
            print("Länge test: %s" % (len(test)))

            # creating x tensor
            x = np.array([i[0] for i in train]).reshape(-1, int(nn_width), int(nn_height), 3)
            # creating y tensor
            y = [i[1] for i in train]
            # creating x validation tensor
            test_x = np.array([i[0] for i in test]).reshape(-1, int(nn_width), int(nn_height), 3)
            # creating y validation tensor
            test_y = [i[1] for i in test]

            # train model
            model.fit({"input": x}, {"targets": y}, n_epoch=1,
                          validation_set=({"input": test_x}, {"targets": test_y}),
                          snapshot_step=2500, show_metric=False, run_id=model_name, batch_size=batchsize)
            
            if count%10 == 0:
                    print("Model wird gespeichert...")
                    # save model
                    model.save(model_name)
                    
        except Exception as e:
                print(str(e))
                
    # save model
    model.save(model_name)
            


