import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model


# Load the Keras model
model = load_model('keras_model.h5')

# Define input image dimensions
img_width, img_height = 224, 224  # Change according to your model's input shape

# Load and preprocess the image
img_path = 'flea_allergy (3).jpg'
img = image.load_img(img_path, target_size=(img_width, img_height))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = img_array / 255.  # Normalize pixel values

# Make predictions
predictions = model.predict(img_array)

# Display predictions
print(predictions)
