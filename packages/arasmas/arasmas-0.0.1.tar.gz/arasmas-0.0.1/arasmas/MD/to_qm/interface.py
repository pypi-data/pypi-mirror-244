import numpy as np
from ase import Atoms
from ase.io import read
from typing import List, Dict, Union
from abc import ABCMeta, abstractmethod


DEVI_STANDARD_KEYS = ("max_accurate", "max_candidate")


class EvaluatorInterface(metaclass=ABCMeta):
    _evaluated_frame_dict_ = {"failed": None, "candidate": None, "accurate": None}

    def __init__(self, traj_list: List[str], devi_standard: Dict[str, float]) -> None:
        self._devi_standard = self.__check_devi_standard(devi_standard)
        self._traj_list = traj_list
        self.standard_keys = DEVI_STANDARD_KEYS

    @staticmethod
    def __check_devi_standard(devi_standard: Dict[str, float]) -> Dict[str, float]:
        for key in DEVI_STANDARD_KEYS:
            assert key in devi_standard, f"{key} should be included in devi_standard"
        return devi_standard

    def extract(self, traj_list: List[str] = None, index=":"):
        if traj_list is None:
            traj_list = self._traj_list
        data_list = []
        for traj in traj_list:
            atoms = read(traj, index=index)
            data = np.asarray(self.stack_property(atoms))
            data_list.append(data.copy())
        return data_list

    @staticmethod
    def evaluate(data_list, func):
        devi_list = func(data_list)
        return devi_list

    def distribute(self, devi_list, devi_standard: Dict[str, float] = None):
        if devi_standard is None:
            devi_standard = self._devi_standard
        max_candidate = devi_standard["max_candidate"]
        max_accurate = devi_standard["max_accurate"]
        failed_frames = np.where(devi_list > max_candidate)[0]
        candidate_frames = np.where((max_candidate >= devi_list) & (devi_list > max_accurate))[0]
        accurate_frames = np.where(max_accurate >= devi_list)[0]
        total_frame = len(failed_frames) + len(candidate_frames) + len(accurate_frames)
        assert total_frame == len(devi_list), "Something is wrong.."
        _evaluated_frame_dict_ = {"failed": failed_frames, "candidate": candidate_frames, "accurate": accurate_frames}
        return _evaluated_frame_dict_

    @abstractmethod
    def stack_property(self, atoms: Union[Atoms, List[Atoms]]):
        pass
