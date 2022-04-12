from functools import cached_property, cache
from bs4 import BeautifulSoup
import requests


class OBHRM:
    # noinspection HttpUrlsUsage
    base = "http://www.obhrm.net"
    __current_page = None

    @classmethod
    @cache
    def get(cls, url: str) -> requests.Response:
        url.removesuffix(cls.base)
        return requests.get(f"{cls.base}{url}")

    @property
    def current_page(self):
        return self.__current_page or self.root_page

    @cached_property
    def root_page(self) -> BeautifulSoup:
        return BeautifulSoup(self.get("/index.php/栏目:研究量表").text, "lxml")

    @classmethod
    def turn_to_next_page(cls):
        cls.__current_page = ...

    @cached_property
    def groups(self) -> list[BeautifulSoup]:
        return self.current_page.find_all("div")[2].find_all("div")[4].find_all("div")[3].find_all("div")[4:]

    @staticmethod
    @cache
    def get_paths(group: BeautifulSoup) -> list[str]:
        return [li.a["href"] for li in group.find_all("li")]

    @cache
    def parse_page(self, path: str) -> tuple[str, list[tuple[str, list[str]]]]:
        soup = BeautifulSoup(self.get(path).text, "lxml")
        # body = soup.body.find_all("div")[2].find_all("div")[3].find_all("div")[3]
        title = soup.head.title.text.removesuffix(" - OBHRM百科")
        toc: BeautifulSoup = soup.body.find_all("div")[2].find_all("div")[3].find_all("div")[3].div

        main_body = []
        for tag in toc.find_next_siblings():
            if tag.name == "p":
                main_body[-1][1].append(tag.text.strip())
                if tag.a is not None:
                    main_body[-1][1].append(self.base + self.get_resource_url(tag.a["href"]))

            elif tag.name == "h2":
                new_subtitle = tag.text
                main_body.append((new_subtitle, []))
            elif tag.name == "pre":
                main_body[-1][1].append(tag.text.strip())
            else:
                raise ValueError(tag)

        return title, main_body

    @classmethod
    @cache
    def get_resource_url(cls, url: str) -> str:
        return BeautifulSoup(cls.get(url).text, "lxml").select_one(".internal")["href"]


obhrm = OBHRM()

if __name__ == '__main__':
    _, results = obhrm.parse_page(obhrm.get_paths(obhrm.groups[4])[6])
    print(results[2][1][-1])
    print(results[2][1][-2])
