"""Normalized dataset models used by retrieval and evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EvidenceItem:
    """A small, source-grounded fact used to justify retrieval answers."""

    field: str
    value: str
    source: str
    supports: str
    confidence: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceItem":
        return cls(
            field=str(data.get("field", "")),
            value=str(data.get("value", "")),
            source=str(data.get("source", "")),
            supports=str(data.get("supports", "")),
            confidence=str(data.get("confidence", "unknown")),
        )


@dataclass(frozen=True)
class DatasetRecord:
    """Source-specific dataset record normalized into the shared catalog shape."""

    schema_version: int
    dataset_id: str
    canonical_dataset_id: str
    source: str
    source_record_id: str
    source_url: str
    title: str
    description: str
    diseases: list[str] = field(default_factory=list)
    cancer_types: list[str] = field(default_factory=list)
    primary_sites: list[str] = field(default_factory=list)
    organisms: list[str] = field(default_factory=list)
    cohort_tags: list[str] = field(default_factory=list)
    data_types: list[str] = field(default_factory=list)
    data_categories: list[str] = field(default_factory=list)
    assays: list[str] = field(default_factory=list)
    molecular_profiles: list[str] = field(default_factory=list)
    has_clinical: bool = False
    has_expression: bool = False
    has_mutation: bool = False
    has_copy_number: bool = False
    has_methylation: bool = False
    clinical_attributes: list[str] = field(default_factory=list)
    explicit_genes: list[str] = field(default_factory=list)
    inferred_genes: list[str] = field(default_factory=list)
    explicit_mutations: list[str] = field(default_factory=list)
    inferred_mutations: list[str] = field(default_factory=list)
    biomarker_notes: str = ""
    case_count: int | None = None
    sample_count: int | None = None
    access_level: str = "unknown"
    study_design: str = ""
    publication_ids: list[str] = field(default_factory=list)
    external_ids: list[str] = field(default_factory=list)
    evidence_level: str = "unknown"
    evidence_items: list[EvidenceItem] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    curation_status: str = "seed"
    last_verified: str = ""
    source_metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DatasetRecord":
        evidence_items = [
            EvidenceItem.from_dict(item) for item in data.get("evidence_items", [])
        ]
        fields = dict(data)
        fields["evidence_items"] = evidence_items
        return cls(**fields)

    def searchable_text(self) -> str:
        """Return a compact text representation for first-pass keyword retrieval."""

        values: list[str] = [
            self.dataset_id,
            self.canonical_dataset_id,
            self.source,
            self.source_record_id,
            self.title,
            self.description,
            self.biomarker_notes,
            self.access_level,
            self.study_design,
        ]
        list_fields = [
            self.diseases,
            self.cancer_types,
            self.primary_sites,
            self.organisms,
            self.cohort_tags,
            self.data_types,
            self.data_categories,
            self.assays,
            self.molecular_profiles,
            self.clinical_attributes,
            self.explicit_genes,
            self.inferred_genes,
            self.explicit_mutations,
            self.inferred_mutations,
            self.publication_ids,
            self.external_ids,
            self.limitations,
        ]
        for items in list_fields:
            values.extend(items)
        for item in self.evidence_items:
            values.extend(
                [item.field, item.value, item.source, item.supports, item.confidence]
            )
        return " ".join(value for value in values if value)
