# sassy_ai/sassy_core/subcategories.py

import re
from typing import Dict, List, Any


def select_subcategory(
    prompt: str,
    pool: Dict[str, List[str]],
    patterns_obj: Dict[str, Any]
) -> List[str]:
    """
    Selects the appropriate subcategory:
    - patterns_obj["subpatterns"] must be a dict { sub_key: regex_str }
    - pool must be a dict { sub_key: [responses], ... }
    Returns pool[sub_key] if a regex matches, otherwise pool["general"] or all flattened responses    """
    text = prompt.lower()
    subpats = patterns_obj.get("subpatterns", {})
    for subkey, regex in subpats.items():
        if re.search(regex, text, re.IGNORECASE) and subkey in pool:
            return pool[subkey]
    # no subcategory: return "general" or flatten all lists
    return pool.get(
        "general",
        [resp for responses in pool.values() for resp in responses]
    )
