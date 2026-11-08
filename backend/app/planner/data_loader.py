"""
KisanSamvaad - Planner Data Loader
Parses and caches data/dose_table.yaml and data/fertilizers.yaml.
Provides zero-external-dependency fallback parsing for nested YAML dictionaries and lists.
"""

import os
import re
from typing import Dict, Any, Optional

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(CURRENT_DIR)
BACKEND_DIR = os.path.dirname(APP_DIR)
ROOT_DIR = os.path.dirname(BACKEND_DIR)

DEFAULT_DOSE_PATH = os.path.join(ROOT_DIR, "data", "dose_table.yaml")
DEFAULT_FERTILIZERS_PATH = os.path.join(ROOT_DIR, "data", "fertilizers.yaml")

def _parse_yaml_basic(content: str) -> Dict[str, Any]:
    """
    Lean, dependency-free YAML parser capable of parsing the structured
    dose_table.yaml and fertilizers.yaml files with indentation levels.
    """
    try:
        import yaml
        return yaml.safe_load(content)
    except Exception:
        pass

    # Standard-library fallback parser for indented YAML
    lines = content.splitlines()
    root: Dict[str, Any] = {}
    stack = [(root, -1, None)]  # (container, indent, key)

    for raw_line in lines:
        line = raw_line.split("#")[0].rstrip()
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        # Pop stack until parent has smaller indent
        while len(stack) > 1 and stack[-1][1] >= indent:
            stack.pop()

        parent_container, _, _ = stack[-1]

        if stripped.startswith("- "):
            # List item
            item_text = stripped[2:].strip()
            if isinstance(parent_container, list):
                if ":" in item_text and not item_text.startswith("{"):
                    # List of dicts
                    sub_dict = {}
                    parent_container.append(sub_dict)
                    k, v = item_text.split(":", 1)
                    sub_dict[k.strip()] = _parse_val(v.strip())
                    stack.append((sub_dict, indent, None))
                else:
                    parent_container.append(_parse_val(item_text))
            continue

        if ":" in stripped:
            key, val_str = stripped.split(":", 1)
            key = key.strip()
            val_str = val_str.strip()

            if not val_str:
                # New nested block (dict or list depending on child)
                new_dict: Dict[str, Any] = {}
                if isinstance(parent_container, dict):
                    parent_container[key] = new_dict
                elif isinstance(parent_container, list):
                    parent_container.append({key: new_dict})
                stack.append((new_dict, indent, key))
            else:
                val = _parse_val(val_str)
                if isinstance(parent_container, dict):
                    parent_container[key] = val

    return root

def _parse_val(s: str) -> Any:
    if not s:
        return ""
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    if s.lower() in ("null", "none"):
        return None
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_parse_val(p.strip()) for p in inner.split(",")]
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        return s

class PlannerDataLoader:
    """Loads and caches versioned agronomic data files."""

    _dose_cache: Optional[Dict[str, Any]] = None
    _fert_cache: Optional[Dict[str, Any]] = None

    @classmethod
    def load_dose_table(cls, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Loads dose_table.yaml mapping crops to recommended doses and schedules."""
        if cls._dose_cache is not None and not file_path:
            return cls._dose_cache

        path = file_path or DEFAULT_DOSE_PATH
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dose table file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        parsed = _parse_yaml_basic(content)
        crops_data = parsed.get("crops", parsed)
        if not file_path:
            cls._dose_cache = crops_data
        return crops_data

    @classmethod
    def load_fertilizers(cls, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Loads fertilizers.yaml mapping commercial products to nutrient content and pricing."""
        if cls._fert_cache is not None and not file_path:
            return cls._fert_cache

        path = file_path or DEFAULT_FERTILIZERS_PATH
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fertilizers registry file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        parsed = _parse_yaml_basic(content)
        ferts_data = parsed.get("fertilizers", parsed)
        if not file_path:
            cls._fert_cache = ferts_data
        return ferts_data

    @classmethod
    def clear_cache(cls):
        cls._dose_cache = None
        cls._fert_cache = None
