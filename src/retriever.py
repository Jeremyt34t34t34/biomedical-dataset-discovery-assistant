"""Small keyword retriever for the first seed catalog."""

from __future__ import annotations

import re
from dataclasses import dataclass

from src.models import DatasetRecord


TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)?")

STOPWORDS = {
    "are",
    "both",
    "can",
    "catalog",
    "comparison",
    "contain",
    "currently",
    "data",
    "dataset",
    "datasets",
    "exist",
    "for",
    "in",
    "include",
    "is",
    "metadata",
    "of",
    "profiles",
    "provide",
    "public",
    "research",
    "studies",
    "study",
    "support",
    "the",
    "to",
    "what",
    "which",
    "with",
}

SYNONYMS: dict[str, set[str]] = {
    "nsclc": {
        "nsclc",
        "non-small cell lung cancer",
        "non small cell lung cancer",
        "luad",
        "lusc",
        "lung adenocarcinoma",
        "lung squamous cell carcinoma",
    },
    "expression": {"expression", "rna-seq", "rna seq", "mrna"},
    "rna-seq": {"rna-seq", "rna seq", "expression", "mrna"},
    "mutation": {"mutation", "mutations", "simple nucleotide variation", "snv"},
    "molecular": {"molecular", "mutation", "expression", "copy number"},
    "clinical": {"clinical", "diagnosis", "tumor stage", "survival"},
    "cbioportal": {"cbioportal", "cbio portal"},
    "gdc": {"gdc", "genomic data commons"},
}


@dataclass(frozen=True)
class RetrievalResult:
    record: DatasetRecord
    score: float
    matched_terms: list[str]


def normalize_text(text: str) -> str:
    return text.lower().replace("_", " ")


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in TOKEN_PATTERN.findall(normalize_text(text))
        if token not in STOPWORDS
    }


def expand_query(query: str) -> set[str]:
    normalized = normalize_text(query)
    terms = tokenize(normalized)
    for trigger, expansions in SYNONYMS.items():
        if trigger in normalized or trigger in terms:
            for expansion in expansions:
                terms.update(tokenize(expansion))
    return terms


def score_record(query_terms: set[str], record: DatasetRecord) -> tuple[float, list[str]]:
    text = normalize_text(record.searchable_text())
    record_terms = tokenize(text)
    matched_terms = sorted(term for term in query_terms if term in record_terms)

    score = float(len(matched_terms))

    for phrase in [
        "breast cancer",
        "lung cancer",
        "lung adenocarcinoma",
        "lung squamous cell carcinoma",
        "non-small cell lung cancer",
        "kras g12c",
        "rna-seq",
        "copy number",
    ]:
        if phrase in query_terms:
            continue
        if phrase in text and all(token in query_terms for token in tokenize(phrase)):
            score += 5.0

    if normalize_text(record.dataset_id) in text:
        score += 0.0
    if "cbioportal" in query_terms and normalize_text(record.source) == "cbioportal":
        score += 4.0
    if "gdc" in query_terms and normalize_text(record.source) == "gdc":
        score += 4.0
    if "mutation" in query_terms and record.has_mutation:
        score += 2.0
    if ("rna-seq" in query_terms or "expression" in query_terms) and record.has_expression:
        score += 2.0
    if "clinical" in query_terms and record.has_clinical:
        score += 2.0
    if "copy" in query_terms and "number" in query_terms and record.has_copy_number:
        score += 2.0

    return score, matched_terms


def search(
    query: str,
    records: list[DatasetRecord],
    top_k: int = 5,
) -> list[RetrievalResult]:
    query_terms = expand_query(query)
    results: list[RetrievalResult] = []

    for record in records:
        score, matched_terms = score_record(query_terms, record)
        if score > 0:
            results.append(
                RetrievalResult(
                    record=record,
                    score=score,
                    matched_terms=matched_terms,
                )
            )

    return sorted(
        results,
        key=lambda result: (
            result.score,
            result.record.canonical_dataset_id,
            result.record.source,
        ),
        reverse=True,
    )[:top_k]
