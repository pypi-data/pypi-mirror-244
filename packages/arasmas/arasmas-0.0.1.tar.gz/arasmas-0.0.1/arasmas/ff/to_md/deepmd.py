from typing import Callable
from .interface import ForceInfoInterface


class ForceInfo(ForceInfoInterface):
    name: str = "deepmd"
    fmt: str = "pb"

    def __init__(self, ith: int = 0, path: str = "./graph", naming_rule: Callable[[str, str], str] = None) -> None:
        super().__init__(ith, path, naming_rule)

    def lammps(self, atom_info):
        lammps_style = {
            "pair_style": f"{self.name} {self.force_name}",
            "pair_coeff": f"* * {' '.join([atom for atom in atom_info.keys()])}",
        }
        return lammps_style
