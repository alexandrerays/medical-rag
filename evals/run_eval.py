"""Evaluation runner for MedReg MCP."""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.rag import answer_question
from evals.metrics import citation_present, keyword_recall, safety_correct, source_org_correct


async def run_evaluation():
    eval_path = Path(__file__).parent / "eval_questions.json"
    with open(eval_path) as f:
        questions = json.load(f)

    print(f"Running evaluation with {len(questions)} questions...\n")
    print(f"{'#':<3} {'Question':<60} {'Safety':<7} {'Cite':<5} {'KW':<5} {'Org':<4}")
    print("-" * 90)

    results = []
    for i, q in enumerate(questions, start=1):
        response = await answer_question(q["question"])

        safety_ok = safety_correct(response, q["is_medical_advice"])
        has_citation = citation_present(response) if not q["is_medical_advice"] else True
        kw_score = keyword_recall(response, q["expected_keywords"])
        org_ok = source_org_correct(response, q.get("expected_source_org"))

        results.append(
            {
                "question": q["question"],
                "safety_correct": safety_ok,
                "has_citation": has_citation,
                "keyword_recall": kw_score,
                "source_org_correct": org_ok,
            }
        )

        safety_mark = "OK" if safety_ok else "FAIL"
        cite_mark = "OK" if has_citation else "FAIL"
        org_mark = "OK" if org_ok else "FAIL"

        print(f"{i:<3} {q['question'][:58]:<60} {safety_mark:<7} {cite_mark:<5} {kw_score:<5.2f} {org_mark:<4}")

    print("\n" + "=" * 90)
    print("SUMMARY")
    print("=" * 90)

    total = len(results)
    safety_rate = sum(1 for r in results if r["safety_correct"]) / total
    citation_rate = sum(1 for r in results if r["has_citation"]) / total
    avg_keyword = sum(r["keyword_recall"] for r in results) / total
    org_rate = sum(1 for r in results if r["source_org_correct"]) / total

    print(f"  Safety accuracy:     {safety_rate:.0%} ({sum(1 for r in results if r['safety_correct'])}/{total})")
    print(f"  Citation presence:   {citation_rate:.0%} ({sum(1 for r in results if r['has_citation'])}/{total})")
    print(f"  Avg keyword recall:  {avg_keyword:.2f}")
    print(f"  Source org accuracy: {org_rate:.0%} ({sum(1 for r in results if r['source_org_correct'])}/{total})")
    print(f"\n  Overall score:       {(safety_rate + citation_rate + avg_keyword + org_rate) / 4:.2f}")


if __name__ == "__main__":
    asyncio.run(run_evaluation())
