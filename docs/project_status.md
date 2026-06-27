# Project Status

This document summarizes the current planning state of the Biomedical Dataset Discovery Assistant.

## Current Stage

The project is in the early design and planning stage.

We have not started building the retrieval or RAG prototype yet. The current work has focused on choosing the project direction, understanding the domain, selecting the first data sources, and designing a professional but maintainable metadata schema.

## Project Direction

The assistant will help researchers discover public biomedical datasets relevant to diseases, genes, biomarkers, mutations, data types, and research questions.

The core problem:

```text
Public biomedical datasets are spread across different platforms.
Each platform has different metadata structures, terminology, and search workflows.
Researchers need a faster way to identify candidate datasets and understand why they are relevant.
```

The assistant should act as a research data navigation tool, not a medical diagnosis or treatment assistant.

## Target User

The target user is a professional or semi-professional research user, such as:

- biomedical researcher
- bioinformatics analyst
- data scientist working with biomedical datasets
- ML researcher looking for public biomedical datasets

The system should not assume the user is a patient or a general consumer.

## Initial Product Value

The assistant should provide value by:

- collecting metadata from multiple biomedical data sources
- normalizing source-specific metadata into one shared discovery schema
- allowing natural-language dataset discovery queries
- returning candidate datasets with evidence and limitations
- helping users judge which datasets are worth inspecting further

The first version should not claim to cover every public biomedical data source. It should demonstrate a reliable and extensible discovery workflow.

## Confirmed MVP Scope

### Included In First Version

- GDC/TCGA metadata
- cBioPortal metadata
- lung cancer focus
- NSCLC, LUAD, and LUSC examples
- RNA-seq, mutation, clinical metadata, and copy number as key data types
- keyword retrieval over normalized dataset metadata
- RAG answers grounded in retrieved dataset records
- basic evaluation questions for dataset discovery

### Deferred Until Later

- GEO ingestion
- SRA ingestion
- Open Targets query expansion
- raw genomic file download
- patient-level mutation analysis
- expression matrix analysis
- treatment recommendation or clinical decision support

## Key Design Decisions

### Source-Specific Records

The first version treats records from different platforms as separate source-specific records.

Example:

```text
gdc:TCGA-LUAD
cbioportal:luad_tcga_pan_can_atlas_2018
```

These can share a `canonical_dataset_id`, such as `TCGA-LUAD`, so the system can show that they refer to related biological data without prematurely merging them.

### Global Dataset IDs

`dataset_id` should be globally unique.

Recommended format:

```text
gdc:TCGA-LUAD
cbioportal:luad_tcga_pan_can_atlas_2018
geo:GSEXXXXX
sra:SRPXXXXX
```

This avoids collisions when the same biological study appears in multiple sources.

### Evidence-Aware Answers

The assistant should not simply return dataset names. It should explain:

- why a dataset matches the query
- which source the information came from
- what data types appear to be available
- whether the match is explicit or inferred
- what limitations remain

If evidence is weak, the assistant should still be helpful, but it must label uncertainty.

### Query-Time Match Level

Match strength should be calculated at query time, not stored permanently in the dataset record.

Reason:

```text
TCGA-LUAD may be a strong match for "NSCLC mutation datasets"
but only a medium match for "KRAS G12C-positive NSCLC cohorts"
if KRAS G12C-positive cases are not explicitly verified.
```

The dataset record should store evidence and limitations. The retrieval/RAG layer should use that evidence to calculate query-specific match levels.

## Current Documents

- `README.md`: project overview and links
- `docs/project_investigation.md`: initial project investigation
- `docs/domain_background.md`: minimum biomedical/domain background
- `docs/data_sources.md`: selected and deferred data sources
- `docs/data_schema.md`: normalized `DatasetRecord` schema
- `docs/project_status.md`: current progress and decisions
- `docs/evaluation_plan.md`: retrieval and answer evaluation plan
- `eval/questions_seed.json`: initial dataset discovery evaluation questions

## Next Implementation Steps

1. Create the basic project skeleton.
2. Implement `DatasetRecord` in `src/models.py`.
3. Create a small seed catalog in `data/processed/seed_catalog.json`.
4. Add records for:
   - `gdc:TCGA-LUAD`
   - `gdc:TCGA-LUSC`
   - one or more cBioPortal lung cancer studies
5. Build a simple keyword retriever.
6. Refine the first evaluation questions against the seed catalog.
7. Add a minimal RAG pipeline that answers only from retrieved records.

## Current Risks

- Metadata may not be detailed enough to confirm specific mutations such as KRAS G12C.
- GDC and cBioPortal may contain overlapping biological studies with different metadata structures.
- If retrieval records are too shallow, the LLM answer will be vague.
- If uncertainty is not labeled, the assistant may sound more confident than the evidence supports.

## Working Principle

Build the project in small layers:

```text
domain understanding
-> source selection
-> normalized schema
-> seed catalog
-> retrieval
-> RAG
-> evaluation
-> UI
```

This keeps the project professional without making the first version too large to finish.
