# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
from PIL import Image

# Load the model
model = tf.keras.models.load_model('keras_model.h5')

def predictRisk(image_path):
    img = Image.open(image_path).convert('RGB')
    img = tf.image.resize(img,[224, 224])  # Resize to the model's expected input size
    img_array = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Add a batch dimension

    # Load class labels from labels.txt
    with open('labels.txt', 'r') as f:
        class_labels = [line.strip() for line in f]  # Remove leading/trailing whitespace]

    # Make a prediction
    predictions = model.predict(img_array)
    predicted_class = class_labels[np.argmax(predictions[0])]

    # Print the output
    print("Predicted class:", predicted_class)
    print("Prediction probabilities:", predictions[0])
    
    return predicted_class , predictions[0]