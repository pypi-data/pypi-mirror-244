from ase import Atoms
from typing import Dict, List, Type
from .interface import EvaluatorInterface


class ForceEvaluator(EvaluatorInterface):
    def __init__(self, traj_list: List[str], devi_standard: Dict[str, float]) -> None:
        super().__init__(traj_list, devi_standard)

    def stack_property(self, atoms: Type[Atoms]):
        return [atom.get_forces() for atom in atoms]
