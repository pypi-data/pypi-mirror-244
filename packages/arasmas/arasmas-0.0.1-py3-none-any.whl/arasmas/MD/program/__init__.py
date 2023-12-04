from . import lammps
from typing import Dict, Type
from ..interface import MDProgramInterface


__all__ = ["lammps", "md_program_info"]


md_program_info: Dict[str, Type[MDProgramInterface]] = {lammps.__name__.split(".")[-1].lower(): lammps.Scripter}
