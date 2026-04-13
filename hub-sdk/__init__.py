# Wrapper package — aliases for hyphenated directories
import importlib
import sys
import os

# Create module aliases for hyphenated directories
_hub_path = os.path.join(os.path.dirname(__file__), '..', 'proof-hub')
if _hub_path not in sys.path:
    sys.path.insert(0, os.path.dirname(_hub_path))

# Import submodules
from proof_hub import hub as hub
from proof_hub import agora_post as agora_post
