import hashlib
import os
import shutil
from typing import Any, Dict, Optional

from .abstract import DBManager


class MediaStorage(DBManager):
    """
    Storage Layer for managing media files.
    """

    def __init__(self, storage_dir: str = "./assets") -> None:
        self.__storage_dir = storage_dir
        os.makedirs(self.__storage_dir, exist_ok=True)

    def create(self, name: str) -> None:
        """
        Creates a subdirectory for media storage if needed
        """

        path = os.path.join(self.__storage_dir, name)

        if not os.path.exists(path):
            os.makedirs(path)
        else:
            raise FileExistsError(f"Directory '{name}' already exists.")

    def get_hash(self, file_path: str) -> str:
        """
        Generate a unique hash for a given file based on its content.
        """

        hasher = hashlib.sha256()

        try:
            with open(file_path, "rb") as media_file:
                while chunk := media_file.read(8192):
                    hasher.update(chunk)
        except FileNotFoundError as exception:
            raise ValueError(f"File {file_path} not found.") from exception

        except Exception as exception:
            raise RuntimeError(
                f"Error hashing file {file_path}: {exception}"
            ) from exception

        return hasher.hexdigest()

    def insert(self, key: str, **kwargs: Dict[str, Any]) -> str:
        """
        Store a file in the media storage directory.
        """

        if not os.path.exists(key):
            raise FileNotFoundError(f"File {key} not found.")

        file_hash = self.get_hash(key)
        extension = os.path.splitext(key)[1]
        stored_path = os.path.join(self.__storage_dir, f"{file_hash}{extension}")

        shutil.copy(key, stored_path)
        return stored_path

    def search(self, **kwargs: Dict[str, Any]) -> Optional[str]:
        """
        Retrieve the path to a file based on its hash.
        """

        file_path = kwargs.get("file_path")

        if not file_path:
            raise ValueError("file_path is required for search.")

        file_hash = self.get_hash(file_path)

        matched_files = [
            os.path.join(self.__storage_dir, file_name)
            for file_name in os.listdir(self.__storage_dir)
            if file_name.startswith(file_hash)
        ]

        if not matched_files:
            return None

        elif len(matched_files) == 1:
            return matched_files[0]

        else:
            raise RuntimeError(f"Multiple files found matching the hash: {file_hash}")

    def delete(self, file_path: str) -> None:
        """
        Delete a file from the storage directory.
        """

        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            raise FileNotFoundError(f"File {file_path} not found.")
