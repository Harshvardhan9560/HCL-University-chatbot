# HCL University AI Chatbot

An AI-powered college chatbot designed to answer common university-related questions such as admissions, fees, exams, college timings, library information, office contact details, and leave applications.

The chatbot uses **Natural Language Processing (NLP)** and **Machine Learning** to understand user questions and provide relevant responses.

## Live Demo

Try the deployed chatbot here:

[HCL University AI Chatbot](https://hcl-university-chatbot-p2ueldu2ninx8blrp4chhh.streamlit.app/)

## Features

* AI-based question classification
* Interactive chatbot interface using Streamlit
* NLP-based text processing
* TF-IDF feature extraction
* Linear Support Vector Machine (SVM) classifier
* College/university-specific question answering
* Common Questions section
* Most Asked Questions section
* Recent Questions section
* Greeting detection
* Pre-trained model files for fast application startup

## Technologies Used

* Python
* Streamlit
* Scikit-learn
* Pandas
* NumPy
* TF-IDF Vectorization
* Linear SVM
* Pickle
* Excel / CSV Dataset

## How the Chatbot Works

The chatbot follows this pipeline:

```text
User Question
      ↓
Text Preprocessing
      ↓
TF-IDF Vectorization
      ↓
SVM Classification
      ↓
Intent Prediction
      ↓
Response Mapping
      ↓
Chatbot Response
```

## Project Structure

```text
HCL-University-chatbot/
│
├── dataset/
│   └── AI-Powered Chatbot.xlsx
│
├── .gitignore
├── app.py
├── bot_response_mapping.pkl
├── label_encoder.pkl
├── requirements.txt
├── svm.pkl
├── tfidf_vectorizer.pkl
├── train.py
└── training_data.csv
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Harshvardhan9560/HCL-University-chatbot.git
```

Move into the project directory:

```bash
cd HCL-University-chatbot
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Chatbot Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

The chatbot will open in your browser at the local Streamlit address.

## Model Files

The application uses the following trained files:

* `tfidf_vectorizer.pkl` — TF-IDF vectorizer
* `label_encoder.pkl` — Converts intent labels
* `svm.pkl` — Trained SVM classification model
* `bot_response_mapping.pkl` — Maps intents to chatbot responses

## Training the Model

If the training dataset is modified, the model can be retrained using:

```bash
python train.py
```

This generates the required model files used by `app.py`.

## Example Questions

The chatbot can answer questions such as:

```text
What are the college timings?
Where is the library?
What is the fee structure?
How can I contact the college office?
What are the admission requirements?
When are the exams?
How can I apply for leave?
```

## Deployment

The application is deployed using **Streamlit Community Cloud**.

Live application:

https://hcl-university-chatbot-p2ueldu2ninx8blrp4chhh.streamlit.app/

## Future Improvements

* Improve intent classification accuracy
* Add more university-specific training data
* Add multilingual support
* Add voice input and output
* Connect the chatbot to a live university database
* Add authentication
* Improve conversational context
* Add feedback collection for chatbot responses

## Author

Harshvardhan Singh

## License

This project is developed for educational and academic purposes.
