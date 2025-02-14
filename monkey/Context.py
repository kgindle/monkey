
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Project import Project

import os

class Context:
    """
    The context in which the monkeys operate. For most purposes the context is
    the same as the project, but different contexts can be created for different
    purposes.
    """
    def __init__(self, project: Project) -> None:
        self.project = project

    def command(self, command: str, paths: list[str]):
        """
        Execute a command in the context. The command is a string that specifies
        the action to be taken. The paths are the files or directories to be
        acted upon. If no paths are provided, the command is executed in the
        project directory.
        
        The command can be one of the following:

        - "see": Scan the paths to see what is there
        - "hear": Listen to the paths to see what is being said
        - "do": Do something with the paths
        """
        # If no paths are provided, default to the project directory
        if len(paths) == 0:
            paths = [self.project.path]
        else:
            # Translate relative paths to absolute paths
            paths = [os.path.abspath(path) for path in paths]
        
        # Translate all of the paths back to project relative paths
        paths = [os.path.relpath(path, self.project.path) for path in paths]
        
        match (command):
            case "see":
                return self._see(paths)
            case "hear":
                return self._hear(paths)
            case "do":
                return self._do(paths)
            case _:
                raise Exception(f"Unknown command: {command}")

    def _see(self, paths: list[str]):
        self.project.observe(paths)
    
    def _hear(self, paths: list[str], prompt: str = None):
        chat = self.project.create_chat(paths)

        while chat.is_active():
            chat.tick()
    
    def _do(self, paths: list[str]):
        pass