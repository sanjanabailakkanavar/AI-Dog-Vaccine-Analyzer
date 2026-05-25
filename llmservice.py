from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_vaccine_with_llm(extracted_text, matched_vaccines):
    
    prompt = f"""
You are a veterinary vaccine assistant.

Extracted text:
{extracted_text}

Detected vaccines:
{matched_vaccines}

Give:
1. Vaccine Name
2. Purpose
3. Animal Type
4. Booster Info
5. Side Effects
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content