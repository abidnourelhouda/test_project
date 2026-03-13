import os
import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

def score_cv(text):
    """
    Score the CV based on criteria: education (bac +5) and experience (22 years).
    """
    score = 0
    # Education: look for bac +5 or master
    if re.search(r'bac\s*\+\s*5', text, re.IGNORECASE) or re.search(r'master', text, re.IGNORECASE):
        score += 10
    # Experience: look for X years of experience
    exp_match = re.search(r'(\d+)\s*ans?\s*d\'?expérience', text, re.IGNORECASE)
    if exp_match:
        years = int(exp_match.group(1))
        score += years  # Higher years give higher score
    return score

def sort_cvs(folder_path):
    """
    Sort CVs in the folder based on scores.
    """
    cvs = []
    for file in os.listdir(folder_path):
        if file.lower().endswith('.pdf'):
            path = os.path.join(folder_path, file)
            try:
                text = extract_text_from_pdf(path)
                score = score_cv(text)
                cvs.append((file, score))
            except Exception as e:
                print(f"Error processing {file}: {e}")
    cvs.sort(key=lambda x: x[1], reverse=True)
    return cvs

if __name__ == "__main__":
    folder = input("Enter the folder path containing PDF CVs: ")
    if os.path.isdir(folder):
        rankings = sort_cvs(folder)
        print("Rankings:")
        for i, (cv, score) in enumerate(rankings, 1):
            print(f"{i}. {cv}: Score {score}")
    else:
        print("Invalid folder path.")