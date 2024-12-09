import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
import time

IMAGE_FOLDER = r'discord erpg autotyper\images'  # Directory to monitor for images
model_path = r'discord erpg autotyper\cnn_model.h5'  # Path to the trained model
TRAIN_DATASET = r'discord erpg autotyper\dataset'  # Directory used for training
OUTPUT_TEXT_FILE = r"discord erpg autotyper\storage.txt"  # Output file to write the predictions

model = load_model(model_path)

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_generator = train_datagen.flow_from_directory(
    TRAIN_DATASET,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)
class_indices = train_generator.class_indices
classes = {v: k for k, v in class_indices.items()}  

img_size = (150, 150)  

processed_files = set()

print(f"Monitoring directory: {IMAGE_FOLDER}")
while True:
    try:
        for filename in os.listdir(IMAGE_FOLDER):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(IMAGE_FOLDER, filename)

                if img_path in processed_files:
                    continue

                try:
                    img = load_img(img_path, target_size=img_size)
                    img_array = img_to_array(img)
                    img_array = img_array / 255.0
                    img_array = tf.expand_dims(img_array, axis=0)  

                    prediction = model.predict(img_array)
                    predicted_class = classes[prediction.argmax()]  

                    with open(OUTPUT_TEXT_FILE, 'w') as file:
                        file.write(f"{predicted_class}")

                    print(f"Processed: {filename}, Predicted Class: {predicted_class}")
                    processed_files.add(img_path)  
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
    except Exception as main_error:
        print(f"Monitoring error: {main_error}")

    time.sleep(2)  
