import google.generativeai as genai
import streamlit as st

# Configure your API key (same as in secrets.toml)
genai.configure(api_key="AIzaSyBd4YXrT0uhQt1rbqmiX5wdkmVsis_Gq-c")  # Replace with your key

# List all available models that support generateContent
models = genai.list_models()

print("Available models that support text generation:")
for m in models:
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
