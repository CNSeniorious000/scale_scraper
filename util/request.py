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


# noinspection PyShadowingNames
def parse_page(path):
    page = BeautifulSoup(requests.get(base + path).text)
    title = page.head.title.text.removesuffix(" - OBHRM百科")
    body = page.body.find_all("div")[2].find_all("div")[3].find_all("div")[3]

    toc = body.div

    results = []
    for tag in toc.find_next_siblings():
        if tag.name == "h2":
            new_title = tag.text
            results.append((new_title, []))
        elif tag.name == "p":
            results[-1][1].append(tag)
        else:
            print(tag)
            results[-1][1].append(tag)

    return title, results


title, results = parse_page(parse_group(groups[2])[2])
