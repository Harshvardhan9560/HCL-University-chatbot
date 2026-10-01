import os
import re
import pickle
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCEL_PATHS = [
    os.path.join(BASE_DIR, "dataset", "AI-Powered Chatbot.xlsx"),
    os.path.join(BASE_DIR, "AI-Powered Chatbot.xlsx")
]

EXCEL_FILE = next((p for p in EXCEL_PATHS if os.path.exists(p)), EXCEL_PATHS[0])
CSV_FILE = os.path.join(BASE_DIR, "training_data.csv")


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


print(f"\nLoading Excel dataset from: {EXCEL_FILE}")
if not os.path.exists(EXCEL_FILE):
    raise FileNotFoundError(f"Excel file not found at {EXCEL_FILE}")

excel_df = pd.read_excel(EXCEL_FILE)

msg_col = next((c for c in excel_df.columns if any(k in c.lower() for k in ["user message", "question", "text"])), None)
intent_col = next((c for c in excel_df.columns if "intent" in c.lower()), None)
resp_col = next((c for c in excel_df.columns if any(k in c.lower() for k in ["bot response", "response", "answer"])), None)

if not msg_col or not intent_col:
    raise ValueError(f"Required 'User Message' and 'Intent' columns not found. Detected: {excel_df.columns.tolist()}")

bot_response_mapping = {}
if resp_col:
    for _, row in excel_df.dropna(subset=[intent_col, resp_col]).iterrows():
        i_val = str(row[intent_col]).strip()
        r_val = str(row[resp_col]).strip()
        if i_val not in bot_response_mapping and r_val:
            bot_response_mapping[i_val] = r_val

excel_df = excel_df[[msg_col, intent_col]].copy()
excel_df.columns = ["text", "intent"]


if os.path.exists(CSV_FILE):
    print(f"\nLoading supplementary CSV from: {CSV_FILE}")
    csv_df = pd.read_csv(CSV_FILE)
 
    csv_resp_col = next((c for c in csv_df.columns if any(k in c.lower() for k in ["response", "bot response", "answer"])), None)
    if csv_resp_col and "intent" in csv_df.columns:
        for _, row in csv_df.dropna(subset=["intent", csv_resp_col]).iterrows():
            i_val = str(row["intent"]).strip()
            r_val = str(row[csv_resp_col]).strip()
            if i_val not in bot_response_mapping and r_val:
                bot_response_mapping[i_val] = r_val

    if "text" in csv_df.columns and "intent" in csv_df.columns:
        csv_df = csv_df[["text", "intent"]].copy()
    else:
        print("Warning: CSV missing 'text' or 'intent' column. Skipping CSV.")
        csv_df = pd.DataFrame(columns=["text", "intent"])
else:
    print("\nSupplementary training_data.csv not found (continuing with Excel data).")
    csv_df = pd.DataFrame(columns=["text", "intent"])

common_seed_data = [
    # College Timings
    ("What are the college timings?", "college_timings", "College working hours are 8:30 AM to 4:30 PM, Monday through Friday."),
    ("College timing", "college_timings", "College working hours are 8:30 AM to 4:30 PM, Monday through Friday."),
    ("When does college open and close?", "college_timings", "College working hours are 8:30 AM to 4:30 PM, Monday through Friday."),
    
    # Office Contact
    ("How can I contact the college office?", "office_contact", "You can reach the college office at admin@college.edu or call (555) 010-1000."),
    ("Contact details for college office", "office_contact", "You can reach the college office at admin@college.edu or call (555) 010-1000."),
    
    # Library
    ("Where is the library?", "campus_facilities", "The main library is located in Building B, 2nd floor."),
    
    # Admission Requirements
    ("What are the admission requirements?", "admissions", "Admission requirements include high school transcripts, valid ID, and standard application forms on our admissions portal."),
    ("Admission eligibility criteria", "admissions", "Admission requirements include high school transcripts, valid ID, and standard application forms on our admissions portal."),
    
    # Fee Structure
    ("What is the fee structure?", "fee_structure", "Tuition and fee breakdowns are available under the Finance section on the student portal."),
    ("College tuition fees", "fee_structure", "Tuition and fee breakdowns are available under the Finance section on the student portal."),
    
    # Exam Dates
    ("What are the exam dates?", "exam_schedule", "Exam dates and schedules are published on the Student Portal under Exam Schedule."),
    ("When are the exams?", "exam_schedule", "Exam dates and schedules are published on the Student Portal under Exam Schedule."),
    
    # Leave Application
    ("How can I apply for leave?", "leave_application", "Submit your leave of absence form via Student Portal > Administration > Leave Request."),
    ("Apply for student leave", "leave_application", "Submit your leave of absence form via Student Portal > Administration > Leave Request.")
]

seed_rows = []
for text, intent, resp in common_seed_data:
    seed_rows.append({"text": text, "intent": intent})
    if intent not in bot_response_mapping:
        bot_response_mapping[intent] = resp

seed_df = pd.DataFrame(seed_rows)

df = pd.concat([excel_df, csv_df, seed_df], ignore_index=True)
df = df.dropna(subset=["text", "intent"])
df["text"] = df["text"].astype(str)
df["intent"] = df["intent"].astype(str)

df["clean_text"] = df["text"].apply(clean_text)
df = df[df["clean_text"].str.len() > 0]
df = df.drop_duplicates(subset=["clean_text", "intent"]).reset_index(drop=True)

print(f"\nTotal clean training questions: {len(df)}")
print(f"Total unique intents: {df['intent'].nunique()}")

# Ensure every intent in df has a fallback answer in bot_response_mapping
for intent in df["intent"].unique():
    if intent not in bot_response_mapping:
        bot_response_mapping[intent] = "Please check the college student portal for detailed information regarding this topic."


label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["intent"])
X_text = df["clean_text"]

# Using min_df=1 and standard english stop_words
tfidf = TfidfVectorizer(
    ngram_range=(1, 2),
    stop_words="english",
    sublinear_tf=True,
    max_features=10000
)

X_train = tfidf.fit_transform(X_text)

svm_model = LinearSVC(class_weight="balanced", C=1.0, random_state=42)
svm_model.fit(X_train, y)


training_questions = df["clean_text"].tolist()
training_intents = df["intent"].tolist()
training_question_vectors = tfidf.transform(training_questions)


print("\nSaving model artifacts...")
artifacts = {
    "tfidf_vectorizer.pkl": tfidf,
    "label_encoder.pkl": label_encoder,
    "svm.pkl": svm_model,
    "bot_response_mapping.pkl": bot_response_mapping,
    "training_questions.pkl": training_questions,
    "training_question_vectors.pkl": training_question_vectors,
    "training_intents.pkl": training_intents
}

for filename, obj in artifacts.items():
    with open(os.path.join(BASE_DIR, filename), "wb") as f:
        pickle.dump(obj, f)
    print(f"  ✓ Saved: {filename}")

print("\nRetraining complete! Restart your existing app.py now.")