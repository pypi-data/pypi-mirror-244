from abc import ABCMeta, abstractproperty


class MLFFInterface(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractproperty
    def force_file_name(self) -> str:
        pass
