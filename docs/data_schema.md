# Dataset Schema

This document defines the normalized metadata schema for the Biomedical Dataset Discovery Assistant.

The schema is intentionally professional enough to support a real system, but still scoped to dataset discovery. It does not try to store raw biomedical data.

## Design Goal

All source-specific metadata should be converted into a common record called `DatasetRecord`.

The retriever, RAG pipeline, evaluation scripts, and UI should work with `DatasetRecord` objects instead of directly depending on GDC, cBioPortal, GEO, or SRA response formats.

The most important design rule:

```text
source-specific ingestion can be messy
normalized DatasetRecord should be stable
retrieval and RAG should only depend on DatasetRecord
```

## Schema Strategy

The schema has two layers:

1. A shared discovery layer used by retrieval, RAG, evaluation, and UI.
2. A source-specific preservation layer that stores details from GDC, cBioPortal, GEO, SRA, or future sources.

This avoids two bad extremes:

- Too simple: cannot explain why a dataset matched a query.
- Too complex: every new source requires a painful schema redesign.

## DatasetRecord V1

### 1. Identity

These fields identify the record and prevent conflicts across sources.

```text
schema_version
dataset_id
canonical_dataset_id
source
source_record_id
source_url
title
description
```

Field meanings:

- `schema_version`: version of this normalized schema, starting with `1`
- `dataset_id`: globally unique record ID, such as `gdc:TCGA-LUAD` or `cbioportal:luad_tcga_pan_can_atlas_2018`
- `canonical_dataset_id`: shared ID for related records across sources, such as `TCGA-LUAD`
- `source`: source system, such as `GDC`, `cBioPortal`, `GEO`, or `SRA`
- `source_record_id`: source-native ID, such as `TCGA-LUAD` or a cBioPortal study ID
- `source_url`: source link where a user can inspect the dataset
- `title`: human-readable dataset or study title
- `description`: short text summary for retrieval and RAG context

Why both `dataset_id` and `canonical_dataset_id` exist:

```text
gdc:TCGA-LUAD                         -> canonical_dataset_id: TCGA-LUAD
cbioportal:luad_tcga_pan_can_atlas_2018 -> canonical_dataset_id: TCGA-LUAD
```

The first version treats these as separate source-specific records, but can still show that they refer to related biological data.

### 2. Biomedical Context

These fields describe what disease, tissue, organism, or cohort the dataset represents.

```text
diseases
cancer_types
primary_sites
organisms
cohort_tags
```

Field meanings:

- `diseases`: broad disease terms, such as `non-small cell lung cancer`
- `cancer_types`: cancer-specific labels, such as `lung adenocarcinoma`, `LUAD`, or `LUSC`
- `primary_sites`: anatomical sites, such as `lung`
- `organisms`: organisms represented in the data, usually `Homo sapiens` for the MVP
- `cohort_tags`: practical search labels, such as `NSCLC`, `TCGA`, `adult`, or `tumor`

These fields help the system map a user query like `NSCLC datasets` to records involving LUAD and LUSC.

### 3. Data Availability

These fields describe what kinds of data the dataset appears to contain.

```text
data_types
data_categories
assays
molecular_profiles
has_clinical
has_expression
has_mutation
has_copy_number
has_methylation
clinical_attributes
```

Field meanings:

- `data_types`: user-facing categories, such as `RNA-seq`, `mutation`, `clinical`, `copy number`
- `data_categories`: source-facing broad categories, such as GDC `Transcriptome Profiling`
- `assays`: experimental strategies or technologies, such as `RNA-Seq`, `WXS`, or `WGS`
- `molecular_profiles`: platform-specific profile names, especially useful for cBioPortal
- `has_clinical`: whether clinical metadata appears to be available
- `has_expression`: whether gene expression data appears to be available
- `has_mutation`: whether mutation data appears to be available
- `has_copy_number`: whether copy number data appears to be available
- `has_methylation`: whether methylation data appears to be available
- `clinical_attributes`: known clinical fields, such as `diagnosis`, `tumor stage`, or `survival`, when available

The boolean fields support filtering and UI controls. The list fields preserve richer detail.

