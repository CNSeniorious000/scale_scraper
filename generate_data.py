from concurrent.futures import ThreadPoolExecutor
from alive_progress import alive_it
from util.request import obhrm
from util.db import *
import pickle
import json


class MirrorOBHRM(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    title: str = Field()
    content: str = Field(default="")


create_all()

block_size = 8

try:
    data = pickle.load(open("data.pkl", "rb"))
    lth = len(data)
except FileNotFoundError:
    lth = len(obhrm.all_paths)
    pool = ThreadPoolExecutor(8)
    data = list(alive_it(pool.map(obhrm.parse_page, obhrm.all_paths), lth, title="scraping"))
    print(f"{len(data) = }")
    pickle.dump(data, open("data.pkl", "wb"))

with Session(engine) as session:
    for i in alive_it(range(0, lth, block_size), title="uploading"):
        for title, content in data[i:i + block_size]:
            session.add(MirrorOBHRM(title=title, content=json.dumps(content)))
        session.commit()
