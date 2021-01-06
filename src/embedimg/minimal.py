#!/usr/bin/env python


import pathlib
from bs4 import BeautifulSoup as BS


images_path = pathlib.Path(r"C:\Users\ssiegmun\rtfparse\attachments")
file_path = pathlib.Path(r"C:\Users\ssiegmun\rtfparse\html\ MIB3 OI 37W EU RW JP KR PCC  Testing approval for SW 231  SOP 25 20  .html")


def merge(file_path: pathlib.Path, encoding: str, images_path: pathlib.Path) -> None:
    with open(file_path, mode="r", encoding=encoding) as html_file:
        html_doc = html_file.read()
        soup = BS(html_doc, "html.parser")
        style_text = str(soup.style.string)
        return style_text.find("image00")


if __name__ == "__main__":
    merge()
