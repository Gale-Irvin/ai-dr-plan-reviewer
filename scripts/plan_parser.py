from docx import Document

def extract_text(file_path):
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return text

# Example use:
if __name__ == "__main__":
    sample_path = "data/sample_dr_plan.docx"
    content = extract_text(sample_path)
    print(content[:1000])  # Show only the first 1000 characters
