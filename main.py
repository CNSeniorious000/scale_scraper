from pickle import load
from random import shuffle
from fastapi import FastAPI
from functools import cache
from thefuzz.process import extractBests

data_map = dict(load(open("data.pkl", "rb")))
app = FastAPI(title="APIs about OBHRM scales wiki")


@app.get("/scales", name="get_scale_list")
@cache
def get_scale_list():
    """获取全部量表标题（顺序与OBHRM百科原顺序一致）"""
    return list(data_map)


data_keys = get_scale_list().copy()


@app.get("/scales/random")
def get_random(n: int = 10) -> list[str]:
    """随机获取n个量表标题，每次请求都会重新计算"""
    shuffle(data_keys)
    return data_keys[:n]


@app.get("/scales/query/{query}", name="find_best_match")
@cache
def find_best_match(query: str, n: int = 3) -> list[str]:
    """模糊搜索，返回前n个结果，结果有缓存"""
    return [title for title, score in extractBests(query, data_keys, limit=n)]


@app.get("/scales/{title}")
def get_scale_content(title: str) -> list[tuple]:
    """得到某个量表的正文json数据，格式为 ``list[tuple[str, list[str]]]``"""
    return data_map[find_best_match(title, 1)[0]]
