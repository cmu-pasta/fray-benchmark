import os
import re
from typing import List

def resolve_classpaths(classpaths: List[str]) -> List[str]:
    resolved_paths = []
    for path in classpaths:
        if '*' in path:
            dir_path = os.path.dirname(path)
            pattern = os.path.basename(path).replace('*', '.*')
            regex = re.compile(pattern)

            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                for entry in os.listdir(dir_path):
                    if regex.match(entry):
                        resolved_paths.append(os.path.join(dir_path, entry))
        else:
            resolved_paths.append(os.path.abspath(path))

    return resolved_paths

