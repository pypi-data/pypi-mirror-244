import yaml
import argparse


def load_yaml(args):
    with open(args.file, "r") as file:
        film = yaml.load(file, Loader=yaml.FullLoader)
        print(film["rest"]["url"])


def parsing_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True)
    return parser.parse_args()


def main():
    pass


if __name__ == "__main__":
    args = parsing_args()
    load_yaml(args=args)
