
import os.path as osp, os
from pathlib import Path
from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, DateTime, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from pyt.fileio import serialize, deserialize

Base = declarative_base()
db_string_len = 128


class Dict(Base):
    __tablename__ = "dict"
    key = Column(String(db_string_len), primary_key=True)
    value = Column(Text(), nullable=True)
    version = Column(Text(), nullable=True)
    last_modified = Column(DateTime(), nullable=True)


this_folder =  Path(__file__).parent
database_folder = this_folder / "databases"


class DictDatabase:
    def __init__(self, database_name, delete_old=False):
        super(DictDatabase, self).__init__()
        os.makedirs(database_folder, exist_ok=True)
        database_path = database_folder / f"{database_name}.db"
        if delete_old:
            if osp.exists(database_path):
                print(f"Delete {database_name} database.")
                from os import remove

                try:
                    remove(database_path)
                except OSError:
                    pass
        # print(f"{database_name} database is stored at {database_path}")
        engine = create_engine(f"sqlite:///{database_path}")
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        self.table = Dict

    @classmethod
    def to_str_key(cls, key):
        return str(key)
    
    def check_exist(self, key):
        key = self.to_str_key(key)
        return self.session.query(self.table.key).filter_by(key=key).first() is not None

    def get(self, key):
        key = self.to_str_key(key)
        return self.__getitem__(key)

    def get_full(self, key):
        key = self.to_str_key(key)
        item = self.session.query(self.table).filter_by(key=key).first()
        return deserialize(item.value), deserialize(item.version), item.last_modified

    def set(self, key, value, version=None):
        key = self.to_str_key(key)
        item = self.session.query(self.table).filter_by(key=key).first()
        value = serialize(value)
        version = serialize(version)
        if item is None:
            self.session.add(self.table(key=key, value=value, version=version, last_modified=datetime.now()))
        else:
            item.key = key
            item.value = value
            item.version = version
            item.last_modified = datetime.now()
        self.session.flush()
        self.session.commit()

    def __getitem__(self, key):
        key = self.to_str_key(key)
        if not self.check_exist(key):
            return None
        return deserialize(self.session.query(self.table).filter_by(key=key).first().value)

    def __contains__(self, key):
        key = self.to_str_key(key)
        return self.check_exist(key)
    
    def __setitem__(self, key, value):
        key = self.to_str_key(key)
        self.set(key, value)
        
    def update(self, key, value):
        key = self.to_str_key(key)
        item = self[key]
        item.update(value)
        self.set(key, item)


gl_db = DictDatabase("global")
