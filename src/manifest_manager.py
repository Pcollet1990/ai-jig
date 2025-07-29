import json
import os
import copy
from typing import Optional
from src.data_models import Manifest

# Module-level variable to cache the loaded manifest's "master" state
_master_manifest_cache: Optional[Manifest] = None
# CORRECTED: Default manifest path is now directly in the root
_default_manifest_path: str = "manifest.json"

def _ensure_manifest_directory(manifest_path: str):
    """
    Ensures the parent directory for the manifest.json file exists.
    If the manifest_path is just a filename (e.g., "manifest.json"),
    this effectively ensures the current working directory is writable.
    """
    directory = os.path.dirname(manifest_path)
    if directory: # Only create if path includes a directory (e.g., "data/manifest.json")
        os.makedirs(directory, exist_ok=True)
    # If directory is empty string, it means file is in current directory, no need to create it.

def _create_default_manifest_and_save(manifest_path: str) -> Manifest:
    """
    Creates a default Manifest object and saves it to the expected path.
    """
    global _master_manifest_cache

    default_manifest = Manifest()
    _ensure_manifest_directory(manifest_path)

    try:
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(default_manifest.to_dict(), f, indent=2)
        print(f"Default manifest created and saved to: {manifest_path}")
        # When a default is created and saved, it becomes the new master
        _master_manifest_cache = copy.copy(default_manifest)
    except Exception as e:
        print(f"Error saving default manifest: {e}")
    return default_manifest

def _load_or_create_master_manifest(manifest_path: str) -> Manifest:
    """
    Internal helper to load the master manifest into cache or create a default one.
    """
    global _master_manifest_cache

    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            _master_manifest_cache = Manifest.from_dict(data)
            print(f"Master manifest loaded successfully from: {manifest_path}")
        except json.JSONDecodeError as e:
            print(f"Error decoding manifest JSON at {manifest_path}: {e}. Creating default manifest.")
            _master_manifest_cache = _create_default_manifest_and_save(manifest_path)
        except Exception as e:
            print(f"An unexpected error occurred loading manifest from {manifest_path}: {e}. Creating default manifest.")
            _master_manifest_cache = _create_default_manifest_and_save(manifest_path)
    else:
        print(f"Manifest file not found at {manifest_path}. Creating default manifest.")
        _master_manifest_cache = _create_default_manifest_and_save(manifest_path)
    return _master_manifest_cache


def get_window_title(manifest_path: str = _default_manifest_path) -> str:
    """
    Declaratively retrieves the window title from the manifest.
    This function handles loading, caching, and shallow cloning internally.

    Args:
        manifest_path (str): The path to the manifest.json file.

    Returns:
        str: The window title from the manifest.
    """
    global _master_manifest_cache

    if _master_manifest_cache is None:
        _load_or_create_master_manifest(manifest_path)

    return _master_manifest_cache.window_title

def save_manifest(manifest_obj: Manifest, manifest_path: str = _default_manifest_path):
    """
    Saves the provided Manifest object to the specified path, overwriting the file.
    This function also updates the internal master cache with the saved state.

    Args:
        manifest_obj (Manifest): The Manifest object to save. This object
                                 is typically a shallow clone obtained from `get_manifest()`
                                 that has been modified.
        manifest_path (str): The path to save the manifest.json file.
    """
    global _master_manifest_cache

    _ensure_manifest_directory(manifest_path)

    try:
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_obj.to_dict(), f, indent=2)
        print(f"Manifest saved successfully to: {manifest_path}")
        # Update the master cache with the newly saved state
        _master_manifest_cache = copy.copy(manifest_obj)
    except Exception as e:
        print(f"Error saving manifest to {manifest_path}: {e}")
