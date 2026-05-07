import tensorflow as tf
import cv2
import numpy as np

model = tf.keras.models.load_model("body_shape_model.h5")

classes = ["hourglass", "inverted_triangle", "pear", "rectangle"]  # update if needed

def predict_body_shape(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return "Unknown"

    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.reshape(img, (1, 224, 224, 3))

    prediction = model.predict(img)

    index = np.argmax(prediction)   # ✅ VERY IMPORTANT LINE

    return classes[index]