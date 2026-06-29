from src.catalog import group_by_canonical_id, load_catalog
from src.retriever import search
import unittest


class RetrieverTest(unittest.TestCase):
    def test_nsclc_query_retrieves_lung_records(self) -> None:
        records = load_catalog()
        results = search("What public datasets exist for NSCLC?", records, top_k=5)
        result_ids = {result.record.dataset_id for result in results}

        self.assertIn("gdc:TCGA-LUAD", result_ids)
        self.assertIn("gdc:TCGA-LUSC", result_ids)

    def test_cbioportal_query_prefers_cbioportal_records(self) -> None:
        records = load_catalog()
        results = search(
            "Which cBioPortal studies are relevant to NSCLC?",
            records,
            top_k=3,
        )

        self.assertTrue(results)
        self.assertEqual("cBioPortal", results[0].record.source)

    def test_breast_query_prefers_brca_records(self) -> None:
        records = load_catalog()
        results = search(
            "Which breast cancer comparison datasets are currently in the catalog?",
            records,
            top_k=2,
        )
        result_ids = {result.record.dataset_id for result in results}

        self.assertEqual(
            {
                "gdc:TCGA-BRCA",
                "cbioportal:brca_tcga_pan_can_atlas_2018",
            },
            result_ids,
        )

    def test_related_source_views_group_by_canonical_dataset(self) -> None:
        records = load_catalog()
        grouped = group_by_canonical_id(records)

        self.assertEqual(
            {
                "gdc:TCGA-LUAD",
                "cbioportal:luad_tcga_pan_can_atlas_2018",
            },
            {record.dataset_id for record in grouped["TCGA-LUAD"]},
        )


if __name__ == "__main__":
    unittest.main()
