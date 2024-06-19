####################################
# load Reuters dataset             #
####################################
import numpy as np
from tensorflow.keras.datasets import reuters
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical

# Load Reuters dataset
max_words = 10000
(x_train, y_train), (x_test, y_test) = reuters.load_data(num_words=max_words)

# Tokenize the data
tokenizer = Tokenizer(num_words=max_words)
x_train = tokenizer.sequences_to_matrix(x_train, mode='binary')
x_test = tokenizer.sequences_to_matrix(x_test, mode='binary')

# Convert labels to categorical
num_classes = np.max(y_train) + 1
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

####################################
# Build DNN model                  #
####################################
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Build the DNN model
dnn_model = Sequential()
dnn_model.add(Dense(512, input_shape=(max_words,), activation='relu'))
dnn_model.add(Dropout(0.5))
dnn_model.add(Dense(num_classes, activation='softmax'))

# Compile the DNN model
dnn_model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

# Train the DNN model
dnn_history = dnn_model.fit(x_train, y_train,batch_size=32,epochs=5,verbose=1,validation_split=0.1)

# Evaluate the DNN model
dnn_score = dnn_model.evaluate(x_test, y_test, verbose=0)
print(f"DNN Test accuracy: {dnn_score[1]}")

####################################
# Build LSTM model                 #
####################################
import numpy as np
from tensorflow.keras.datasets import reuters
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Load and preprocess data
max_words = 10000
(x_train, y_train), (x_test, y_test) = reuters.load_data(num_words=max_words)

# Determine the maximum sequence length
maxlen = 80  # Reduced maxlen for faster computation

# Pad sequences
x_train = pad_sequences(x_train, maxlen=maxlen)
x_test = pad_sequences(x_test, maxlen=maxlen)

# Convert labels to categorical
num_classes = np.max(y_train) + 1
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

# Build and compile the LSTM model
lstm_model = Sequential()
lstm_model.add(Embedding(max_words, 128, input_length=maxlen))
lstm_model.add(LSTM(64))  # Reduced number of LSTM units
lstm_model.add(Dense(num_classes, activation='softmax'))
lstm_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the LSTM model
lstm_model.fit(x_train, y_train,batch_size=32,epochs=5,verbose=1,validation_split=0.1)  # Increased batch size and reduced epochs

# Evaluate the LSTM model
lstm_score = lstm_model.evaluate(x_test, y_test, verbose=0)
print(f"LSTM Test accuracy: {lstm_score[1]}")

####################################
# Compare results                  #
####################################
print(f"DNN Test accuracy: {dnn_score[1]}")
print(f"LSTM Test accuracy: {lstm_score[1]}")