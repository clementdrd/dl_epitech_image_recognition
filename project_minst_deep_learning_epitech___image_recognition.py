# -*- coding: utf-8 -*-
"""Project MINST Deep-Learning Epitech | Image recognition

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1loZR_JkM3J_Mp0Gj9Y8D2vLbmMEo5gNB
"""

#pip install python-mnist

"""Import des modules:
  - pandas => use for the manipulation of the datasets
  - matplotlib => use for rendre graphicly some results
  - tensorflow => use for all the functions to create the cnn and launch the test/train process
  - sklearn => use for spliting the train and test dataset
  - mnist => use for the small image processing
"""

# Commented out IPython magic to ensure Python compatibility.
import os
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
# %matplotlib inline
#import easygui

print(tf.__version__)

"""Import dataset.csv (stock not in the drive but in the local google colab environment) with their correct paths."""

st.write("Select a train file")
#filename = easygui.fileopenbox()
file = st.file_uploader("Upload a csv", type=["csv"])
df_train = pd.read_csv(filename)
st.write("Select a test file")
#filename = easygui.fileopenbox()
df_test = pd.read_csv(filename)

print(df_train)
print(df_test)

df_train.sample(10)

df_test.sample(10)

"""Here we create and load our dataset in keras dataset"""

fashion_mnist = tf.keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

"""Here we are going to classify all categories we want and shape the images"""

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

train_images.shape

len(train_labels)

train_labels

test_images.shape

len(test_labels)

fig = plt.figure()
plt.imshow(train_images[10])
plt.colorbar()
plt.grid(False)
st.pyplot(fig)

"""We have to divide the table of images by 255 so we can have a table of number between 0 and 1."""

train_images = train_images / 255.0

test_images = test_images / 255.0

fig = plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
#plt.show()
st.pyplot(fig)
"""After printing all stuff, to check if everything is ok, we then have to start making the models. The input shape is based on the image scale which is 28x28 pixels. Then we use Dense with an "relu" activation and 128 units to be more precise."""

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])

"""Here we decided to use 'adam' as optimizer because he is one the most efficient nowadays. Then we decided to use loss SparseCategoricalCrossentropy because we have more than 2 labels and for the metrics we use accuracy to display it during training in able to have floats."""

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

"""We want to train the models, we then make 10 epochs to train the deep learning 10 times for a better training which became more effective each time but also taking more time."""

model.fit(train_images, train_labels, epochs=10)

"""We evaluate what we obtained and what was expected to create a percent of accuracy. As we can see in the result, we have 88% accuracy average."""

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\nTest accuracy:', test_acc)

"""We use a sequential with a Softmax layer to normalize the data of each image"""

probability_model = tf.keras.Sequential([model, 
                                         tf.keras.layers.Softmax()])

predictions = probability_model.predict(test_images)

predictions[0]

np.argmax(predictions[0])

test_labels[0]

"""Those functions help us to display plots and images of the dataset and predictions."""

def plot_image(i, predictions_array, true_label, img):
  true_label, img = true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  true_label = true_label[i]
  plt.grid(False)
  plt.xticks(range(10))
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')

"""We here make some function to print the image and the pourcentage of recognition we have for each."""

i = 0
fig = plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions[i], test_labels, test_images)
plt.subplot(1,2,2)
plot_value_array(i, predictions[i],  test_labels)

st.pyplot(fig)
#plt.show()

i = 12
fig = plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions[i], test_labels, test_images)
plt.subplot(1,2,2)
plot_value_array(i, predictions[i],  test_labels)

st.pyplot(fig)
#plt.show()

# Plot the first X test images, their predicted labels, and the true labels.
# Color correct predictions in blue and incorrect predictions in red.
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
fig = plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions[i], test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
st.pyplot(fig)
#plt.show()

# Grab an image from the test dataset.
img = test_images[1]

print(img.shape)

# Add the image to a batch where it's the only member.
img = (np.expand_dims(img,0))

print(img.shape)

predictions_single = probability_model.predict(img)

print(predictions_single)

plot_value_array(1, predictions_single[0], test_labels)
_ = plt.xticks(range(10), class_names, rotation=45)

np.argmax(predictions_single[0])