### 4. Biomarker Context

Gene and mutation fields must distinguish explicit evidence from inferred usefulness.

```text
explicit_genes
inferred_genes
explicit_mutations
inferred_mutations
biomarker_notes
```

Field meanings:

- `explicit_genes`: genes explicitly mentioned by source metadata or curated evidence
- `inferred_genes`: genes inferred as relevant because the dataset has suitable disease and data availability
- `explicit_mutations`: mutations explicitly mentioned by source metadata or curated evidence
- `inferred_mutations`: mutations inferred as potentially relevant, but not directly verified in metadata
- `biomarker_notes`: short explanation of biomarker relevance and uncertainty

Example:

```text
KRAS G12C query
```

Possible match levels:

- Strong: metadata explicitly mentions `KRAS G12C`
- Medium: metadata supports KRAS mutation analysis but does not explicitly mention G12C
- Weak: lung cancer dataset has mutation profiling, but KRAS availability is not verified

This prevents the assistant from claiming more certainty than the metadata supports.

### 5. Cohort Summary

These fields describe size, access, and high-level availability.

```text
case_count
sample_count
access_level
study_design
publication_ids
external_ids
```

Field meanings:

- `case_count`: number of cases or patients, if available
- `sample_count`: number of biological samples, if available
- `access_level`: `open`, `controlled`, `mixed`, or `unknown`
- `study_design`: short label or description, if available
- `publication_ids`: PubMed IDs, DOIs, or publication references
- `external_ids`: related IDs such as project IDs, accessions, or API IDs

`case_count` and `sample_count` should remain separate because one patient can contribute multiple biological samples.

### 6. Evidence and Limitations

These fields make the RAG answer safer and more professional.

```text
evidence_level
evidence_items
limitations
curation_status
last_verified
```

Field meanings:

- `evidence_level`: overall confidence, such as `source_metadata`, `curated`, `inferred`, or `unknown`
- `evidence_items`: specific facts used to justify retrieval and answers
- `limitations`: what is missing, uncertain, or not yet verified
- `curation_status`: `seed`, `api_imported`, `curated`, or `needs_review`
- `last_verified`: date when the record was last checked

Example evidence item:

```json
{
  "field": "data_types",
  "value": "mutation",
  "source": "GDC project/file metadata",
  "supports": "Dataset may support mutation-oriented discovery",
  "confidence": "medium"
}
```

RAG answers should cite or summarize evidence items instead of relying only on the model's background knowledge.

### 7. Source Metadata

This field stores source-specific details without forcing them into the shared schema too early.

```text
source_metadata
```

Examples:

```json
{
  "gdc": {
    "program": "TCGA",
    "project_id": "TCGA-LUAD",
    "data_categories": ["Transcriptome Profiling", "Simple Nucleotide Variation"],
    "experimental_strategies": ["RNA-Seq", "WXS"]
  }
}
```

```json
{
  "cbioportal": {
    "study_id": "luad_tcga_pan_can_atlas_2018",
    "molecular_profiles": ["mutations", "mRNA expression", "copy number alterations"]
  }
}
```

## JSON Example

The first seed catalog can be stored as JSON using this shape:

