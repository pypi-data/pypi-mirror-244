import os
import yaml
import argparse
from . import ff
from . import md


def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required=True, type=str)
    return parser.parse_args()


def load_yaml(args):
    yaml_path = args["file"]
    assert yaml_path[:-5] == ".yaml", ValueError("Please input file with format of .yaml")
    assert os.path.isfile(yaml_path), FileExistsError(f"Please Check the Yaml File PATH, not in {yaml_path}")
    with open(yaml_path, "r") as yl:
        yaml_data = yaml.load(yl, Loader=yaml.FullLoader)
    return yaml_data


def temp_full_script(yaml_data):
    base_yaml = yaml_data["BASE"]
    ff_yaml = yaml_data["FF"]
    md_yaml = yaml_data["MD"]
    qm_yaml = yaml_data["QM"]

    if "number_of_force_field" in base_yaml:
        N_ff = base_yaml["number_of_force_field"]
    else:
        N_ff = 4

    for ith in range(N_ff):
        ## [FF] TRAIN SCRIPT 작성
        ##
        ff.to_md.from_[ff_yaml.program]
        allegro_force_info = ff.to_md.allegro.ForceInfo(ith=0)


if __name__ == "__main__":
    args = parsing()
    yaml_data = load_yaml(args=args)
