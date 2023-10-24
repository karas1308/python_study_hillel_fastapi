import requests
import xmltodict
from bs4 import BeautifulSoup


def wrap_text(text, max_line_length=50):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) <= max_line_length:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return "\n".join(lines)


def print_news(entries_list):
    for data in entries_list:
        print("##################title########################")
        print(f"Title: {wrap_text(data['title'])}")
        print("##################link########################")
        print(f"Link: {data['link']}")
        if data["summary"]["info"]:
            print("##################text########################")
            print(f"Text: {data['summary']['info']}")
            print(f"Text type: {data['summary']['type']}")
        print("##################end########################")
        print("\n")


url = "https://scipost.org/atom/publications/comp-ai"
response = requests.get(url)
soup = BeautifulSoup(response.content)
entries = soup.find_all("entry")
entries_list = []
for entry in entries:
    title = entry.find("title").text.replace("\n", "")
    link = entry.link["href"]
    summary = entry.summary
    summary_type = summary["type"]
    text = summary.text.strip() if summary else ""
    entries_list.append({"title": title, "link": link, "summary": {"info": text, "type": summary_type}})
print_news(entries_list)
###############
new_dict = xmltodict.parse(response.content)
entries = new_dict["feed"]["entry"]
entries_list_xmltodict = []
for entry in entries:
    title = entry["title"]
    link = entry["link"]["@href"]
    summary = entry["summary"].get("#text")
    summary_type = entry["summary"].get("@type")
    text = summary.strip() if summary else ""
    entries_list_xmltodict.append({"title": title, "link": link, "summary": {"info": text, "type": summary_type}})
print_news(entries_list_xmltodict)
