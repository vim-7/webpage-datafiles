import glob
import json
import markdown
import os
import shutil
from datetime import datetime
from markdown.extensions.codehilite import CodeHiliteExtension

pypath = os.path.dirname(os.path.abspath(__file__))
md_path = input("ファイル名を指定 >")
with open(md_path) as f:
    md = markdown.Markdown(extensions=["extra", CodeHiliteExtension()])
    result = md.convert(f.read())

t = input("1 お知らせ\n2 ブログ\n> ")
if t == "1":
    title = input("タイトルを入力> ")
    author = input("あなたの名前を入力> ")
    with open(pypath + "/tags.json", "r") as f:
        tag_data = json.load(f)["news"]
        tag = tag_data[int(input(
            "\n".join(list(map(lambda n: str(n[0] + 1) + " " + n[1], enumerate(tag_data))))
            + "\n> ")) - 1]
    id = len(glob.glob(pypath + "/news/*"))
    path = pypath + "/news/" + str(id) + "/"
    os.makedirs(path, exist_ok=True)
    shutil.copyfile(md_path, path + "/contents.md")
    with open(path + "contents.html", "w") as f:
        f.write(result)
    with open(pypath + "/news/index.json", "r") as f:
        data = json.load(f)
    data[list(map(lambda n:n["name"],data)).index(tag)]["content"].append({"date": datetime.now().strftime("%Y/%m/%d"), "title": title, "id": id})
    with open(pypath + "/news/index.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    data = {
        "author": author,
        "update": datetime.now().strftime("%Y/%m/%d"),
        "title": title,
        "info": ["news", tag]
    }
    with open(path + "/data.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
