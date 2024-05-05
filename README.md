## Description
The Sentiment Analysis on Crypto Legalization in Pakistan is a Flask web application designed to analyze public sentiment regarding cryptocurrency legalization in Pakistan. It predicts cryptocurrency legalization sentiment and performs sentiment analysis on textual data. Users can input text data through a form or upload a file to get sentiment predictions.

## Problem Setup
With the increasing global interest in cryptocurrencies, the legal status of cryptocurrencies, including Bitcoin and others, is a topic of discussion in many countries, including Pakistan. This project aims to analyze public sentiment regarding the legalization of cryptocurrencies in Pakistan to understand the attitude towards this emerging technology.
 
 ## Techniques
- Sentiment Analysis: The project uses a machine learning model trained on the dataset to predict sentiment and perform sentimental analysis. The sentiment analysis model is built using deep learning techniques with Keras and TensorFlow.
- Text Preprocessing: Before feeding the data into the sentiment analysis model, text preprocessing techniques such as removing URLs, punctuation, and converting text to lowercase are applied to clean the textual data.
- Flask Web Application: The predictor is deployed as a Flask web application, allowing users to input text data through a form or upload a file to get sentiment predictions. User registration and login functionalities are implemented using Flask-Login and user data is stored in a MySQL database.
- Model Deployment: The sentiment analysis model is loaded within the Flask application and used to make predictions on user input data.
## Dependencies
- Flask
- TensorFlow
- Keras
- Pandas
- Flask-SQLAlchemy
- Flask-Login

## Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up a MySQL database and update the `SQLALCHEMY_DATABASE_URI` in `app.py`.
4. Set a secure secret key in `app.py` for Flask session management.

## Usage
1. Run the Flask application: `python app.py`
2. Navigate to `http://localhost:5000` in your web browser.
3. Register or log in with your credentials.
4. Input text data in the form or upload a file.
5. Click the "Predict" button to get sentiment predictions.

## Model
- The sentiment analysis model is trained using Keras and TensorFlow.
- Pretrained model weights are loaded from `sentiment_analysis_model.h5`.
- Tokenizer for text preprocessing is loaded from `tokenizer.pkl`.

## Database
-Datasets sre created and retrieved from platform lite twitter websites and instagram through webscraping.


## Contributing
f247805 Amna Shafaq, f23 Arham

