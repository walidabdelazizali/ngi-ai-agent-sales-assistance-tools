"""Shared file I/O utilities."""

import os
import tempfile
from pathlib import Path


def atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    """Write *content* to *path* atomically.

    Writes to a temporary file in the same directory, then replaces the
    target.  On success no temp file remains.  On failure the original
    file (if any) is left untouched.
    """
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(dir=parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(content)
        os.replace(tmp_path, path)
    except BaseException:
        # Clean up the temp file if the rename failed.
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
