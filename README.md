# AI-Augmented Disaster Recovery (DR) Plan Reviewer  
*A standards-assisted DR Plan analysis tool using Python, embeddings, and OpenAI models.*

---

## 📌 Overview  

This project automates the review of Disaster Recovery (DR) Plans by using AI to:

- Extract text from a DR plan document (.docx)  
- Retrieve relevant requirements from standards or policies (HITRUST summaries, NIST SP 800-34, internal policies, etc.)  
- Compare the DR Plan to those standards  
- Generate:
  - A findings table with severity ratings  
  - Evidence-based citations  
  - Prioritized remediation recommendations  
  - A readiness score (0–100)

This tool supports **Risk**, **Resilience**, **BCP/DR**, **Audit**, and **Compliance** teams wanting a faster and more consistent method to evaluate documentation.

---

## 🧠 How It Works  

This project uses a **Retrieval-Augmented Generation (RAG)** workflow:

### **1. Ingest Standards/Policies**
Place `.docx`, `.txt`, or `.pdf` documents into the `standards/` folder.

Example standards you can use:

- NIST SP 800-34  
- NIST 800-53 (CP controls)  
- Internal DR policies  
- HITRUST summaries you create  

The ingestion script converts them to embeddings and stores them in `standards_index/`.

---

### **2. Extract DR Plan Text**
The tool loads `.docx` DR plans from the `data/` folder.

---

### **3. Retrieve Matching Controls**
- DR plan text is embedded  
- Most relevant chunks from standards are retrieved from the index  

---

### **4. AI Analysis**
The OpenAI model (`gpt-4o-mini` by default):

- Reviews the DR plan against retrieved controls  
- Generates findings  
- Provides citations  
- Produces a remediation plan  
- Assigns a readiness score  

---

### **5. Output**
- A Markdown report is saved into `reviews/`  
- Includes inline citations like:

```
[HITRUST_DR_Summary.docx :: chunk0]
```

---

## 🚀 Features  

- DR Plan text extraction (`.docx`)  
- Standards/policies ingestion  
- Local embeddings index  
- Evidence-based findings  
- Inline control citations  
- Readiness scoring  
- Markdown reporting  
- Extensible to NIST, ISO, HITRUST summaries, internal controls  

---

## 📁 Project Structure  

```
ai_dr_reviewer/
│
├── scripts/
│   ├── review_engine.py        # Main AI review logic
│   ├── standards_ingest.py     # Embeds standards/policies
│   ├── plan_parser.py          # Extracts DR plan text
│   └── review_cli.py           # Command-line runner
│
├── standards/                  # Place your standards/policy documents here
├── standards_index/            # Auto-generated embeddings index
├── data/                       # Place DR plans here (.docx)
├── reviews/                    # AI-generated reports
└── prompts/
    └── evaluation_checklist.txt
```

---

## 🛠 Requirements  

- Python 3.10+  
- pip  
- OpenAI Python SDK  
- python-docx  
- python-dotenv  
- pypdf (optional, for PDF parsing)

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## 🔑 API Key & Billing Notice  

This project requires **OpenAI API** access.

⚠ **ChatGPT Plus does *not* include API credits.**  
You must configure pay-as-you-go billing:

👉 https://platform.openai.com/account/billing/overview

Set your API key:

Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-xxxxx
```

---

## 📥 Ingesting Standards / Policies  

Place files into:

```
standards/
```

Run ingestion:

```bash
python scripts/standards_ingest.py
```

This generates:

```
standards_index/standards_index.jsonl
```

---

## 📄 Running a DR Plan Review  

Place your DR plan into:

```
data/
```

Run:

```bash
python scripts/review_cli.py data/your_plan.docx
```

Expected output:

```
Reading document...
Loading checklist...
Retrieved X control chunks for this review.
Saving results...
Done! Review saved to: reviews/dr_review_YYYYMMDD-HHMMSS.md
```

---

## 🌐 Compatible Frameworks  

You may ingest any of the following (if you have permission):

- ✔ NIST SP 800-34  
- ✔ NIST 800-53 CP controls  
- ✔ Internal DR/BCP policies  
- ✔ HITRUST summaries you create  
- ✔ ISO 22301 summaries you create  

⚠ Do NOT ingest copyrighted frameworks without redistribution rights.

---

## 🧩 Extending the Tool  

- Add a Streamlit UI  
- Export to Excel or PDF  
- Add scoring logic  
- Add dashboards  
- Add vendor dependency mapping  
- Integrate with SIEM/SOAR pipelines  

---

## 📘 License  

MIT License — Free to modify and extend with attribution.

---

## 💬 Maintainer  

**Gale Irvin**  
LinkedIn: (Add your profile link)
