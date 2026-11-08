"""
KisanSamvaad - Knowledge Store for Agricultural Advisory
Loads verified agronomic packages from ICAR, KVK, UAS Bangalore.
"""

import os
import json
from typing import List, Dict, Any

class KnowledgeStore:
    """In-memory cache for ICAR packages and guidelines."""
    
    def __init__(self, data_dir: str = None):
        if not data_dir:
            # Resolves SARVAM project root from backend/app/ai/rag/
            current = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(current)))
            project_root = os.path.dirname(backend_dir)
            data_dir = os.path.join(project_root, "data", "knowledge")
            if not os.path.exists(data_dir):
                # Fallback check
                alt_dir = os.path.join(backend_dir, "data", "knowledge")
                if os.path.exists(alt_dir):
                    data_dir = alt_dir
        self.data_dir = data_dir
        self.crop_packages: List[Dict[str, Any]] = []
        self.soil_standards: Dict[str, Any] = {}
        self.banned_pesticides: Dict[str, Any] = {}
        self._load_all()

    def _load_all(self):
        if not os.path.exists(self.data_dir):
            return
            
        crop_pkg_path = os.path.join(self.data_dir, "icar_kolar_tomato_package.json")
        if os.path.exists(crop_pkg_path):
            with open(crop_pkg_path, "r", encoding="utf-8") as f:
                self.crop_packages = json.load(f)

        soil_path = os.path.join(self.data_dir, "icar_soil_health_standards.json")
        if os.path.exists(soil_path):
            with open(soil_path, "r", encoding="utf-8") as f:
                self.soil_standards = json.load(f)

        banned_path = os.path.join(self.data_dir, "cibrc_banned_pesticides.json")
        if os.path.exists(banned_path):
            with open(banned_path, "r", encoding="utf-8") as f:
                self.banned_pesticides = json.load(f)

knowledge_store = KnowledgeStore()
