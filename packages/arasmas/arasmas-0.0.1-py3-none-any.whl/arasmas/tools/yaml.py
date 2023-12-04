import yaml
from typing import Dict


def load_yaml(path: str) -> Dict[str, Dict]:
    with open(path, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def input_yaml_info(path: str, data: Dict[str, Dict]) -> Dict:
    if path is not None:
        if data is not None:
            raise InterruptedError("data and yaml_path both are not None, we will use yaml_path")
        data = load_yaml(path=path)
    else:
        if data is None:
            assert ValueError("Please input your data for path or data")
    return data
