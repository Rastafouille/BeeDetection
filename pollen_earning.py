# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 11:04:21 2019

@author: JS235785
"""

# https://www.tensorflow.org/tutorials/images/classification
# https://www.kaggle.com/ivanfel/honey-bee-pollen
# https://www.kaggle.com/jenny18/honey-bee-annotated-images/data



from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd

import os
import numpy as np
import matplotlib.pyplot as plt

train_dir = 'C:/Users/js235785/Documents/GitHub/PollenDataSet2/train'
validation_dir = 'C:/Users/js235785/Documents/GitHub/PollenDataSet2/test'

#train_dir = 'C:/Users/rastafouille/Documents/GitHub/PollenDataSet/train'
#validation_dir = 'C:/Users/rastafouille/Documents/GitHub/PollenDataSet/test'




train_with_dir = os.path.join(train_dir, 'with') 
train_without_dir = os.path.join(train_dir, 'without')  
validation_with_dir = os.path.join(validation_dir, 'with')  
validation_without_dir = os.path.join(validation_dir, 'without')  


num_with_tr = len(os.listdir(train_with_dir))
print ('num_with_tr='+str(num_with_tr))
num_without_tr = len(os.listdir(train_without_dir))
print ('num_without_tr='+str(num_without_tr))

num_with_val = len(os.listdir(validation_with_dir))
print ('num_with_val='+str(num_with_val))
num_without_val = len(os.listdir(validation_without_dir))
print ('num_without_val='+str(num_without_val))

total_train = num_with_tr + num_without_tr
total_val = num_with_val + num_without_val

batch_size = 50
epochs = 100

IMG_HEIGHT = 150
IMG_WIDTH = 100

train_image_generator = ImageDataGenerator(rescale=1./255)#,rotation_range=45,width_shift_range=.15,height_shift_range=.15,horizontal_flip=True,zoom_range=0.5) # Generator for our training data
validation_image_generator = ImageDataGenerator(rescale=1./255)#,rotation_range=45,width_shift_range=.15,height_shift_range=.15,horizontal_flip=True,zoom_range=0.5) # Generator for our validation data


train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='binary')

val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                              directory=validation_dir,
                                                              target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                              class_mode='binary')

sample_val_images, _ = next(val_data_gen)

# This function will plot images in the form of a grid with 1 row and 5 columns where images are placed in each column.
def plotImages(images_arr):
    fig, axes = plt.subplots(1, 2, figsize=(10,10))
    axes = axes.flatten()
    for img, ax in zip( images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.show()
    
#plotImages(sample_training_images[:5])



model = Sequential([
    Conv2D(8, 3, padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
    MaxPooling2D(),
    Dropout(0.2),
    Conv2D(16, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Dropout(0.2),
    Flatten(input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
    Dense(512, activation='relu'),
    Dense(1,activation='sigmoid')
])
    
    
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])


model.summary()
print('summary OK')
history = model.fit_generator(
    train_data_gen,
    steps_per_epoch=total_train // batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=total_val // batch_size
)
print('Fit OK')

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()


predictions = model.predict(sample_val_images)
    
plt.figure(figsize=(10,80))
for i in range(batch_size):
    plt.subplot(40,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(sample_val_images[i], cmap=plt.cm.binary)
    plt.xlabel(predictions[i])
plt.show()




