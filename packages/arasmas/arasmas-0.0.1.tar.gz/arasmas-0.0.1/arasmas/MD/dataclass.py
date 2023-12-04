from typing import Dict
from dataclasses import dataclass


@dataclass
class MDSystem:
    """
    DataClass for containg Molecular Dynamics Simulation Information.

    atom_info   :   Dict[str, int]      ->  {"H": 1, "O": 2}
    atom_mass   :   Dict[str, float]    ->  {"H": 1.00, "O", 15.999}
    temp        :   float               ->  330.0
    pressure    :   float               ->  1.0
    nstep       :   int                 ->  1000000
    intial      :   str                 ->  "./some_path_for_initial_configuration in format of .lmp"
    ensemble    :   str                 ->  "NVT", or "NpT"
    time_step   :   float[optional]     ->  default=0.5e-3
    tau_P       :   int[optional]       ->  default=time_step * 1000
    tau_T       :   int[optional]       ->  default=time_step * 100
    thermo_freq :   int[optional]       ->  default=10
    dump_freq   :   int[optional]       ->  default=10
    """

    atom_info: Dict[str, int]
    atom_mass: Dict[str, float]
    temp: float
    pressure: float
    nstep: int
    initial: str
    ensemble: str = "NVT"
    time_step: float = 0.5e-3
    tau_P: int = int(time_step * 1000)
    tau_T: int = int(time_step * 100)
    thermo_freq: int = 10
    dump_freq: int = 10

    def __str__(self) -> str:
        string = "=" * 20 + "  MDSystem  " + "=" * 20 + "\n"
        string += f">>   Atom info   :   {self.atom_info}\n"
        string += f">>   Atom Mass   :   {self.atom_mass}\n"
        string += f">>   Temp  [K]   :   {self.temp}\n"
        string += f">>   Press [bar] :   {self.pressure}\n"
        string += f">>   dt    [ps]  :   {self.pressure}\n"
        string += f">>   tau_P [ps]  :   {self.pressure}\n"
        string += f">>   tau_T [ps]  :   {self.pressure}\n"
        string += f">>   nstep       :   {self.nstep}\n"
        string += f">>   Initial     :   {self.initial}\n"
        string += f">>   Ensemble    :   {self.ensemble}\n"
        string += f">>   thermo_freq :   {self.pressure}\n"
        string += f">>   dump_freq   :   {self.pressure}\n"
        string += "=" * 20 + "=" * 12 + "=" * 20 + "\n"
        return string
