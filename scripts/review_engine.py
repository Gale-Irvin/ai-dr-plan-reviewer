import os, json, math
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

# ------------------------
# Initialization
# ------------------------
load_dotenv()
_api_key = os.getenv("OPENAI_API_KEY")
if not _api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in your .env file.")

client = OpenAI(api_key=_api_key)
INDEX_PATH = Path("standards_index/standards_index.jsonl")


# ------------------------
# Helper Functions
# ------------------------

def load_checklist(path="prompts/evaluation_checklist.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_markdown(md_text: str, out_dir="reviews"):
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(out_dir, f"dr_review_{ts}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md_text)
    return path

def embed_query(q: str):
    return client.embeddings.create(
        model="text-embedding-3-large",
        input=q
    ).data[0].embedding

def cosine_sim(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb + 1e-8)

def retrieve_relevant_controls(plan_text: str, top_k=12) -> List[Dict]:
    if not INDEX_PATH.exists():
        print("⚠️ No standards index found.")
        return []

    q_emb = embed_query(
        f"Controls or policies applicable to Disaster Recovery:\n{plan_text[:2000]}"
    )

    results = []
    with INDEX_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            sim = cosine_sim(q_emb, rec["embedding"])
            results.append((sim, rec))

    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results[:top_k]]


# ------------------------
# Main Review Function
# ------------------------

def review_against_standards(plan_text: str, checklist: str, model="gpt-4o-mini"):

    controls = retrieve_relevant_controls(plan_text, top_k=12)

    controls_text = "No controls retrieved."
    if controls:
        controls_text = "\n\n---\n".join(
            f"[{c['source']} :: {c['chunk_id']}]\n{c['text']}"
            for c in controls
        )

    print(f"Retrieved {len(controls)} control chunks for this review.")

    system_prompt = (
        checklist +
        "\n\nYou are performing an evidence-based verification.\n"
        "- You MUST use ONLY the provided control excerpts/policy text as authority.\n"
        "- EVERY finding MUST include a [source :: chunk_id] citation.\n"
        "- If no control applies, use [no matching control].\n"
    )

    user_prompt = (
        "DR PLAN (excerpt):\n"
        f"{plan_text[:12000]}\n\n"
        "REFERENCE CONTROLS/POLICY EXCERPTS (reuse [source :: chunk_id] labels exactly):\n"
        f"{controls_text}\n\n"
        "TASK: Cross-check the DR plan against the controls.\n"
        "Produce, in Markdown:\n"
        "1) A findings table with EXACTLY these columns:\n"
        "   | Finding | Evidence from DR Plan | Control evidence [source :: chunk_id] | Severity | Recommendation |\n"
        "2) Top 10 remediation actions with first steps.\n"
        "3) A readiness score (0–100) + how to reach 90+.\n"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
