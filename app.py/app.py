from flask import Flask, render_template, request, jsonify, send_file, Response,redirect, url_for,flash
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re
import tempfile
import os
import pandas as pd
//u7jgu7jhg
import csv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin,current_user



app = Flask(__name__, template_folder='D:/finexo-html/templates')
app.static_url_path = '/static'
app.static_folder = 'D:/finexo-html/static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/database'
app.config['SECRET_KEY'] = '0506038dc4e24614eb1450594a405d76'  # Change this to a secure secret key

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'index'


# Define the User class for Flask-Login
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


# Define the user_loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!', 'error')

    return render_template('index.html')





# New route for handling user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get user input from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Validate the user input (you can add more validation if needed)
        if not username or not email or not password:
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('index'))

        # Check if the email already exists in the database
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists!', 'error')
            return redirect(url_for('index'))

        # Create a new user object
        new_user = Users(username=username, email=email, password=password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Flash a success message and redirect to the index page
        flash('User registered successfully!', 'success')
        return redirect(url_for('index'))

    # If the request method is not POST, redirect to the index page
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))




# Load the model (modify paths if necessary)

model = load_model('sentiment_analysis_model.h5')








# Load the tokenizer
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Preprocess text
def preprocess_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation and keep only words and whitespaces
    text = text.lower()
    return text

# Route for rendering the form HTML page
@app.route('/form')
def form():
    return render_template('results.html')

#@app.route('/index')
#def index():
    #return render_template('index.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/about')
def about():
    return render_template('about.html')
#@app.route('/registration')
#def registration():
    #return render_template('registration.html')

# Route to handle form submission
@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        # Extract text input from the form
        text_input = request.form['text_input']

        # Check if the input text contains references to cryptocurrency or crypto with case sensitivity
        if "cryptocurrency" in text_input or "Crypto" in text_input or "CRYPTOCURRENCY" in text_input or "CRYPTO" in text_input or "Cryptocurrency" in text_input or "cryptoCurrency" in text_input or "crypto" in text_input:
            # Preprocess text
            preprocessed_text = preprocess_text(text_input)

            # Tokenize and pad sequence
            sequence = tokenizer.texts_to_sequences([preprocessed_text])
            padded_sequence = pad_sequences(sequence, maxlen=73, padding='post')

            # Make prediction
            prediction = model.predict(padded_sequence)[0][0]
            sentiment = "positive" if prediction > 0.5 else "negative"

            # Return the predicted sentiment as JSON
            return jsonify({'sentiment': sentiment})
        else:
            # Return an error message for invalid text
            return jsonify({'error': 'Please talk according to the aspect of cryptocurrency.'})

        # If the request is not POST, return an empty response
    return ''

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        # Read the file contents as binary data
        file_content = file.read().decode('latin-1')

        # Preprocess text from the file
        preprocessed_texts = [preprocess_text(line) for line in file_content.split('\n') if line.strip()]

        # Tokenize and pad sequences
        sequences = tokenizer.texts_to_sequences(preprocessed_texts)
        padded_sequences = pad_sequences(sequences, maxlen=73, padding='post')

        # Make predictions
        predictions = model.predict(padded_sequences)
        sentiments = ["positive" if pred > 0.5 else "negative" for pred in predictions]

        # Create DataFrame with original text and predicted sentiment
        df = pd.DataFrame({'Text': preprocessed_texts, 'Sentiment': sentiments})

        # Write DataFrame to a temporary CSV file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w', newline='', encoding='utf-8') as temp_file:
            df.to_csv(temp_file.name, index=False)

        # Read the content of the temporary file
        with open(temp_file.name, 'rb') as file:
            file_content = file.read()

        # Serve the file content as a response
        return Response(file_content, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=labeled_dataset.csv'})

    # If the request is not POST, return an empty response
    return ''






if __name__ == '__main__':
    app.run(debug=True)
