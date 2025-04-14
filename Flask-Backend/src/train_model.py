# # In train.py
# import os
# import cv2
# import numpy as np
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# from tensorflow.keras.utils import to_categorical
# from sklearn.model_selection import train_test_split

# def load_images(folder, label, img_size=(64, 64)):
#     images = []
#     labels = []
#     if not os.path.exists(folder):
#         raise FileNotFoundError(f"Directory {folder} does not exist.")
#     for filename in os.listdir(folder):
#         if filename.endswith((".jpg", ".png")):
#             img_path = os.path.join(folder, filename)
#             img = cv2.imread(img_path)
#             if img is not None:
#                 img = cv2.resize(img, img_size)
#                 images.append(img)
#                 labels.append(label)
#     if not images:
#         raise ValueError(f"No valid images found in {folder}.")
#     return images, labels

# # Create models directory
# os.makedirs("models", exist_ok=True)

# # Define dataset paths
# base_path = "datasets/"
# try:
#     eye_open_images, eye_open_labels = load_images(base_path + "eyes/open/", 0)
#     eye_closed_images, eye_closed_labels = load_images(base_path + "eyes/closed/", 1)
#     mouth_not_yawn_images, mouth_not_yawn_labels = load_images(base_path + "mouth/no_yawn/", 0)
#     mouth_yawn_images, mouth_yawn_labels = load_images(base_path + "mouth/yawn/", 1)
# except Exception as e:
#     print(f"Error loading images: {e}")
#     exit()

# # Combine and convert to numpy arrays
# eye_images = np.array(eye_open_images + eye_closed_images)
# eye_labels = np.array(eye_open_labels + eye_closed_labels)
# mouth_images = np.array(mouth_not_yawn_images + mouth_yawn_images)
# mouth_labels = np.array(mouth_not_yawn_labels + mouth_yawn_labels)

# # Normalize and process as before
# eye_images = eye_images / 255.0
# mouth_images = mouth_images / 255.0
# eye_labels = to_categorical(eye_labels, 2)
# mouth_labels = to_categorical(mouth_labels, 2)

# eye_X_train, eye_X_val, eye_y_train, eye_y_val = train_test_split(
#     eye_images, eye_labels, test_size=0.2, random_state=42
# )
# mouth_X_train, mouth_X_val, mouth_y_train, mouth_y_val = train_test_split(
#     mouth_images, mouth_labels, test_size=0.2, random_state=42
# )

# def create_model(input_shape):
#     model = Sequential([
#         Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
#         MaxPooling2D((2, 2)),
#         Conv2D(64, (3, 3), activation='relu'),
#         MaxPooling2D((2, 2)),
#         Conv2D(128, (3, 3), activation='relu'),
#         MaxPooling2D((2, 2)),
#         Flatten(),
#         Dense(128, activation='relu'),
#         Dropout(0.5),
#         Dense(2, activation='softmax')
#     ])
#     model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#     return model

# eye_model = create_model((64, 64, 3))
# eye_model.fit(eye_X_train, eye_y_train, epochs=10, batch_size=32, validation_data=(eye_X_val, eye_y_val))
# eye_model.save("models/drowsiness_model.h5")

# mouth_model = create_model((64, 64, 3))
# mouth_model.fit(mouth_X_train, mouth_y_train, epochs=10, batch_size=32, validation_data=(mouth_X_val, mouth_y_val))
# mouth_model.save("models/mouth_model.h5")

# # print("Models trained and saved successfully!")


import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Function to load and preprocess images
def load_images(folder, label, img_size=(64, 64)):
    images = []
    labels = []
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Directory {folder} does not exist.")
    for filename in os.listdir(folder):
        if filename.endswith((".jpg", ".png")):  # Ensure valid image files
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path)
            if img is not None:
                img = cv2.resize(img, img_size)
                images.append(img)
                labels.append(label)
    if not images:
        raise ValueError(f"No valid images found in {folder}.")
    return images, labels

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Define dataset paths
base_path = "../datasets/"
try:
    eye_open_images, eye_open_labels = load_images(base_path + "eyes/open/", 0)  # 0 = open
    eye_closed_images, eye_closed_labels = load_images(base_path + "eyes/closed/", 1)  # 1 = closed
    mouth_yawn_images, mouth_yawn_labels = load_images(base_path + "mouth/yawn/", 1)  # 1 = yawning
    mouth_not_yawn_images, mouth_not_yawn_labels = load_images(base_path + "mouth/no_yawn/", 0)  # 0 = not yawning
except Exception as e:
    print(f"Error loading images: {e}")
    exit()

# Combine datasets
eye_images = np.array(eye_open_images + eye_closed_images)
eye_labels = np.array(eye_open_labels + eye_closed_labels)
mouth_images = np.array(mouth_yawn_images + mouth_not_yawn_images)
mouth_labels = np.array(mouth_yawn_labels + mouth_not_yawn_labels)

# Normalize pixel values
eye_images = eye_images / 255.0
mouth_images = mouth_images / 255.0

# Convert labels to categorical
eye_labels = to_categorical(eye_labels, 2)
mouth_labels = to_categorical(mouth_labels, 2)

# Split into training and validation sets
eye_X_train, eye_X_val, eye_y_train, eye_y_val = train_test_split(
    eye_images, eye_labels, test_size=0.2, random_state=42
)
mouth_X_train, mouth_X_val, mouth_y_train, mouth_y_val = train_test_split(
    mouth_images, mouth_labels, test_size=0.2, random_state=42
)

# Build CNN model
def create_model(input_shape=(64, 64, 3)):
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(2, activation='softmax')  # 2 classes
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Train eye model
eye_model = create_model()
eye_model.fit(eye_X_train, eye_y_train, epochs=10, batch_size=32, validation_data=(eye_X_val, eye_y_val))
eye_model.save("models/eye_model.h5")

# Train mouth model
mouth_model = create_model()
mouth_model.fit(mouth_X_train, mouth_y_train, epochs=10, batch_size=32, validation_data=(mouth_X_val, mouth_y_val))
mouth_model.save("models/mouth_model.h5")

# Evaluate and print accuracy for eye model
eye_loss, eye_accuracy = eye_model.evaluate(eye_X_val, eye_y_val, verbose=0)
print(f"Eye Model Accuracy on Validation Set: {eye_accuracy * 100:.2f}%")

# Evaluate and print accuracy for mouth model
mouth_loss, mouth_accuracy = mouth_model.evaluate(mouth_X_val, mouth_y_val, verbose=0)
print(f"Mouth Model Accuracy on Validation Set: {mouth_accuracy * 100:.2f}%")

print("Models trained and saved!")