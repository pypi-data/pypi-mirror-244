from typing import Dict, Type
from . import allegro, deepmd
from .interface import ForceInfoInterface


from_: Dict[str, Type[ForceInfoInterface]] = {"allegro": allegro.ForceInfo, "deepmd": deepmd.ForceInfo}
