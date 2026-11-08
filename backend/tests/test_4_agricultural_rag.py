"""
Test Suite 4: Agricultural RAG Knowledge Retrieval & Provenance Tracking
Verifies ICAR package matching and provenance citation metadata for Karnataka crops.
"""

import unittest
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BACKEND_DIR)

from app.ai.rag.retriever import AgriRAGRetriever
from app.ai.rag.knowledge_store import knowledge_store

class TestAgriculturalRAG(unittest.TestCase):
    def test_knowledge_store_loaded(self):
        """Verifies verified ICAR packages are properly loaded into memory."""
        self.assertGreater(len(knowledge_store.crop_packages), 0)
        crops = [p["crop"].lower() for p in knowledge_store.crop_packages]
        self.assertIn("tomato", crops)
        self.assertIn("cotton", crops)

    def test_kolar_tomato_package_retrieval(self):
        """Verifies tomato early blight query retrieves ICAR Kolar package with citation."""
        guidance, citation = AgriRAGRetriever.retrieve_context("My Kolar tomato crop has dark brown spots and blight on leaves")
        self.assertIsNotNone(guidance)
        self.assertIsNotNone(citation)
        self.assertEqual(citation.document_id, "ICAR-UASB-TOMATO-2025-V2")
        self.assertIn("UAS Bangalore", citation.institution)
        self.assertIn("Mancozeb", guidance["chemical_remedy"])

    def test_raichur_cotton_package_retrieval(self):
        """Verifies cotton pink bollworm query retrieves CICR Raichur package."""
        guidance, citation = AgriRAGRetriever.retrieve_context("Raichur cotton bollworm problem and leaf reddening")
        self.assertIsNotNone(guidance)
        self.assertIsNotNone(citation)
        self.assertEqual(citation.document_id, "ICAR-CICR-COTTON-2024-V3")
        self.assertTrue(citation.source_url.startswith("https://"))

if __name__ == "__main__":
    unittest.main()

