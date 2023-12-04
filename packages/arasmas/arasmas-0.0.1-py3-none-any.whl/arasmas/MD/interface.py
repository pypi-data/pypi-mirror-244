from typing import Type
from .dataclass import MDSystem
from abc import ABCMeta, abstractmethod
from ..ff.to_md.interface import ForceInfoInterface


class MDProgramInterface(metaclass=ABCMeta):
    def __init__(self, md_system: Type[MDSystem], force_info: Type[ForceInfoInterface] = None, *args, **kwrgs) -> None:
        assert isinstance(md_system, MDSystem), TypeError("md_system should be in dataclass of MDSystem")
        self._script_lines = []
        self._md_system = md_system
        self._force_info = force_info

    @abstractmethod
    def write_script(self, path: str, is_rerun: int = 0):
        pass
