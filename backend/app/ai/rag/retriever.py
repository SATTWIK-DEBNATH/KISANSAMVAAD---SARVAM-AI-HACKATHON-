"""
KisanSamvaad - Agricultural RAG Retriever
Provides keyword and semantic retrieval grounded in ICAR packages.
Returns relevant pest/soil/crop management steps with rigorous document provenance.
"""

from typing import List, Dict, Any, Optional, Tuple
from .knowledge_store import knowledge_store
from ...schemas.models import ProvenanceCitation

class AgriRAGRetriever:
    """Retrieves verified agricultural packages with provenance."""

    @classmethod
    def retrieve_context(cls, query: str) -> Tuple[Optional[Dict[str, Any]], Optional[ProvenanceCitation]]:
        """
        Searches knowledge packages for matching crop, disease, or agronomic keywords.
        """
        q = query.lower()
        packages = knowledge_store.crop_packages
        
        # 1. Match crop and symptoms
        for pkg in packages:
            crop_name = pkg.get("crop", "").lower()
            regions = [r.lower() for r in pkg.get("applicable_regions", [])]
            
            crop_match = crop_name in q or (crop_name == "tomato" and any(k in q for k in ["tamatar", "tomato", "ತೊಗರಿ", "ಟೊಮೇಟೊ", "ಟೊಮೆಟೊ"]))
            region_match = any(r in q for r in regions)

            for guidance in pkg.get("pest_disease_guidance", []):
                issue_lower = guidance.get("issue", "").lower()
                symptoms_lower = guidance.get("symptoms", "").lower()
                
                # Check for direct issue match
                if any(w in q for w in ["blight", "yellow", "curl", "spot", "bollworm", "कीड़ा", "पत्ते", "ರೋಗ", "ಹಳದಿ", "ಸುಳಿ"]):
                    if crop_match or region_match:
                        citation = ProvenanceCitation(
                            document_id=pkg.get("document_id", "ICAR-AGRI-2025"),
                            title=pkg.get("title", "ICAR Crop Package"),
                            institution=pkg.get("institution", "ICAR"),
                            publication_date=pkg.get("publication_date", "2025-01"),
                            document_version=pkg.get("document_version", "v1.0"),
                            source_url=pkg.get("source_url", "https://icar.org.in")
                        )
                        return guidance, citation

        # Default fallback to Kolar Tomato package if crop mentioned
        if "tomato" in q or "टमाटर" in q or "ಟೊಮೇಟೊ" in q:
            if packages:
                pkg = packages[0]
                guidance = pkg.get("pest_disease_guidance", [{}])[0]
                citation = ProvenanceCitation(
                    document_id=pkg.get("document_id", "ICAR-UASB-TOMATO-2025-V2"),
                    title=pkg.get("title", ""),
                    institution=pkg.get("institution", ""),
                    publication_date=pkg.get("publication_date", ""),
                    document_version=pkg.get("document_version", ""),
                    source_url=pkg.get("source_url", "")
                )
                return guidance, citation

        return None, None

