# Biomedical Dataset Discovery Assistant

This project is an LLM Zoomcamp project for helping researchers discover public biomedical datasets relevant to diseases, genes, biomarkers, mutations, assays, and research questions.

The initial focus is dataset discovery and research data navigation, not clinical advice or biological interpretation. The system will combine structured metadata search with retrieval-augmented generation (RAG).

## Core Idea

Public biomedical datasets are spread across several platforms. A researcher may need to check GDC, cBioPortal, GEO, SRA, and other sources just to answer a practical question such as:

```text
What public datasets can support KRAS G12C research in NSCLC?
```

The goal of this project is not to replace those platforms. The goal is to create a lightweight discovery assistant that can:

- normalize dataset metadata from multiple sources
- search over that normalized catalog
- explain why a dataset is relevant
- separate confirmed evidence from inferred usefulness
- clearly state limitations when metadata is not enough

In other words, the assistant should help users find candidate datasets faster while staying honest about what has and has not been verified.

## Current Status

The project is currently in the planning and schema-design stage.

Completed so far:

- Project mission and MVP direction defined
- Initial biomedical/domain background summarized
- First data sources selected: GDC/TCGA and cBioPortal
- Deferred sources documented: GEO, SRA, Open Targets
- Professional `DatasetRecord` schema drafted
- Evidence-aware RAG behavior defined

Next step:

- Create the project skeleton, implement `DatasetRecord`, and build a small seed catalog.

## MVP User Scenario

The first user scenario is a professional or semi-professional research user looking for lung cancer datasets.

Example question:

```text
What datasets are available for KRAS G12C research in NSCLC?
```

The assistant should not simply return `TCGA-LUAD` or `TCGA-LUSC`. It should answer with evidence-aware reasoning:

```text
TCGA-LUAD is a candidate dataset because it is a lung adenocarcinoma dataset related to NSCLC and has mutation data availability.

However, the current catalog has not explicitly verified KRAS G12C-positive cases, so this should be treated as a candidate match rather than confirmed KRAS G12C cohort evidence.
```

This distinction is central to the project. The assistant should help with dataset discovery, not overclaim biological or clinical findings.

## Initial Scope

- Dataset sources: GDC/TCGA and cBioPortal first
- Later sources: GEO, SRA, Open Targets
- First disease area: lung cancer, especially NSCLC, LUAD, and LUSC
- First data types: RNA-seq, mutation, clinical metadata, copy number where available
- First interface: simple search/RAG prototype before a richer UI

## Data Source Strategy

The first version uses a small number of sources on purpose. The MVP should prove the workflow before expanding into harder metadata-cleaning problems.

### GDC / TCGA

GDC is the official cancer data portal for TCGA-style project and file metadata.

For this project, GDC is useful for proving:

- a cancer dataset exists
- its official project ID, such as `TCGA-LUAD` or `TCGA-LUSC`
- high-level disease and project metadata
- available data categories and file types
- whether data appears to include RNA-seq, mutation, clinical, or copy number information
- official source links

GDC is less convenient for quickly answering gene- or variant-specific questions such as whether a project explicitly contains KRAS G12C-positive cases.

### cBioPortal

cBioPortal is a cancer genomics study portal that is more convenient for gene, mutation, clinical, and molecular profile discovery.

For this project, cBioPortal is useful for proving:

- a cancer genomics study exists
- the study is related to a source dataset such as TCGA-LUAD or TCGA-LUSC
- mutation, expression, copy number, and clinical molecular profiles may be available
- the study is suitable for follow-up gene or mutation inspection

cBioPortal records may refer to the same biological study as GDC records, but they represent a different access and metadata layer. For example:

```text
gdc:TCGA-LUAD
cbioportal:luad_tcga_pan_can_atlas_2018
```

These should be stored as separate source-specific records and connected through a shared `canonical_dataset_id` such as `TCGA-LUAD`.

### Deferred Sources

GEO, SRA, and Open Targets are intentionally deferred from the first implementation.

- GEO is valuable but has noisier and less standardized study metadata.
- SRA is useful for raw sequencing run discovery but is too granular for the first dataset-discovery MVP.
- Open Targets is useful for gene-disease query expansion, but it is not primarily a dataset catalog.

The first prototype should focus on GDC and cBioPortal, then expand only after the normalized catalog, retrieval, and evaluation workflow are working.

## Evidence-Aware Matching

The assistant should not treat every match as equally strong. Match strength should depend on what the catalog has actually verified.

Example:

```text
Query: What datasets are available for KRAS G12C research in NSCLC?
```

Possible match levels:

- `strong`: metadata explicitly verifies KRAS G12C-positive cases or direct KRAS G12C evidence.
- `medium`: the dataset is NSCLC-related and has mutation profiling, but KRAS G12C-positive cases are not explicitly verified.
- `weak`: the dataset is lung cancer-related, but gene or variant relevance is only indirectly inferred.

This behavior is important because many dataset discovery questions involve incomplete metadata. The assistant should return useful candidates while labeling uncertainty.

## Project Principles

- Keep source-specific ingestion separate from the shared dataset catalog.
- Normalize all sources into a common dataset schema.
- Keep retrieval behind a replaceable interface so keyword, vector, and hybrid search can evolve independently.
- Start with a small, testable catalog before expanding source coverage.
- Create evaluation questions early so improvements can be measured.

## Planned MVP Build Order

The first implementation should stay small and runnable:

1. Create the project skeleton.
2. Implement `DatasetRecord`.
3. Create a manual seed catalog in `data/processed/seed_catalog.json`.
4. Add initial records:
   - `gdc:TCGA-LUAD`
   - `gdc:TCGA-LUSC`
   - `cbioportal:luad_tcga_pan_can_atlas_2018`
   - `cbioportal:lusc_tcga_pan_can_atlas_2018`
5. Build a simple keyword retriever over the normalized records.
6. Run retrieval evaluation using `eval/questions_seed.json`.
7. Add a minimal RAG answer layer that only answers from retrieved records.

## Current MVP Prototype

The repository now includes a first runnable retrieval prototype:

- `src/models.py`: normalized `DatasetRecord` and `EvidenceItem` models
- `src/catalog.py`: seed catalog loading and canonical dataset grouping
- `src/retriever.py`: simple keyword retriever with query expansion
- `data/processed/seed_catalog.json`: first curated seed catalog
- `evaluation/retrieval_eval.py`: retrieval evaluation script
- `tests/test_retriever.py`: smoke tests for retrieval and grouping behavior

The seed catalog currently includes GDC and cBioPortal source views for:

- `TCGA-LUAD`
- `TCGA-LUSC`
- `TCGA-BRCA` as a non-lung comparison dataset

Run retrieval evaluation:

```bash
PYTHONPATH=. python3 -m evaluation.retrieval_eval
```

Run tests:

```bash
PYTHONPATH=. python3 -m unittest discover -s tests
```

## Documents

- [Initial Project Investigation](docs/project_investigation.md)
- [Domain Background](docs/domain_background.md)
- [Data Sources](docs/data_sources.md)
- [Dataset Schema](docs/data_schema.md)
- [Project Status](docs/project_status.md)
- [Week 3 Meeting Prep](docs/week3_meeting_prep.md)
- [Evaluation Plan](docs/evaluation_plan.md)
