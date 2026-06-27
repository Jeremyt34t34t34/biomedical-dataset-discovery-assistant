# Week 3 Meeting Prep

This document maps the Biomedical Dataset Discovery Assistant project to the Week 3 theme:

```text
Project Definition -> Knowledge Base Construction
```

## Project Summary

Project: Biomedical Dataset Discovery Assistant

Goal:

Help professional research users discover public biomedical datasets relevant to diseases, genes, biomarkers, mutations, data types, and research questions.

Core problem:

Public biomedical datasets are distributed across multiple platforms. Each platform has different metadata structures, terminology, and search workflows. The assistant will normalize metadata across sources and help users identify candidate datasets with evidence and limitations.

## Repository Setup

Status: started.

Current repository contains planning and design documentation:

- `README.md`
- `docs/project_investigation.md`
- `docs/domain_background.md`
- `docs/data_sources.md`
- `docs/data_schema.md`
- `docs/project_status.md`
- `docs/week3_meeting_prep.md`
- `docs/evaluation_plan.md`
- `eval/questions_seed.json`

Implementation files have not started yet, but the initial evaluation question seed file has been created.

## Primary RAG Document Sources

These are documentation sources that can be collected, chunked, and indexed for RAG support.

### Phase 1 Documentation

- GDC API and data model documentation
- GDC project, case, file, and annotation documentation
- cBioPortal API documentation
- cBioPortal study, sample, mutation, molecular profile, and clinical data documentation

### Phase 2 Documentation

- GEO programmatic access documentation
- NCBI Entrez / E-utilities documentation for GEO DataSets
- SRA metadata and accession documentation
- Open Targets Platform API documentation

The first RAG prototype should prioritize GDC and cBioPortal documentation. GEO, SRA, and Open Targets should remain planned extensions.

## Structured Data Sources

These are metadata sources that can become structured records in the dataset catalog.

### Phase 1 Structured Sources

- GDC/TCGA project metadata
- GDC case metadata
- GDC file metadata
- cBioPortal study metadata
- cBioPortal molecular profile metadata
- cBioPortal clinical/sample metadata where available

### Phase 2 Structured Sources

- GEO dataset or series metadata
- SRA study/sample/experiment/run metadata
- Open Targets disease-gene-target relationship data for query expansion

## Knowledge Base Design

The knowledge base will have two complementary parts.

### 1. Dataset Catalog

Structured metadata records normalized into `DatasetRecord`.

Used for:

- dataset discovery
- filtering
- ranking
- evidence-based RAG answers
- evaluation

### 2. Documentation Index

Chunked documentation from GDC, cBioPortal, and later sources.

Used for:

- explaining source-specific fields
- explaining data access details
- answering questions about platform terminology
- supporting RAG answers when metadata alone is not enough

The first prototype should mainly answer from the dataset catalog and use documentation as supporting context.

## Ingestion Strategy

### Step 1: Seed Catalog

Manually create a small seed catalog using the normalized schema.

Initial records:

- `gdc:TCGA-LUAD`
- `gdc:TCGA-LUSC`
- one or more cBioPortal lung cancer studies

Purpose:

- validate schema
- build the first retriever
- create evaluation examples
- avoid getting blocked by API complexity too early

### Step 2: Source-Specific Loaders

Implement separate loaders for each source:

```text
GDC metadata       -> GDC loader       -> DatasetRecord
cBioPortal metadata -> cBioPortal loader -> DatasetRecord
GEO metadata       -> GEO loader       -> DatasetRecord
```

Retrieval and RAG should only depend on `DatasetRecord`, not source-specific API responses.

### Step 3: Documentation Collection

Collect and chunk selected official documentation pages for GDC and cBioPortal.

Store chunks separately from dataset records so the system can distinguish:

- dataset evidence
- platform/documentation explanation

## Retrieval Strategy

### First Version

Use keyword retrieval over normalized dataset records.

Searchable fields:

- dataset ID
- title
- description
- diseases
- cancer types
- primary sites
- cohort tags
- data types
- assays
- molecular profiles
- explicit and inferred genes
- explicit and inferred mutations
- limitations

### Later Versions

Add:

- vector search
- hybrid retrieval
- metadata filters
- reranking
- query expansion using disease and gene synonyms

## Evaluation Planning

Evaluation should be split into retrieval evaluation and answer evaluation.

### Retrieval Evaluation

Measure whether the system retrieves expected dataset records.

Possible metrics:

- top-k hit rate
- recall@k
- precision@k for curated questions
- whether expected source appears in retrieved results

### Answer Evaluation

Measure whether the final RAG answer is useful and safe.

Checks:

- names relevant dataset IDs
- explains why each dataset matches
- mentions data types
- distinguishes explicit evidence from inferred relevance
- includes limitations when evidence is weak
- avoids unsupported medical or treatment claims

## Example User Questions

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

## Potential Evaluation Questions

Initial evaluation questions can reuse the example questions, but each should include expected records or expected concepts.

Example evaluation record:

```json
{
  "question": "What datasets are available for KRAS G12C research in NSCLC?",
  "expected_dataset_ids": ["gdc:TCGA-LUAD", "gdc:TCGA-LUSC"],
  "expected_keywords": ["NSCLC", "KRAS", "mutation", "lung"],
  "expected_behavior": [
    "returns candidate datasets",
    "labels KRAS G12C evidence as not explicitly verified unless metadata supports it",
    "mentions limitations"
  ]
}
```

## Architecture Alignment

Planned flow:

```text
source APIs / seed metadata
-> source-specific ingestion
-> normalized DatasetRecord catalog
-> retrieval index
-> retrieved dataset context
-> RAG answer with evidence and limitations
-> evaluation
-> UI
```

Key architecture principle:

```text
source-specific ingestion can change
DatasetRecord should stay stable
retrieval and RAG should depend on DatasetRecord
```

## Week 4 Deliverables

Target deliverables:

- Repository initialized with planning docs
- Project skeleton created
- `DatasetRecord` model implemented
- small seed catalog created
- 5-10 dataset discovery evaluation questions refined against the seed catalog
- initial keyword retrieval prototype working
- first RAG prompt drafted
- clear distinction between dataset metadata context and documentation context

## Current Gaps Before Week 4

Needs implementation:

- project skeleton
- `src/models.py`
- seed catalog JSON
- retrieval code
- evaluation file
- RAG prompt and pipeline

Needs refinement:

- exact cBioPortal study IDs for the first seed catalog
- exact GDC fields to fetch during API ingestion
- final retrieval metrics for the first evaluation script
