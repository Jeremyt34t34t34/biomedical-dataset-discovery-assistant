# Domain Background

This document explains the minimum biomedical and data-domain background needed for the Biomedical Dataset Discovery Assistant project.

The goal is not to become a biomedical expert. The goal is to understand enough public dataset metadata to build a useful retrieval and RAG system.

## What Is Public Metadata?

Public metadata is descriptive information about a public dataset.

It is not usually the full raw biomedical data. Instead, it is the catalog information that helps a researcher decide whether a dataset is relevant.

Example metadata fields:

```text
dataset_id: TCGA-LUAD
source: GDC / TCGA
title: Lung Adenocarcinoma
disease: lung adenocarcinoma
primary_site: lung
sample_count: 500+
data_types: RNA-seq, mutation, clinical, copy number
organism: human
access_level: open / controlled
url: ...
```

The real dataset may contain gene expression matrices, mutation files, clinical tables, or sequencing files. Metadata describes those resources without requiring us to download all of them.

For this project, metadata is the first thing to collect and search.

## Metadata vs Raw Data

Think of biomedical public data like a library:

- Raw data is the book content.
- Metadata is the catalog card.
- The assistant is the research librarian that helps users find the right books.

The first version of this project should answer questions like:

- Which datasets exist?
- What disease do they cover?
- What data types do they include?
- Which genes or mutations are relevant?
- Where can the researcher access the dataset?

It should not initially answer questions that require analyzing raw expression values or patient-level outcomes.

## Key Dataset Sources

### TCGA

TCGA stands for The Cancer Genome Atlas.

It is a major cancer genomics program with public datasets for many cancer types. TCGA project IDs are commonly used in cancer research.

Examples:

- TCGA-LUAD: lung adenocarcinoma
- TCGA-LUSC: lung squamous cell carcinoma
- TCGA-BRCA: breast invasive carcinoma

For this project, TCGA is useful because its project names, cancer types, and data categories are well-known and easy to explain.

### GDC

GDC stands for Genomic Data Commons.

It is a platform from the National Cancer Institute for accessing cancer genomics data, including TCGA data. GDC provides structured APIs for projects, cases, files, and annotations.

For this project, GDC is useful as an official source of TCGA metadata.

### cBioPortal

cBioPortal is a cancer genomics data portal.

It provides study-level and sample-level information, including clinical data, mutations, molecular profiles, and cancer types.

For this project, cBioPortal is especially useful for questions like:

- Which studies contain mutation data?
- Which studies may support EGFR or KRAS research?
- Which molecular profiles are available for a study?

### GEO

GEO stands for Gene Expression Omnibus.

It is a broad public repository for gene expression and functional genomics datasets. GEO covers many diseases, organisms, platforms, and study designs.

For this project, GEO is valuable but should come after the first MVP because the metadata is less standardized.

### SRA

SRA stands for Sequence Read Archive.

It stores raw sequencing data. Its metadata often uses several levels, such as study, sample, experiment, and run.

For this project, SRA is useful later if we want sequencing-run discovery, but it is too granular for the first MVP.

### Open Targets

Open Targets is a platform for disease, gene, target, drug, variant, and study relationships.

It is not mainly a dataset catalog. It can help with query expansion, such as connecting a gene to a disease area.

For this project, Open Targets should be a supporting knowledge source rather than the first source of dataset records.

## Important Data Levels

Biomedical repositories often organize information in levels.

### Project or Study

A project or study is the broad dataset unit.

Examples:

- TCGA-LUAD
- TCGA-LUSC
- A cBioPortal lung cancer study
- A GEO series accession such as GSE...

This is usually the best level for dataset discovery.

### Case or Patient

A case or patient is one person represented in the dataset.

Clinical metadata often belongs to this level.

Examples:

- diagnosis
- age
- sex
- tumor stage
- survival information

### Sample

A sample is biological material collected from a patient, organism, or experiment.

