
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Project import Project

import os
import logging
from langchain_chroma import Chroma

logger = logging.getLogger("monkey")

class VectorStorage:
    def __init__(self, project: Project):
        self.project = project
        self.vdbs = {}

    def unload_vdb(self, space: str) -> None:
        """
        Unload a vector database.
        """
        if space in self.vdbs:
            del self.vdbs[space]
    
    def unload_all_vdbs(self) -> None:
        """
        Unload all vector databases.
        """
        self.vdbs = {}
    
    def get_vdb(self, space: str) -> Chroma:
        """
        Get the default vector database for this project.
        """
        if space in self.vdbs:
            return self.vdbs[space]
        
        metadata_path = self.project.get_metadata_path()
        all_vdbs_path = os.path.join(metadata_path, "vdbs")
        vdb_path = os.path.join(all_vdbs_path, space)
        
        logger.debug(f"Creating vector database for '{space}'")
        vdb = Chroma(
            embedding_function=self.project.get_embedding(),
            persist_directory=vdb_path,
            
            # TODO: Cannot disable telemetry as client_settings takes
            # precedence and causes other settings to be ignored
            #client_settings=Settings(anonymized_telemetry=False)
        )

        self.vdbs[space] = vdb
        return vdb