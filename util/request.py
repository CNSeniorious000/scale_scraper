import requests
from bs4 import BeautifulSoup

# noinspection HttpUrlsUsage
base = "http://www.obhrm.net"

r = requests.get(f"{base}/index.php/栏目:研究量表")
bs = BeautifulSoup(r.text)

# start from 4
groups = bs.html.body.find_all("div")[2].find_all("div")[4].find_all("div")[3].find_all("div")[4:]


def parse_group(group):
    return [li.a["href"] for li in group.find_all("li")]


for i in parse_group(groups[0]):
    print(base + i)


def parse_page(path):
    page = BeautifulSoup(requests.get(base + path).text)
    title = page.head.title.text.removesuffix(" - OBHRM百科")
    body = page.body.find_all("div")[2].find_all("div")[3].find_all("div")[3]

    list_of_h2 = [h2.text for h2 in body.find_all("h2")]
    list_of_p = body.find_all("p")

    return title, list_of_h2, list_of_p
