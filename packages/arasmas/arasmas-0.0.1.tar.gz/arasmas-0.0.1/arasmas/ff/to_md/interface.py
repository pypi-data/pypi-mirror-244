from abc import ABCMeta, abstractproperty
from typing import Callable, Dict


class ForceInfoInterface:
    @abstractproperty
    def name(self) -> str:
        pass

    @abstractproperty
    def fmt(self) -> str:
        pass

    def __init__(self, ith: int = 0, path: str = "./graph", naming_rule: Callable[[str, str], str] = None) -> None:
        self.ith = ith
        self.path = path
        self.naming_rule = lambda path, ith: f"{path}_{ith}.{self.fmt}" if naming_rule is None else naming_rule
        self.force_name = self.naming_rule(path=path, ith=ith)

    # @property
    def lammps(self, atom_info) -> Dict[str, str]:
        pass
