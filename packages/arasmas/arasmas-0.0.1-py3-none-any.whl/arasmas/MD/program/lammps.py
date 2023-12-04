from typing import Type
from ..dataclass import MDSystem
from ..interface import MDProgramInterface
from ...ff.to_md.interface import ForceInfoInterface

THIS_MD_PROGRAM_NAME = "lammps"
REQUIREMENT = {"force": {"pair_coeff": None, "pair_style": None}}
SCRIPT_DEFAULT_VAR_NAME = {"NSTEPS", "THERMOQ", "DUMQ", "TEMP", "PRESS", "TAU_T", "TAU_P"}
TRJ_DEFAULT_PATH = "./trj_NUM/*.lammptrj"
MAIN_TRJ_DEFAULT_PATH = "./trj_000/*.lammptrj"


class Scripter(MDProgramInterface):
    def __init__(
        self,
        md_system: Type[MDSystem],
        force_info: Type[ForceInfoInterface] = None,
        units: str = "metal",
        boundary: str = "p p p",
        atom_style: str = "atomic",
        neighbor: str = "1.0 bin",
        *args,
        **kwargs,
    ):
        super().__init__(md_system, force_info, *args, **kwargs)
        self._defaults_ = {
            "units": units,
            "boundary": boundary,
            "atom_style": atom_style,
            "neighbor": neighbor,
        }

    def write_script(self, path: str, is_rerun: int = 0) -> None:
        fmt = path[-5:]
        if fmt not in [".lmps", ".lmp"]:
            path += ".lmps"

        if not len(self._script_lines):
            self.build_base_line()
            self.add_atom_mass_lines()
            self.add_force_lines()
            dump_name = TRJ_DEFAULT_PATH.replace("NUM", str(is_rerun).zfill(3))
            self.add_dump_lines(dump_name=dump_name)
            if is_rerun:
                self.add_rerun_lines()
            else:
                self.add_run_lines()

        script_lines = "\n".join(self._script_lines)
        with open(path, "w+") as f:
            f.writelines(script_lines)

    def build_base_line(self):
        self.add_variable_line("NSTEPS", int(self._md_system.nstep))
        self.add_variable_line("THERMOQ", int(self._md_system.thermo_freq))
        self.add_variable_line("DUMQ", int(self._md_system.dump_freq))
        self.add_variable_line("TEMP", float(self._md_system.temp))
        self.add_variable_line("PRESS", float(self._md_system.pressure))
        self.add_variable_line("TAU_T", int(self._md_system.tau_T))
        self.add_variable_line("TAU_P", int(self._md_system.tau_P))
        self.add_new_lines()
        for key, values in self._defaults_.items():
            self.add_lines(key, values)
        self.add_lines("read_data", str(self._md_system.initial))
        self.add_lines("timestep", self._md_system.time_step)
        self.add_new_lines()

    def add_lines(self, key, value):
        assert value is not None, ValueError(f"The Value of MD run is None !!, {key} : {value}")
        self._script_lines.append(f"{key:<10s}\t\t{value}")

    def add_new_lines(self):
        self._script_lines.append(" ")

    def add_variable_line(self, key, value):
        assert value is not None, ValueError(f"The Value of MD run is None !!, {key} : {value}")
        self._script_lines.append(f"variable        {key}\t\t\tequal {value}")

    def add_atom_mass_lines(self):
        atom_info = self._md_system.atom_info
        atom_mass = self._md_system.atom_mass
        assert len(atom_info) == len(atom_mass)
        for atom_name, atom_index in atom_info.items():
            self._script_lines.append(f"mass\t\t {atom_index:4d}\t{atom_mass[atom_name]:.6f}")
        self.add_new_lines()

    # !TODO: Should be make force field
    def add_force_lines(self):
        if self._force_info is not None:
            force_info = self._force_info
            lammps_force_info = force_info.lammps(self._md_system.atom_info)
            assert "pair_style" in lammps_force_info and "pair_coeff" in lammps_force_info, ValueError(
                "force_info should be included of 'pair_style' and 'pair_coeff'"
            )
            pair_style = lammps_force_info["pair_style"]
            pair_coeff = lammps_force_info["pair_coeff"]
            self._script_lines.append(f"pair_style\t\t{pair_style}")
            self._script_lines.append(f"pair_coeff\t\t{pair_coeff}")
        else:
            raise ValueError("No force info in argument")
        self.add_new_lines()

    def add_dump_lines(self, dump_name: str, thermo_style: str = None, dump_style: str = None):
        if thermo_style is None:
            thermo_style = "custom step temp pe ke etotal press vol lx ly lz xy xz yz"
        if dump_style is None:
            dump_style = "id type x y z fx fy fz"
        self._script_lines.append(f"thermo_style\t{thermo_style}")
        self._script_lines.append("thermo\t\t\t${THERMOQ}")
        self._script_lines.append("dump\t\t\tmydump all custom ${DUMQ} " + f"{dump_name} {dump_style}")
        self.add_new_lines()

    def add_ensemble_lines(self):
        ensemble = self._md_system.ensembe.lower()
        if ensemble == "nvt":
            lines = "fix\t\t\t\t mynvt all nvt temp ${TEMP} ${TEMP} ${TAU_T}"
        elif ensemble == "npt":
            lines = "fix\t\t\t\t mynpt all npt temp ${TEMP} ${TEMP} ${TAU_T} iso ${PRESS} ${PRESS} ${TAU_P}"
        else:
            raise ValueError("Ensembel should be in [npt or nvt]")
        self._script_lines.append(lines)
        self.add_new_lines()

    def add_run_lines(self):
        self.add_lines("run", self._md_system.nstep)
        self.add_new_lines()

    def add_rerun_lines(self):
        self.add_lines("rerun", f"{MAIN_TRJ_DEFAULT_PATH} dump x y z")
        self.add_new_lines()
