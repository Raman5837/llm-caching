from typing import Union

from database.abstract import DBManager
from database.media import MediaStorage
from database.vector import VectorDB

DB = Union[DBManager, VectorDB, MediaStorage]
