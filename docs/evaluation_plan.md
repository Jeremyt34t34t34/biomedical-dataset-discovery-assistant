# Evaluation Plan

This document defines the initial evaluation approach for the Biomedical Dataset Discovery Assistant.

Evaluation should measure two separate parts of the system:

1. Retrieval: did the system find the right dataset records?
2. RAG answer quality: did the assistant explain the results correctly and safely?

Keeping these separate helps diagnose failures. A bad final answer may come from weak retrieval, incomplete metadata, or a poor prompt.

## Evaluation Scope

The first evaluation set should focus on dataset discovery, not general biomedical knowledge.

Initial scope:

- lung cancer
- NSCLC
- LUAD
- LUSC
- EGFR
- KRAS
- KRAS G12C
- RNA-seq
- mutation data
- clinical metadata

## Retrieval Evaluation

Retrieval evaluation checks whether expected dataset records appear in the top results.

Candidate metrics:

- `hit_rate_at_k`: whether at least one expected dataset appears in the top-k results
- `recall_at_k`: how many expected datasets were retrieved in the top-k results
- `precision_at_k`: how many retrieved results are relevant
- `source_coverage`: whether expected source systems appear in the results

For the first prototype, `hit_rate_at_5` and qualitative review are enough.

## Answer Evaluation

Answer evaluation checks whether the final RAG answer is useful, grounded, and honest about uncertainty.

The answer should:

- name relevant dataset IDs
- name the source systems
- explain why each dataset matches the query
- mention important available data types
- distinguish explicit evidence from inferred relevance
- include limitations when evidence is weak
- avoid medical advice or treatment recommendations

## Failure Diagnosis

When an answer is weak, diagnose the failure source:

```text
Wrong or missing datasets
-> retrieval problem

Right datasets, but metadata lacks enough detail
-> catalog/schema problem

Enough context, but vague or unsupported answer
-> prompt/RAG generation problem

Question requires patient-level data not in metadata
-> scope limitation
```

## Initial Evaluation Questions

These questions are also stored in `eval/questions_seed.json`.

1. What public datasets exist for NSCLC?
2. Which public datasets are available for lung adenocarcinoma?
3. Which datasets are available for lung squamous cell carcinoma?
4. Compare TCGA-LUAD and TCGA-LUSC.
5. Which datasets contain RNA-seq data for lung cancer?
6. Which datasets can support EGFR mutation research?
7. Which datasets can support KRAS mutation research?
8. What datasets are available for KRAS G12C research in NSCLC?
9. Which datasets include both clinical metadata and molecular data?
10. Which cBioPortal studies are relevant to NSCLC?

## Match Strength Guidance

Match strength should be calculated at query time.

Example:

```text
Query: What datasets are available for KRAS G12C research in NSCLC?
```

Possible labels:

- `strong`: metadata explicitly mentions KRAS G12C
- `medium`: dataset has KRAS or mutation data, but KRAS G12C-positive cases are not explicitly verified
- `weak`: dataset is lung cancer-related and has mutation profiling, but gene or variant relevance is not verified

The assistant may return medium or weak candidate datasets, but it must label uncertainty and explain limitations.

## Initial Evaluation File Shape

Each evaluation question should eventually include:

```json
{
  "id": "q001",
  "question": "What public datasets exist for NSCLC?",
  "expected_dataset_ids": ["gdc:TCGA-LUAD", "gdc:TCGA-LUSC"],
  "expected_sources": ["GDC"],
  "expected_keywords": ["NSCLC", "LUAD", "LUSC", "lung"],
  "answer_checks": [
    "mentions relevant dataset IDs",
    "explains why LUAD and LUSC are relevant to NSCLC",
    "does not provide medical advice"
  ]
}
```

This structure can be expanded after the seed catalog is created.
