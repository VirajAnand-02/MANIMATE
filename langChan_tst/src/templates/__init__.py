"""
Template system
"""
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.templates.layouts import TemplateScene

__all__ = ["TemplateScene"]
