import pdfplumber
import spacy
from groq import Groq
import json
def extractTextfromPdf(pdf_path):
    text=""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text+=page.extract_text() + "\n"
    return text.strip()




API_KEY="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"


def resume_with_text(text:str,job_des:str)->dict:
    prompt=f"""
        You are an AI assitant that analyzes resumes for a software engineering job application.
        Given a resume and a job description ,extract the following details:

        1. Identify all skills mentioned in the resume
        2.Calculate the total years of experience
        3.Categories the projects based on the domain(e.g. AI,web development,cloud etc)
        4. Give the resume rating relevance to the job description on a range between 0 t0 100

        Resume:
        {text}
        Job Description:
        {job_des}

        provide the output in a valid JSON format in the following structure:

        {{
        "ratting":"<percentage>",
        "skills": ["skill1","skill2",.......],
        "total_experience":"<number of years>",
        "project_category":["category1","category2",......]
       
       }}

    """

    try:
        client=Groq(api_key=API_KEY)
        response=client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                "role":"user",
                "content":prompt
            }
            ],
            temperature=0.6,
            response_format={"type":"json_object"}

        )
        result=response.choices[0].message.content
        return json.loads(result)
    except Exception as e:
        return str(e)
        print(e)

def process_resume(pdf_path,job_description):
    try:
        resume_text=extractTextfromPdf(pdf_path)
        data=resume_with_text(resume_text,job_description)
        return data
    except Exception as e:
        return str(e)







