import PyPDF2
from docx import Document

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


def extract_text_from_word(file_path):
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text


if __name__ == "__main__":
    pdf_text = extract_text_from_pdf("Documents\Assignment Question.pdf")
    word_text = extract_text_from_word("Documents\Assignment Question.docx")