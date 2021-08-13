import glob
import json
import markdown
import os
import shutil
from datetime import datetime
from markdown.extensions.codehilite import CodeHiliteExtension

pypath = os.path.dirname(os.path.abspath(__file__))
print("ver β1.0.0")
md_path = input("ファイル名を指定 >")
with open(md_path) as f:
    md = markdown.Markdown(extensions=["extra", CodeHiliteExtension()])
    result = md.convert(f.read())

t = input("1 お知らせ\n2 ブログ\n> ")
if t == "1":
    title = input("タイトルを入力> ")
    author = input("あなたの名前を入力> ")
    with open(pypath + "/tags.json", "r") as f:
        data = json.load(f)
    tag_data = data["news"]
    l = int(input("カテゴリ名を指定\n" +
                  "\n".join(list(map(lambda n: str(n[0] + 1) + " " + n[1], enumerate(tag_data))))
                  + "\n" + str(len(tag_data) + 1) + " [新規作成]\n> ")) - 1
    if len(tag_data) > l:
        tag = tag_data[l]
    else:
        tag = input("カテゴリ名 > ")
        with open(pypath + "/tags.json", "w") as f:
            data["news"].append(tag)
            json.dump(data, f, indent=2, ensure_ascii=False)
        with open(pypath + "/news/index.json", "r") as f:
            data = json.load(f)
        data.append({"name":tag,"content":[]})
        with open(pypath + "/news/index.json", "w") as f:
            json.dump(data,f, indent=2, ensure_ascii=False)
    id = len(glob.glob(pypath + "/news/*"))
    path = pypath + "/news/" + str(id) + "/"
    os.makedirs(path, exist_ok=True)
    shutil.copyfile(md_path, path + "/contents.md")
    with open(path + "contents.html", "w") as f:
        f.write(result)
    with open(pypath + "/news/index.json", "r") as f:
        data = json.load(f)
    data[list(map(lambda n: n["name"], data)).index(tag)]["content"].append(
        {"date": datetime.now().strftime("%Y/%m/%d"), "title": title, "id": id})
    with open(pypath + "/news/index.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    data = {
        "author": author,
        "update": datetime.now().strftime("%Y/%m/%d"),
        "title": title,
        "info": ["ニュース", tag]
    }
    with open(path + "/data.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
elif t == "2":
    title = input("タイトルを入力> ")
    author = input("あなたの名前を入力> ")
    with open(pypath + "/tags.json", "r") as f:
        data = json.load(f)
    tag_data = data["blog"]
    l = int(input("カテゴリ名を指定\n" +
                  "\n".join(list(map(lambda n: str(n[0] + 1) + " " + n[1], enumerate(tag_data))))
                  + "\n" + str(len(tag_data) + 1) + " [新規作成]\n> ")) - 1
    if len(tag_data) > l:
        tag = tag_data[l]
    else:
        tag = input("カテゴリ名 > ")
        with open(pypath + "/tags.json", "w") as f:
            data["blog"].append(tag)
            json.dump(data, f, indent=2, ensure_ascii=False)
        with open(pypath + "/blog/index.json", "r") as f:
            data = json.load(f)
        data.append({"name":tag,"content":[]})
        with open(pypath + "/blog/index.json", "w") as f:
            json.dump(data,f, indent=2, ensure_ascii=False)
    id = len(glob.glob(pypath + "/blog/*"))
    path = pypath + "/blog/" + str(id) + "/"
    os.makedirs(path, exist_ok=True)
    shutil.copyfile(md_path, path + "/contents.md")
    with open(path + "contents.html", "w") as f:
        f.write(result)
    with open(pypath + "/blog/index.json", "r") as f:
        data = json.load(f)
    data[list(map(lambda n: n["name"], data)).index(tag)]["content"].append(
        {"date": datetime.now().strftime("%Y/%m/%d"), "title": title, "id": id})
    with open(pypath + "/blog/index.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    data = {
        "author": author,
        "update": datetime.now().strftime("%Y/%m/%d"),
        "title": title,
        "info": ["ブログ", tag]
    }
    with open(path + "/data.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
