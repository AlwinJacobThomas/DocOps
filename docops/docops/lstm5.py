import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense
import pickle

def train_sentiment_model():
    # Load the dataset
    data = pd.read_csv('docops/reviews.csv')
    data['tag'] = data['tag'].map({'negative': 0, 'positive': 1})
    # Split the dataset into training and testing sets
    X = data['review'].values
    y = data['tag'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Tokenize the text data
    max_words = 10000
    tokenizer = Tokenizer(num_words=max_words)
    tokenizer.fit_on_texts(X_train)

    # Save the tokenizer
    with open('tokenizer.pkl', 'wb') as f:
        pickle.dump(tokenizer, f)

    # Convert text to sequences
    X_train_seq = tokenizer.texts_to_sequences(X_train)
    X_test_seq = tokenizer.texts_to_sequences(X_test)

    # Pad sequences for equal length
    max_sequence_length = 100
    X_train_padded = pad_sequences(X_train_seq, maxlen=max_sequence_length)
    X_test_padded = pad_sequences(X_test_seq, maxlen=max_sequence_length)

    # Build the LSTM model
    embedding_dim = 100
    model = Sequential()
    model.add(Embedding(input_dim=max_words, output_dim=embedding_dim, input_length=max_sequence_length))
    model.add(LSTM(units=128, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(units=1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()

    # Train the model
    batch_size = 64
    epochs = 10
    model.fit(X_train_padded, y_train, batch_size=batch_size, epochs=epochs, validation_data=(X_test_padded, y_test))

    # Save the trained model
    model.save('sentiment_model.h5')

def analyze_sentiment(review_text):
    # Load the trained model
    model = load_model('sentiment_model.h5')

    # Load the tokenizer
    with open('tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)

    # Convert text to sequences
    review_seq = tokenizer.texts_to_sequences([review_text])

    # Pad sequences for equal length
    max_sequence_length = 100
    review_padded = pad_sequences(review_seq, maxlen=max_sequence_length)

    # Make predictions
    prediction = model.predict(review_padded)[0][0]

    return float(prediction)

# Example usage
train_sentiment_model()
review = "This movie is bad!"
positivity = analyze_sentiment(review)
print('Review:', review)
print('Positivity:', positivity)
