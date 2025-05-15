# import numpy as np
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense, Dropout
# from sklearn.model_selection import train_test_split
# import os

# # Simulate sequence data (replace with your dataset)
# def generate_synthetic_data(num_samples=1000, sequence_length=30):
#     sequences = []
#     labels = []
#     for _ in range(num_samples):
#         sequence = []
#         is_drowsy = np.random.choice([0, 1])
#         for _ in range(sequence_length):
#             # [left_eye_closed, right_eye_closed, is_yawning]
#             if is_drowsy:
#                 state = [np.random.choice([0, 1], p=[0.3, 0.7]),
#                          np.random.choice([0, 1], p=[0.3, 0.7]),
#                          np.random.choice([0, 1], p=[0.4, 0.6])]
#             else:
#                 state = [np.random.choice([0, 1], p=[0.8, 0.2]),
#                          np.random.choice([0, 1], p=[0.8, 0.2]),
#                          np.random.choice([0, 1], p=[0.9, 0.1])]
#             sequence.append(state)
#         sequences.append(sequence)
#         labels.append(is_drowsy)
#     return np.array(sequences), np.array(labels)

# # Generate data
# sequence_length = 30
# X, y = generate_synthetic_data(num_samples=1000, sequence_length=sequence_length)

# # Convert labels to one-hot
# from tensorflow.keras.utils import to_categorical
# y = to_categorical(y, num_classes=2)

# # Split data
# X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# # Build LSTM model
# model = Sequential([
#     LSTM(64, input_shape=(sequence_length, 3), return_sequences=False),
#     Dropout(0.5),
#     Dense(32, activation='relu'),
#     Dense(2, activation='softmax')  # 2 classes: drowsy, not drowsy
# ])

# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# # Train model
# model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))

# # Save model
# os.makedirs("models", exist_ok=True)
# model.save("models/lstm_model.h5")

# # Evaluate
# loss, accuracy = model.evaluate(X_val, y_val)
# print(f"LSTM Model Accuracy: {accuracy * 100:.2f}%")

# train_lstm_feature_model.py

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import os

# Generate synthetic EAR/MAR sequences
def generate_synthetic_data(n_samples=2000, seq_len=30):
    X, y = [], []
    for _ in range(n_samples):
        label = np.random.choice([0,1])  # 0=alert,1=drowsy
        seq = []
        for _ in range(seq_len):
            if label == 1:
                # simulate drowsy: lower EAR, higher MAR
                ear = np.random.normal(loc=0.15, scale=0.05)  # closed eye ~0.15
                mar = np.random.normal(loc=0.8, scale=0.1)    # wide mouth
            else:
                # simulate alert: normal EAR/MAR
                ear = np.random.normal(loc=0.3, scale=0.05)   # open eye ~0.3
                mar = np.random.normal(loc=0.3, scale=0.05)   # closed mouth ~0.3
            seq.append([ear, mar])
        X.append(seq)
        y.append(label)
    return np.array(X), np.array(y)

# Prepare data
SEQ_LEN = 30
X, y = generate_synthetic_data(2000, SEQ_LEN)
y = to_categorical(y, 2)

# Split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Build LSTM
model = Sequential([
    LSTM(64, input_shape=(SEQ_LEN, 2), return_sequences=False),
    Dropout(0.5),
    Dense(32, activation='relu'),
    Dense(2, activation='softmax')
])
model.compile('adam', 'categorical_crossentropy', metrics=['accuracy'])

# Train
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_val, y_val))

# Save
os.makedirs("models", exist_ok=True)
model.save("models/lstm_feature_model.h5")

# Evaluate
loss, acc = model.evaluate(X_val, y_val, verbose=0)
print(f"LSTM-Feature Model Accuracy: {acc*100:.2f}%")
