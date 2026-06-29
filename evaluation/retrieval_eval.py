"""Run retrieval evaluation against the seed catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from src.catalog import load_catalog
from src.retriever import search


DEFAULT_QUESTIONS_PATH = Path("eval/questions_seed.json")


def load_questions(path: Path | str = DEFAULT_QUESTIONS_PATH) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate(top_k: int = 5) -> dict[str, Any]:
    records = load_catalog()
    questions = load_questions()
    results = []

    for question in questions:
        retrieved = search(question["question"], records, top_k=top_k)
        retrieved_ids = [result.record.dataset_id for result in retrieved]
        expected_ids = question.get("expected_dataset_ids", [])
        expected_sources = question.get("expected_sources", [])

        dataset_hit = (
            any(dataset_id in retrieved_ids for dataset_id in expected_ids)
            if expected_ids
            else True
        )
        source_hit = (
            any(result.record.source in expected_sources for result in retrieved)
            if expected_sources
            else True
        )

        results.append(
            {
                "id": question["id"],
                "question": question["question"],
                "expected_dataset_ids": expected_ids,
                "retrieved_dataset_ids": retrieved_ids,
                "dataset_hit": dataset_hit,
                "source_hit": source_hit,
                "top_results": [
                    {
                        "dataset_id": result.record.dataset_id,
                        "canonical_dataset_id": result.record.canonical_dataset_id,
                        "source": result.record.source,
                        "score": result.score,
                        "matched_terms": result.matched_terms,
                    }
                    for result in retrieved
                ],
            }
        )

    dataset_hits = sum(1 for result in results if result["dataset_hit"])
    source_hits = sum(1 for result in results if result["source_hit"])
    total = len(results)

    return {
        "top_k": top_k,
        "questions": total,
        "dataset_hit_rate": dataset_hits / total if total else 0.0,
        "source_hit_rate": source_hits / total if total else 0.0,
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = evaluate(top_k=args.top_k)
    if args.json:
        print(json.dumps(report, indent=2))
        return

    print("Seed catalog retrieval evaluation")
    print(f"Questions: {report['questions']}")
    print(f"Top K: {report['top_k']}")
    print(f"Dataset hit rate: {report['dataset_hit_rate']:.2f}")
    print(f"Source hit rate: {report['source_hit_rate']:.2f}")
    print()

    for result in report["results"]:
        status = "PASS" if result["dataset_hit"] and result["source_hit"] else "FAIL"
        print(f"{status} {result['id']}: {result['question']}")
        for item in result["top_results"][:3]:
            print(
                "  "
                f"{item['dataset_id']} "
                f"({item['source']}, score={item['score']:.1f})"
            )
        print()


if __name__ == "__main__":
    main()
