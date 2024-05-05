# Crypto Currency Legalization Predictor

## Description
The Crypto Currency Legalization Predictor  in PAkistan is a Flask web application that predicts cryptocurrency legalization sentiment and performs sentimental analysis. Users can input text data through a form or upload a file to get sentiment predictions.
 All code in this project is original and not sourced from external websites or repositories.
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

