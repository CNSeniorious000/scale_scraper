from functools import cached_property, cache
from bs4 import BeautifulSoup
from rich import *
import requests


class OBHRM:
    # noinspection HttpUrlsUsage
    base = "http://www.obhrm.net"
    _current_page = None

    @classmethod
    @cache
    def get(cls, url: str) -> requests.Response:
        url.removesuffix(cls.base)
        return requests.get(f"{cls.base}{url}")

    @property
    def current_page(self):
        return self._current_page or self.root_page

    @cached_property
    def root_page(self) -> BeautifulSoup:
        return BeautifulSoup(self.get("/index.php/栏目:研究量表").text, "lxml")

    def turn_to_next_page(self):
        tag = self.current_page.find_all("div")[2].find_all("div")[4].find_all("div")[3].div.div.find_all("a")[-1]
        assert tag.text == "下一页"
        self._current_page = BeautifulSoup(self.get(tag["href"]).text, "lxml")

    @property
    def groups(self) -> list[BeautifulSoup]:
        return self.current_page.find_all("div")[2].find_all("div")[4].find_all("div")[3].find_all("div")[4:]

    @staticmethod
    @cache
    def get_paths(group: BeautifulSoup) -> list[str]:
        return [li.a["href"] for li in group.find_all("li")]

    @cached_property
    def all_paths(self) -> list[str]:
        paths = sum(map(self.get_paths, self.groups), [])
        self.turn_to_next_page()
        paths.extend(sum(map(self.get_paths, self.groups), []))
        self.turn_to_next_page()
        paths.extend(sum(map(self.get_paths, self.groups), []))
        return paths

    @cache
    def parse_page(self, path: str) -> tuple[str, dict[str, list[str]]]:
        soup = BeautifulSoup(self.get(path).text, "lxml")
        # body = soup.body.find_all("div")[2].find_all("div")[3].find_all("div")[3]
        title = soup.head.title.text.removesuffix(" - OBHRM百科")
        toc: BeautifulSoup = soup.body.find_all("div")[2].find_all("div")[3].find_all("div")[3].div

        content = {}
        paragraphs = None
        for tag in toc.find_next_siblings():
            tag: BeautifulSoup

            if tag.name == "h2":
                new_subtitle = tag.text
                content[new_subtitle] = paragraphs = []
            elif tag.name == "p":
                paragraphs.append(tag.text.strip())
                if tag.a is not None:
                    paragraphs.append(self.base + self.get_resource_url(tag.a["href"]))
            elif tag.name == "pre":
                paragraphs.append(tag.text.strip())
            else:
                print(f"\n{tag.prettify() = !s}\n{tag.text.strip() = !s}\n")
                paragraphs.append(tag.text.strip())

        return title, content

    @classmethod
    @cache
    def get_resource_url(cls, url: str) -> str:
        if url.startswith("/index.php/"):
            return BeautifulSoup(cls.get(url).text, "lxml").select_one(".internal")["href"]
        else:
            return url


obhrm = OBHRM()

if __name__ == '__main__':
    assert len(obhrm.all_paths) == 531
