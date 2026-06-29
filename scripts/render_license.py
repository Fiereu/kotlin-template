#!/usr/bin/env python3
"""Fetch a license from the GitHub Licenses API and write it to disk.

This lives outside the template tree on purpose so license texts are never
vendored into this repository. Copier runs it as a task during generation.
"""
import argparse
import json
import subprocess
import urllib.request
from datetime import date

API = "https://api.github.com/licenses/{key}"


def fetch_body(spdx):
    req = urllib.request.Request(
        API.format(key=spdx.lower()),
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "kotlin-template-copier",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)["body"]


def resolve_author(author):
    if author.strip():
        return author.strip()
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], text=True
        ).strip()
        if name:
            return name
    except Exception:
        pass
    return "The Authors"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spdx", required=True)
    parser.add_argument("--author", default="")
    parser.add_argument("--out", default="LICENSE")
    args = parser.parse_args()

    author = resolve_author(args.author)
    year = str(date.today().year)
    body = fetch_body(args.spdx)
    for token in ("[year]", "[yyyy]"):
        body = body.replace(token, year)
    for token in ("[fullname]", "[name of copyright owner]"):
        body = body.replace(token, author)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"Wrote {args.spdx} license to {args.out} (Copyright {year} {author})")


if __name__ == "__main__":
    main()
