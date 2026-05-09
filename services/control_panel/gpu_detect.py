"""dGPU detection for default-model selection.

Result is cached at process scope — GPU presence doesn't change between requests
without an app restart (which is what we want for the daemon-still-warming case
to settle deterministically).
"""
from __future__ import annotations

import os
import shutil
import subprocess


_cache: bool | None = None


def has_active_dgpu() -> bool:
    """True iff `nvidia-smi -L` returns at least one GPU on stdout.

    We probe nvidia-smi only — AMD/Intel dGPUs aren't on this user's hardware
    today, and the gemma-3-12b model is sized for the RTX 4060 path. If that
    changes, extend with a Vulkan probe (`vulkaninfo --summary`). Cached after
    the first call.
    """
    global _cache
    if _cache is not None:
        return _cache
    if os.environ.get("CONTROL_PANEL_FORCE_DGPU") == "1":
        _cache = True
        return _cache
    if os.environ.get("CONTROL_PANEL_FORCE_DGPU") == "0":
        _cache = False
        return _cache
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        _cache = False
        return _cache
    try:
        result = subprocess.run(
            [nvidia_smi, "-L"],
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
    except (subprocess.TimeoutExpired, OSError):
        _cache = False
        return _cache
    _cache = result.returncode == 0 and bool(result.stdout.strip())
    return _cache


def reset_cache() -> None:
    """Test hook — drop the cached probe result."""
    global _cache
    _cache = None
