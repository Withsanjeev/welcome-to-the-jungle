# app.py
import streamlit as st
import pickle
import pandas as pd
from fuzzywuzzy import process

# Load the saved model and data
try:
    df = pickle.load(open('model.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Error: model.pkl or similarity.pkl not found. Please upload them.")
    st.stop()  # Stop execution if files are missing

def recommendation(title, threshold=80):
    jobs = []
    for existing_title in df['Title']:
        score = process.extractOne(title, [existing_title])[1]
        if score >= threshold:
            jobs.append(existing_title)
    if not jobs:
        st.write("I am enil avaible .")
    return jobs

# Streamlit app
st.title("Job Recommendation System")

# Input field for job title
job_title = st.text_input("Enter a job title:")

# Recommendation button
if st.button("Recommend Jobs"):
    if job_title:
        recommendations = recommendation(job_title)
        if recommendations:
            st.write("Recommended Jobs:")
            for job in recommendations:
                st.write(job)

# File upload for model.pkl and similarity.pkl (optional)
st.sidebar.markdown("## Upload Model Files (Optional)")
model_file = st.sidebar.file_uploader("Upload model.pkl", type=["pkl"])
similarity_file = st.sidebar.file_uploader("Upload similarity.pkl", type=["pkl"])

if model_file and similarity_file:
    try:
        df = pickle.load(model_file)
        similarity = pickle.load(similarity_file)
        st.success("Model files uploaded successfully!")
    except Exception as e:
        st.error(f"Error loading model files: {e}")
