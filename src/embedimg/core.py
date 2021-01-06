#!/usr/bin/env python


import pathlib
import re
import base64
import logging
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def named_regex_group(name: str, content: str) -> bytes:
    group_start = r"(?P<" + name + r">"
    group_end = r")"
    return r"".join((group_start, content, group_end))


cid = named_regex_group("cid", "cid:")
file_name = named_regex_group("file_name", "image\d{3}")
extensions = ("png", "jpg", "jpeg", "gif")
types = named_regex_group("type", "|".join(extensions))
extension = named_regex_group("extension", r"\." + types)
file = named_regex_group("file", "".join((file_name, extension)))
adr_part = r"[0-9A-F]{8}"
adr_part1 = named_regex_group("adr_part1", adr_part)
adr_part2 = named_regex_group("adr_part2", adr_part)
address = named_regex_group("address", r"\\?@" + adr_part1 + r"\." + adr_part2)
img_pattern = re.compile(named_regex_group("img", "".join((cid, file, address))))


def replace_link_with_data(text: str, pattern: re.Pattern, search_path: pathlib.Path) -> str:
    while (match := pattern.search(text)):
        with open(search_path / match.group("file"), mode="rb") as img_file:
            data = base64.b64encode(img_file.read()).decode("ascii")
            text = text.replace(match.group("img"), "data:image/" + match.group("type") + ";base64," + data)
    return text


def merge(file_path: pathlib.Path, encoding: str, images_path: pathlib.Path) -> None:
    with open(file_path, mode="r", encoding=encoding) as html_file:
        html_doc = html_file.read()
        soup = BeautifulSoup(html_doc, "html.parser")
        style_text = replace_link_with_data(str(soup.style.string), img_pattern, images_path)
        soup.style.string.replace_with(style_text)
        for image_tag in soup.select("img"):
            try:
                data = replace_link_with_data(image_tag["src"], img_pattern, images_path)
                image_tag["src"] = data
            except Exception as err:
                logger.error(err)
        with open(file_path.with_name("replaced.html"), mode="wb") as result_file:
            result_file.write(soup.encode(encoding))


if __name__ == "__main__":
    images_path = pathlib.Path(r"C:\Users\ssiegmun\rtfparse\attachments")
    file_path = pathlib.Path(r"C:\Users\ssiegmun\rtfparse\html\ MIB3 OI 37W EU RW JP KR PCC  Testing approval for SW 231  SOP 25 20  .html")
    merge(file_path, "cp1252", images_path)
