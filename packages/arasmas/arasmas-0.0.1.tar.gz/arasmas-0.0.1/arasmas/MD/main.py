from typing import Dict, Type
from .program import md_program_info
from .generator import MDSystemGenerator
from .interface import MDProgramInterface
from ..tools.yaml import input_yaml_info


class MDSimulation(object):
    __supported_md_fmt__ = md_program_info.keys()

    def __init__(self, yaml_path: str = None, yaml_data: Dict[str, Dict] = None) -> None:
        self._yaml_data = input_yaml_info(path=yaml_path, data=yaml_data)
        self._yaml_data = self._yaml_data["MD"] if "MD" in self._yaml_data else self._yaml_data
        self._program: Type[MDProgramInterface] = self._extract_program_from(yaml_data=self._yaml_data)

    @property
    def program(self) -> Type[MDProgramInterface]:
        return self._program

    def build(self, ith_iteration: int = 0, yaml_data: Dict[str, Dict] = None) -> Type[MDSystemGenerator]:
        if yaml_data is None:
            yaml_data = self._yaml_data
        return MDSystemGenerator(yaml_data=yaml_data, ith_iteration=ith_iteration)

    def _extract_program_from(self, yaml_data: Dict[str, Dict]) -> Type[MDProgramInterface]:
        program_name = str(yaml_data["program"]).lower()
        assert program_name in self.__supported_md_fmt__, ValueError(
            f"Program should be in {self.__supported_md_fmt__}, Not Your Program {program_name}"
        )
        self.program_name = program_name
        return md_program_info[program_name]
