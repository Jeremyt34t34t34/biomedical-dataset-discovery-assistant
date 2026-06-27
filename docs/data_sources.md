# Data Sources

This document defines the first data sources for the Biomedical Dataset Discovery Assistant and explains which sources are intentionally deferred.

## Source Selection Principles

The first version should prefer sources that are:

- public or programmatically accessible
- relevant to cancer dataset discovery
- metadata-rich enough for retrieval
- structured enough to normalize into a shared schema
- small enough to support a working MVP quickly

The goal is not to collect every biomedical dataset at once. The goal is to build a reliable discovery workflow that can expand source by source.

## Phase 1 Sources

### GDC / TCGA

Status: included in MVP.

Why this source:

- TCGA cancer projects are well-known and useful for discovery examples.
- GDC exposes structured metadata for projects, cases, files, and annotations.
- It supports questions about cancer type, data category, data type, experimental strategy, access level, and available files.

Initial use:

- Use GDC as the official metadata source for TCGA projects.
- Start with lung cancer projects:
  - TCGA-LUAD
  - TCGA-LUSC
- Optionally include TCGA-BRCA as a non-lung comparison example.

Useful metadata levels:

- project level for dataset identity
- case level for case counts and disease information
- file level for available data types such as RNA-seq, mutation, copy number, and clinical data

Initial records should avoid downloading large genomic files. The MVP only needs metadata and links.

### cBioPortal

Status: included in MVP.

Why this source:

- cBioPortal is strong for cancer genomics study discovery.
- It is useful for molecular profiles, mutations, clinical attributes, sample counts, and study-level metadata.
- It helps answer gene- and mutation-oriented questions better than project-only catalogs.

Initial use:

- Collect a small set of lung cancer studies.
- Record available molecular profiles, clinical data, mutation data, and study URLs.
- Use cBioPortal records alongside GDC/TCGA records in the shared catalog.

Useful metadata levels:

- study level for dataset identity
- cancer type level for disease grouping
- sample/patient level for counts
- molecular profile level for available data modalities
- mutation profile availability for gene-oriented queries

## Phase 2 Sources

### GEO

Status: deferred until after MVP retrieval works.

Why defer:

- GEO has broad coverage but less standardized metadata.
- Disease names, platforms, sample annotations, and assay labels often require cleaning.
- Adding it too early could turn the project into a metadata-cleaning project before the RAG pipeline works.

Future use:

- Add selected GEO studies as curated records first.
- Later add programmatic ingestion through NCBI tools.

### SRA

Status: deferred until later expansion.

Why defer:

- SRA is sequencing-run oriented.
- It introduces several granular levels: study, sample, experiment, and run.
- It is better for raw sequencing discovery than first-pass dataset discovery.

Future use:

- Add only when the assistant needs run-level sequencing metadata.

### Open Targets

Status: supporting knowledge source, not a primary dataset source.

Why defer as catalog source:

- Open Targets is not primarily a dataset catalog.
- It is more useful for gene-disease-target relationships.

Future use:

- Query expansion: map genes, variants, and diseases to related terms.
- Explanation support: help users understand why a gene or disease term is related to a dataset search.

## MVP Source Scope

The first implementation should contain a small seed catalog from:

- GDC/TCGA
- cBioPortal

Initial disease scope:

- NSCLC
- lung adenocarcinoma
- lung squamous cell carcinoma

Initial project/study examples:

- TCGA-LUAD
- TCGA-LUSC
- a small number of cBioPortal lung cancer studies

Initial query concepts:

- NSCLC
- LUAD
- LUSC
- EGFR
- KRAS
- KRAS G12C
- RNA-seq
- mutation
- clinical metadata

## Source Abstraction Rule

Each source should have its own ingestion logic, but all sources must output the same normalized `DatasetRecord`.

Example:

```text
GDC project metadata       -> GDC loader       -> DatasetRecord
cBioPortal study metadata -> cBioPortal loader -> DatasetRecord
GEO series metadata       -> GEO loader       -> DatasetRecord
```

Retrieval and RAG should only depend on `DatasetRecord`, not on GDC-specific or cBioPortal-specific response formats.
