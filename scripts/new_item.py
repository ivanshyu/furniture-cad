#!/usr/bin/env python3
"""Create a furniture item from the standard template."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "90_Templates" / "ITEM_TEMPLATE"
ALLOWED_CATEGORIES = {"01_Chairs", "02_Tables", "03_Cabinets"}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a new furniture engineering item."
    )
    parser.add_argument("category", choices=sorted(ALLOWED_CATEGORIES))
    parser.add_argument("item_id", help="For example: CH001")
    parser.add_argument("name", help="Folder-safe name, for example: Wood_Chair")
    args = parser.parse_args()

    item_id = args.item_id.strip().upper()
    safe_name = args.name.strip().replace(" ", "_")
    if not item_id.isalnum() or not safe_name or any(
        char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
        for char in safe_name
    ):
        parser.error("item_id must be alphanumeric and name may use letters, digits, - or _")

    destination = ROOT / args.category / f"{item_id}_{safe_name}"
    if destination.exists():
        parser.error(f"destination already exists: {destination}")

    shutil.copytree(TEMPLATE, destination)
    display_name = safe_name.replace("_", " ").replace("-", " ")
    for document in destination.rglob("*.md"):
        content = document.read_text(encoding="utf-8")
        content = content.replace("{ITEM_ID}", item_id)
        content = content.replace("{ITEM_NAME}", display_name)
        document.write_text(content, encoding="utf-8")

    print(destination)


if __name__ == "__main__":
    main()
