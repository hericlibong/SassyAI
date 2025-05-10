# sassy_ai/sassy_core/subcategories.py

import re
from typing import Dict, List, Any

def select_subcategory(
    prompt: str,
    pool: Dict[str, List[str]],
    patterns_obj: Dict[str, Any]
) -> List[str]:
    """
    Sélectionne la sous-catégorie appropriée :
    - patterns_obj["subpatterns"] doit être un dict { sous_key: regex_str }
    - pool doit être un dict { sous_key: [réponses], ... }
    Retourne pool[sous_key] si un regex matche, sinon pool["general"] ou toutes réponses à plat.
    """
    text = prompt.lower()
    subpats = patterns_obj.get("subpatterns", {})
    for subkey, regex in subpats.items():
        if re.search(regex, text, re.IGNORECASE) and subkey in pool:
            return pool[subkey]
    # pas de sous-cat : renvoyer "general" ou aplatir toutes listes
    return pool.get(
        "general",
        [resp for responses in pool.values() for resp in responses]
    )
