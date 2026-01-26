import os
import sys

from plan_parser import extract_text
from review_engine import load_checklist, review_against_standards, save_markdown

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/review_cli.py data/your_plan.docx")
        sys.exit(1)

    docx_path = sys.argv[1]
    if not os.path.exists(docx_path):
        print(f"File not found: {docx_path}")
        sys.exit(1)

    print("Reading document...")
    text = extract_text(docx_path)

    print("Loading checklist...")
    checklist = load_checklist()

    print("Reviewing with AI...")
    result_md = review_against_standards(text, checklist)

    print("Saving results...")
    out_path = save_markdown(result_md)
    print(f"Done! Review saved to: {out_path}")

if __name__ == "__main__":
    main()
