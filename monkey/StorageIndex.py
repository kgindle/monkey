import os
import json
import logging
import hashlib
from typing import Optional

from . import util

logger = logging.getLogger("monkey")

class StorageIndex:
    """
    Keeps track of which files have changed and associates metadata with them.
    
    Metadata is stored in a directory, which may be stored within the same
    directory as the files being tracked or in a separate directory. For
    example, a project may have a `.monkey` directory in the root.

    The last committed version of a file is stored in the metadata directory
    with a name that is a hash of the relative path of the file. Metadata is
    stored in a JSON file with the same name as the committed file but with a
    `.json` extension.
    """
    def __init__(self, content_path: str, metadata_path: str) -> None:
        """
        Initialize a new StorageIndex instance.

        Parameters:
            content_path (str): The path to the directory containing the original content.
                                This directory must exist and contain the files to be tracked.
            metadata_path (str): The path to the directory where metadata and committed file
                                 copies will be stored.
                                 This directory must exist.

        Raises:
            FileNotFoundError: If either the content_path or metadata_path does not exist or is not a directory.
        """
        content_path = os.path.abspath(content_path)
        metadata_path = os.path.abspath(metadata_path)

        if not os.path.isdir(content_path):
            raise FileNotFoundError(f"Content path '{content_path}' does not exist or is not a directory.")
        if not os.path.isdir(metadata_path):
            raise FileNotFoundError(f"Metadata path '{metadata_path}' does not exist or is not a directory.")

        self.content_path = content_path
        self.metadata_path = metadata_path
    
    def _hash_path(self, path: str) -> str:
        """
        Calculates a hash for a path within the content directory.
        """
        relative_path = os.path.relpath(path, self.content_path)

        # Ensure the path is within the content directory
        if relative_path.startswith(".."):
            raise ValueError(f"Path {path} is not within content directory {self.content_path}")
        
        return hashlib.sha256(relative_path.encode()).hexdigest()

    def has_changed(self, path: str) -> bool:
        """
        Returns True if the file at the given path has changed since it was last committed.

        Parameters:
            path (str): Path to the file to check, must be within content directory.

        Returns:
            bool: True if file is new or changed, False otherwise.
        """
        key = self._hash_path(path)
        copy_path = os.path.join(self.metadata_path, key)

        if not os.path.exists(copy_path):
            return True
        
        return util.hash_file(path) != util.hash_file(copy_path)

    def commit(self, path: str) -> bytes:
        """
        Creates a copy of a file in the metadata directory.
        This method reads the contents of a file from the given path, copies it to the
        metadata directory using a hashed filename, and returns the file's contents.

        Args:
            path (str): Path to the source file to be copied.
        
        Returns:
            bytes: The contents of the copied file.
        """
        key = self._hash_path(path)
        copy_path = os.path.join(self.metadata_path, key)

        with open(path, "rb") as f:
            data = f.read()
        
        with open(copy_path, "wb") as f:
            f.write(data)
        
        return data
    
    def update_metadata(self, path: str, changes: dict) -> dict:
        """
        Updates the metadata associated with a file.

        Parameters:
            path (str): Path to the file to update metadata for.
            changes (dict): Dictionary of changes to apply to the metadata.
        
        Returns:
            dict: The complete metadata after applying the changes.
        """
        metadata = self.get_metadata(path)
        metadata.update(changes)
        self.set_metadata(path, metadata)
        return metadata
    
    def set_metadata(self, path: str, metadata: dict) -> dict:
        """
        Sets the metadata associated with a file.

        Parameters:
            path (str): Path to the file to set metadata for.
            metadata (dict): Metadata to set.
        
        Returns:
            dict: The metadata that was set.
        """
        key = self._hash_path(path)
        copy_path = os.path.join(self.metadata_path, f"{key}.json")

        with open(copy_path, "w") as f:
            json.dump(metadata, f)
        
        return metadata
    
    def get_committed(self, path: str) -> Optional[bytes]:
        """
        Returns the last committed version of a file.

        Parameters:
            path (str): Path to the file to get the committed version of.
        
        Returns:
            bytes: The contents of the committed file, or None if the file has not been committed.
        """
        key = self._hash_path(path)
        copy_path = os.path.join(self.metadata_path, key)

        if not os.path.exists(copy_path):
            return None
        
        with open(copy_path, "rb") as f:
            return f.read()
    
    def get_metadata(self, path: str) -> dict:
        """
        Returns the metadata associated with a file.

        Parameters:
            path (str): Path to the file to get metadata for.
        
        Returns:
            dict: The metadata associated with the file, or an empty dictionary if no metadata exists.
        """
        key = self._hash_path(path)
        copy_path = os.path.join(self.metadata_path, f"{key}.json")

        if not os.path.exists(copy_path):
            return {}

        with open(copy_path, "r") as f:
            return json.load(f)
    
    def remove(self, path: str) -> None:
        """
        Removes the content and metadata associated with a file.

        Parameters:
            path (str): Path to the file to remove.
        """
        self.remove_content(path)
        self.remove_metadata(path)
    
    def _remove_file(self, path: str, ext: str = "") -> None:
        """
        Helper method to remove an internal file.
        """
        key = self._hash_path(path)
        copy_path = os.path.join(self.metadata_path, f"{key}{ext}")
        if os.path.exists(copy_path):
            os.remove(copy_path)

    def remove_content(self, path: str) -> None:
        """
        Removes the content of a file.
        """
        self._remove_file(path)

    def remove_metadata(self, path: str) -> None:
        """
        Removes the metadata associated with a file.
        """
        self._remove_file(path, ".json")