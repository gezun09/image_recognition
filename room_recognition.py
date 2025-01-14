# -*- coding: utf-8 -*-
"""room_recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/gezun09/e405b6bc6907f42665d8ed4eb352c64c/room_recognition.ipynb
"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np

from google.colab import drive
drive.mount('/content/drive/')

img = image.load_img("/content/drive/MyDrive/sui/image_recognition/gyarab/bufet/IMG_20220614_074927_BURST1.jpg")
plt.imshow(img)

train = ImageDataGenerator(rescale = 1/225)
valid = ImageDataGenerator(rescale = 1/225)

training_dataset = train.flow_from_directory('/content/drive/MyDrive/sui/image_recognition/gyarab', ##rozdeleni fotek podle slozek na classes
                                            target_size=(200,200),
                                            batch_size=3, 
                                            class_mode = 'categorical')

validation_dataset = train.flow_from_directory('/content/drive/MyDrive/sui/image_recognition/gyarab', 
                                           target_size=(200,200),
                                           batch_size=3,
                                           class_mode = 'categorical')

training_dataset.class_indices

training_dataset.classes

model = tf.keras.models.Sequential([ tf.keras.layers.Conv2D(16, (3,3), activation = 'relu', input_shape=(200,200,3)),
                                   tf.keras.layers.MaxPool2D(2,2),
                                   
                                   tf.keras.layers.Conv2D(32, (3,3), activation = 'relu'),
                                   tf.keras.layers.MaxPool2D(2,2),
                                    
                                   tf.keras.layers.Conv2D(64, (3,3), activation = 'relu'),
                                   tf.keras.layers.MaxPool2D(2,2),
                                    
                                   tf.keras.layers.Flatten(),
                                    
                                   tf.keras.layers.Dense(512, activation = 'relu'),
                                    
                                   tf.keras.layers.Dense(1, activation = 'sigmoid')
                                   ])

model.compile(loss = 'categorical_crossentropy',
             optimizer = RMSprop(learning_rate=0.001),
             metrics = ['accuracy'])

model_fit = model.fit(training_dataset,
                     steps_per_epoch = 7,
                     epochs = 20,
                     validation_data=validation_dataset)

dir_path = '/content/drive/MyDrive/sui/testing_pictures/'

for i in os.listdir(dir_path):
    img = image.load_img(dir_path+'//'+ i, target_size=(200,200))
    plt.imshow(img)
    plt.show(img)
    
    X = image.img_to_array(img)
    X = np.expand_dims(X, axis=0)
    
    images = np.vstack([X])
    val = model.predict(images)

    print(model.predict(images))

    print(val[0][1])
    if val[0][1] == 0:
        print("bufet")
    elif val[0][1] == 1:
        print("kabinet_pocitace")
    elif val[0][1] == 2:
        print("kabinety_prizemi")
    elif val[0][1] == 3:
        print("kabinety_telocvik")
    elif val[0][1] == 4:
        print("pred_wc")
    elif val[0][1] == 5:
        print("schody")
    elif val[0][1] == 6:
        print("u_reditelny")
    elif val[0][1] == 7:
        print("vytah")
    elif val[0][1] == 8:
        print("wc")
    else:
      print("neznámý")