#!/usr/bin/env python3
"""
Regenerate the "Upstream review" section of the profile README.

Queries the GitHub search API for pull requests in the configured upstream
repositories that the user has commented on, and rewrites the block between
the REVIEWS:START / REVIEWS:END markers in README.md.

Runs with only the standard library. Uses GITHUB_TOKEN when present (the
Actions-provided token is enough) for a higher search rate limit.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

USER = "mnfadel"
REPOS = [
    "bitcoin-core/secp256k1",
    "bitcoin/bitcoin",
]
README = "README.md"
START = "<!-- REVIEWS:START -->"
END = "<!-- REVIEWS:END -->"
API = "https://api.github.com/search/issues"


def search(repo):
    """Return PRs in `repo` that USER has commented on, newest first."""
    query = "repo:{} commenter:{} type:pr".format(repo, USER)
    url = "{}?{}".format(
        API,
        urllib.parse.urlencode(
            {"q": query, "sort": "updated", "order": "desc", "per_page": 50}
        ),
    )
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "{}-profile-bot".format(USER),
        },
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", "Bearer " + token)

    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp).get("items", [])


def render():
    blocks = []
    total = 0

    for repo in REPOS:
        try:
            items = search(repo)
        except urllib.error.HTTPError as exc:
            print("warn: {}: HTTP {}".format(repo, exc.code), file=sys.stderr)
            continue
        except Exception as exc:  # network, parse, etc.
            print("warn: {}: {}".format(repo, exc), file=sys.stderr)
            continue

        if not items:
            continue

        blocks.append("**[{0}](https://github.com/{0})**".format(repo))
        blocks.append("")
        for item in items:
            state = item.get("state", "")
            merged = item.get("pull_request", {}).get("merged_at")
            badge = "merged" if merged else state
            blocks.append(
                "- [#{}]({}) — {} `{}`".format(
                    item["number"], item["html_url"], item["title"], badge
                )
            )
            total += 1
        blocks.append("")

    if not total:
        return "_No upstream reviews recorded yet._"

    return "\n".join(blocks).rstrip()


def main():
    if not os.path.exists(README):
        print("error: {} not found".format(README), file=sys.stderr)
        return 1

    with open(README, "r", encoding="utf-8") as fh:
        content = fh.read()

    if START not in content or END not in content:
        print(
            "error: markers {} / {} not found in {}".format(START, END, README),
            file=sys.stderr,
        )
        return 1

    body = render()
    head, rest = content.split(START, 1)
    _, tail = rest.split(END, 1)
    updated = "{}{}\n\n{}\n\n{}{}".format(head, START, body, END, tail)

    if updated == content:
        print("no change")
        return 0

    with open(README, "w", encoding="utf-8") as fh:
        fh.write(updated)
    print("README.md updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
