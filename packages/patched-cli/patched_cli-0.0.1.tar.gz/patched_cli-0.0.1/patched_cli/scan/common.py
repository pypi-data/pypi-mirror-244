from typing import List

from patched_cli.models.common import Patch


def apply_file_changes(patches: List[Patch]) -> List[Patch]:
    applied_patches = []
    for patch in patches:
        file_path = patch.path
        try:
            with open(file_path, "w") as src:
                src.write(patch.patch)
            applied_patches.append(patch)
        except Exception:
            # log something
            pass

    return applied_patches