Examples:

- tumor sample
- normal tissue sample
- blood sample
- cell line sample

A patient may have more than one sample.

### File

A file is a downloadable data resource.

Examples:

- RNA-seq count file
- mutation file
- copy number file
- clinical table

Some questions require file-level metadata, especially questions about whether a study includes RNA-seq, mutation, or clinical data.

## Lung Cancer Terms for the MVP

The first MVP should focus on lung cancer because it provides clear example questions and well-known public datasets.

### NSCLC

NSCLC means non-small cell lung cancer.

It is a broad category that includes multiple lung cancer subtypes.

For this project, NSCLC queries should often retrieve or discuss both LUAD and LUSC.

### LUAD

LUAD means lung adenocarcinoma.

TCGA-LUAD is the TCGA project for lung adenocarcinoma.

### LUSC

LUSC means lung squamous cell carcinoma.

TCGA-LUSC is the TCGA project for lung squamous cell carcinoma.

## Gene, Mutation, and Biomarker Terms

### Gene

A gene is a unit of DNA that can be associated with biological function or disease.

Examples in this project:

- EGFR
- KRAS

### Mutation or Variant

A mutation or variant is a change in DNA sequence.

Examples:

- EGFR mutation
- KRAS mutation
- KRAS G12C

For dataset discovery, the assistant does not need to interpret treatment decisions. It only needs to find datasets that may include mutation data relevant to these genes or variants.

### Biomarker

A biomarker is a measurable biological feature that may be relevant to disease, prognosis, treatment response, or research grouping.

Examples:

- mutation status
- gene expression
- protein expression
- methylation pattern

In this project, biomarker queries should usually map to dataset metadata fields such as genes, mutations, data types, assays, or molecular profiles.

## Common Data Types

### RNA-seq

RNA-seq measures gene expression.

Dataset discovery questions about RNA-seq usually ask whether a dataset includes gene expression data.

### Mutation Data

Mutation data describes genetic variants observed in samples or patients.

In cancer genomics, mutation data may appear as MAF files, variant calls, or cBioPortal mutation profiles.

### Clinical Metadata

Clinical metadata describes patient or case-level information.

Examples:

- diagnosis
- cancer type
- stage
- sex
- age
- survival fields

### Copy Number Data

Copy number data describes gains or losses of DNA regions.

cBioPortal often uses terms such as CNA or copy number alteration.

### Methylation

Methylation data describes DNA methylation patterns.

This is useful in some cancer studies but not necessary for the first MVP.

### Proteomics

Proteomics data measures proteins.

This can be useful later, but it is not necessary for the first MVP.

## What the Assistant Should Answer

The assistant should answer dataset discovery questions with grounded, practical information.

Good answer structure:

```text
Relevant datasets:
- Dataset ID and source
- Why it matches the query
- Available data types
- Useful notes or limitations
- Link or accession
```

Example:

```text
TCGA-LUAD is relevant for lung adenocarcinoma research. It is available through GDC and commonly includes molecular and clinical data such as RNA-seq, mutation, copy number, and clinical metadata. It is relevant to NSCLC because LUAD is a major NSCLC subtype.
```

## What the Assistant Should Avoid

The assistant should avoid:

- giving medical advice
- making treatment recommendations
- claiming a dataset contains a specific mutation unless metadata or retrieved evidence supports it
- pretending to analyze raw files when it only searched metadata
- giving confident answers without naming the dataset source

## First MVP Knowledge Checklist

Before building the first prototype, we should be comfortable with:

- What public metadata is
- Why metadata is different from raw biomedical data
- What TCGA, GDC, and cBioPortal provide
- What NSCLC, LUAD, and LUSC mean
- What EGFR, KRAS, and KRAS G12C represent
- What RNA-seq, mutation, and clinical metadata mean
- Why dataset discovery is a retrieval problem

This is enough domain background to start designing the first catalog schema and retrieval prototype.
