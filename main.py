from pickle import load
from random import shuffle
from fastapi import FastAPI
from functools import cache
from rapidfuzz.fuzz import partial_ratio
from rapidfuzz.process import extract, extractOne

data_map = dict(load(open("data.pkl", "rb")))
app = FastAPI(title="APIs about OBHRM scales wiki")


@app.get("/scales", name="get_scale_list", response_model=list[str, str, str, ...])
@cache
def get_scale_list():
    """获取全部量表标题（顺序与OBHRM百科原顺序一致）"""
    return list(data_map)


data_keys = get_scale_list().copy()


@app.get("/scales/random/{n}", response_model=list[str])
def get_random(n: int) -> list[str]:
    """随机获取n个量表标题，每次请求都会重新计算"""
    shuffle(data_keys)
    return data_keys[:n]


@app.get("/scales/query/{text}", name="search_by_title", response_model=list[str])
@cache
def query_by_title(text: str, n: int = 3) -> list[str]:
    """按标题模糊查询，返回前n个结果，结果有缓存"""
    return [title for title, score, index in extract(text, data_keys, limit=n)]


data_map_flattened = {title: "\n".join("\n".join(paragraphs) for paragraphs in content.values())
                      for title, content in data_map.items()}


@app.get("/scales/search/{text}", name="search_by_content", response_model=list[str])
@cache
def search_by_content(text: str, n: int = 3) -> list[str]:
    """按简介模糊搜索，返回前n个结果，结果有缓存"""
    return [title for summary, score, title in extract(text, data_map_flattened, limit=n, scorer=partial_ratio)]


@app.get("/scales/{title}", response_model=dict[str, list[str]])
def get_scale_content(title: str):
    """得到某个量表的正文json数据，格式为 ``dict[str, list[str]]``"""
    key, score, index = extractOne(title, data_keys)
    return data_map[key]
