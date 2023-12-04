from typing import List, Dict
from .dataclass import MDSystem
from ..tools.atom import ATOM_MASS_DICT
from ..tools.yaml import input_yaml_info


class MDSystemGenerator(object):
    def __init__(self, yaml_data: Dict = None, yaml_path: str = None, ith_iteration: int = 0) -> None:
        """
        Generate the MDSystemList contained with MDSystem in one-iteration

        Parameters
        ----------
        yaml_data : Dict, optional
            input path of data, type of dictionary contained with MD data, by default None
        yaml_path : str, optional
            input path of yaml_path, by default None
        ith_iteration : int, optional
            iteration number of generating process, by default 0
        """
        _yaml_data = input_yaml_info(path=yaml_path, data=yaml_data)
        _yaml_data = _yaml_data["MD"] if "MD" in _yaml_data else _yaml_data
        self.load_info(yaml_data=_yaml_data)
        self.build(ith_iteration=ith_iteration)

    def __len__(self) -> int:
        return len(self.md_system_list)

    def __getitem__(self, index) -> List[MDSystem]:
        if index < self.__len__():
            return self._MDSystemList[index]
        else:
            raise IndexError

    @property
    def MDSystemList(self) -> List[MDSystem]:
        return self._MDSystemList

    def load_info(self, yaml_data: Dict = None):
        # LOAD THE ATOM INFO
        self.atom_index, self.atom_mass = self._extract_atom_from(yaml_data=yaml_data)
        # LOAD THE ITERATION INFO
        self.md_system_list = self._extract_iteraion_info_from(yaml_data=yaml_data)

    def _extract_atom_from(self, yaml_data: Dict):
        atom_index = yaml_data["atom_index"]
        assert type(atom_index) is dict, ValueError("[Script Error] Write atom_index correctly")
        assert len(set(atom_index.values())) == len(atom_index.values())
        assert all([True for atom in atom_index.keys() if atom in ATOM_MASS_DICT.keys()]), ValueError(
            "[Script Error] Write the atom name in Periodic Table"
        )
        atom_mass = yaml_data["atom_mass"]
        if atom_mass == "auto":
            this_atom_mass_dict = {atom_name: ATOM_MASS_DICT[atom_name] for atom_name in atom_index.keys()}
        elif type(atom_mass) == dict:
            assert atom_index.keys() == atom_mass.keys(), ValueError(
                "atom_index and atom_mass's atom should be same and same order"
            )
            this_atom_mass_dict = atom_mass
        else:
            raise ValueError("Checkt the atom_mass keyword, it should be Dict or 'auto'")
        return atom_index, this_atom_mass_dict

    def _extract_iteraion_info_from(self, yaml_data: Dict):
        md_system_list = yaml_data["iteration"]
        return md_system_list

    def build(self, ith_iteration: int = 0) -> None:
        ith_systems_dict = self.md_system_list[ith_iteration]
        initial_list = ith_systems_dict["initial"]
        temp_list = ith_systems_dict["temp"]
        pressures_list = ith_systems_dict["pressure"]
        systm_info = {
            "nstep": ith_systems_dict["nsteps"],
            "time_step": ith_systems_dict["dt"] if "dt" in ith_systems_dict else 0.5,
            "thermo_freq": ith_systems_dict["thermo_freq"] if "thermo_freq" in ith_systems_dict else 10,
            "dump_freq": ith_systems_dict["dump_freq"] if "dump_freq" in ith_systems_dict else 10,
            "ensemble": ith_systems_dict["ensemble"].lower() if "ensemble" in ith_systems_dict else "nvt",
        }
        systm_info["time_step"] *= 1e-3
        systm_info["tau_T"] = ith_systems_dict["tau_T"] if "tau_T" in ith_systems_dict else systm_info["time_step"] * 100
        systm_info["tau_P"] = ith_systems_dict["tau_P"] if "tau_P" in ith_systems_dict else systm_info["time_step"] * 1000
        assert type(initial_list[0]) == list, ValueError("[Script Error] Please Wrap the 'initial' in List")
        assert type(temp_list) == list, ValueError("[Script Error] Please Wrap the 'temp' in List")
        assert type(pressures_list) == list, ValueError("[Script Error] Please Wrap the 'pressure' in List")
        all_MDSystemList = []
        for initials in initial_list:
            i_MDSystemList = []
            for init in initials:
                for temp in temp_list:
                    for pressure in pressures_list:
                        md_run_info = MDSystem(
                            temp=temp,
                            pressure=pressure,
                            initial=init,
                            atom_info=self.atom_index,
                            atom_mass=self.atom_mass,
                            **systm_info,
                        )
                        i_MDSystemList.append(md_run_info)
            all_MDSystemList.append(i_MDSystemList)
        self._MDSystemList = all_MDSystemList