```json
{
  "schema_version": 1,
  "dataset_id": "gdc:TCGA-LUAD",
  "canonical_dataset_id": "TCGA-LUAD",
  "source": "GDC",
  "source_record_id": "TCGA-LUAD",
  "source_url": "https://portal.gdc.cancer.gov/projects/TCGA-LUAD",
  "title": "TCGA Lung Adenocarcinoma",
  "description": "TCGA lung adenocarcinoma project with molecular and clinical data available through GDC.",
  "diseases": ["non-small cell lung cancer"],
  "cancer_types": ["lung adenocarcinoma", "LUAD"],
  "primary_sites": ["lung"],
  "organisms": ["Homo sapiens"],
  "cohort_tags": ["NSCLC", "TCGA", "tumor"],
  "data_types": ["RNA-seq", "mutation", "clinical", "copy number"],
  "data_categories": ["Transcriptome Profiling", "Simple Nucleotide Variation", "Clinical"],
  "assays": ["RNA-Seq", "WXS"],
  "molecular_profiles": [],
  "has_clinical": true,
  "has_expression": true,
  "has_mutation": true,
  "has_copy_number": true,
  "has_methylation": null,
  "clinical_attributes": [],
  "explicit_genes": [],
  "inferred_genes": ["EGFR", "KRAS"],
  "explicit_mutations": [],
  "inferred_mutations": ["KRAS G12C"],
  "biomarker_notes": "Useful for EGFR or KRAS research only if mutation-level data is available and verified.",
  "case_count": null,
  "sample_count": null,
  "access_level": "mixed",
  "study_design": null,
  "publication_ids": [],
  "external_ids": {
    "gdc_project_id": "TCGA-LUAD"
  },
  "evidence_level": "seed",
  "evidence_items": [
    {
      "field": "canonical_dataset_id",
      "value": "TCGA-LUAD",
      "source": "manual seed catalog",
      "supports": "Record represents a TCGA lung adenocarcinoma dataset",
      "confidence": "high"
    }
  ],
  "limitations": [
    "Seed record. Counts and exact file availability should be verified during API ingestion.",
    "KRAS G12C relevance is inferred from cancer type and mutation data availability, not explicitly verified."
  ],
  "curation_status": "seed",
  "last_verified": null,
  "source_metadata": {}
}
```

## Why Lists Are Used

Several fields should be lists even when they contain only one value:

- `diseases`
- `cancer_types`
- `primary_sites`
- `organisms`
- `cohort_tags`
- `data_types`
- `data_categories`
- `assays`
- `molecular_profiles`
- `explicit_genes`
- `inferred_genes`
- `explicit_mutations`
- `inferred_mutations`
- `clinical_attributes`
- `publication_ids`
- `limitations`

This avoids later migrations when one dataset maps to multiple diseases, genes, platforms, or data types.

## What Not To Put In V1

The first schema should not store large raw biomedical data.

Avoid adding:

- expression matrices
- per-patient mutation calls
- sequencing reads
- full clinical tables
- large file manifests

Those may be linked, counted, or summarized later, but the first project is about dataset discovery metadata.

## Retrieval Text

For keyword and vector search, each record can be converted into a text block.

Suggested fields for retrieval text:

```text
dataset_id
canonical_dataset_id
source
title
description
diseases
cancer_types
primary_sites
cohort_tags
data_types
data_categories
assays
molecular_profiles
explicit_genes
inferred_genes
explicit_mutations
inferred_mutations
biomarker_notes
limitations
```

This keeps retrieval focused on concepts that users are likely to ask about.

## Filterable Fields

The following fields are good candidates for filtering:

```text
source
diseases
cancer_types
primary_sites
organisms
cohort_tags
data_types
assays
has_clinical
has_expression
has_mutation
has_copy_number
explicit_genes
inferred_genes
explicit_mutations
inferred_mutations
access_level
curation_status
```

Example query:

```python
search_datasets(
    query="EGFR-mutant lung cancer RNA-seq datasets",
    filters={
        "primary_sites": ["lung"],
        "data_types": ["RNA-seq", "mutation"],
        "has_expression": True,
        "has_mutation": True
    },
    top_k=10,
)
```

## RAG Answer Rules

RAG answers should:

- name the dataset IDs and sources used
- explain why each dataset matches
- mention important data types
- distinguish explicit evidence from inferred relevance
- include limitations when evidence is weak or incomplete
- avoid medical advice and treatment recommendations

Example safe wording:

```text
TCGA-LUAD is a medium match for KRAS G12C research because it is a lung adenocarcinoma dataset with mutation data availability, but this seed record does not explicitly verify KRAS G12C-positive cases.
```

## Versioning

This is schema version 1.

Expected future changes:

- Add a separate `DatasetGroup` layer for merging related source records.
- Add `file_summary` for source-specific file counts.
- Add `license` or `usage_terms`.
- Add richer `clinical_attribute_status`.
- Add `embedding_text` if we want cached vector-search input.
- Add API provenance fields after official ingestion is implemented.
