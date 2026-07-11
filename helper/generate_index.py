#!/usr/bin/env python3
import json
import os
import re
import sys
import urllib.parse
import urllib.request


MAGAZINES = {
    "te": "The Economist",
    "ny": "The New Yorker Magazine",
    "tm": "TIME Magazine",
}
TAG_PATTERN = re.compile(r"^(te|ny|tm)-(\d{8})$")


def fetch_releases(repository, token):
    releases = []
    page = 1
    while True:
        query = urllib.parse.urlencode({"per_page": 100, "page": page})
        request = urllib.request.Request(
            f"https://api.github.com/repos/{repository}/releases?{query}",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "emagzines-index-generator",
            },
        )
        with urllib.request.urlopen(request) as response:
            batch = json.load(response)
        releases.extend(batch)
        if len(batch) < 100:
            return releases
        page += 1


def asset_link(release, extension):
    for asset in release.get("assets", []):
        if asset["name"].lower().endswith(extension):
            return f"[Download]({asset['browser_download_url']})"
    return "—"


def render_index(repository, releases):
    grouped = {mag_id: [] for mag_id in MAGAZINES}
    for release in releases:
        if release.get("draft"):
            continue
        match = TAG_PATTERN.fullmatch(release.get("tag_name", ""))
        if not match:
            continue
        mag_id, issue_date = match.groups()
        grouped[mag_id].append((issue_date, release))

    lines = [
        "# Magazine Index",
        "",
        "This file is generated automatically from GitHub Releases. "
        "Issues are sorted by publication date, newest first.",
        "",
    ]
    total = 0
    for mag_id, mag_name in MAGAZINES.items():
        issues = sorted(grouped[mag_id], key=lambda item: item[0], reverse=True)
        total += len(issues)
        lines.extend(
            [
                f"## {mag_name}",
                "",
                "| Issue date | PDF | EPUB | Release |",
                "| --- | --- | --- | --- |",
            ]
        )
        for issue_date, release in issues:
            formatted_date = f"{issue_date[:4]}-{issue_date[4:6]}-{issue_date[6:]}"
            release_url = f"https://github.com/{repository}/releases/tag/{release['tag_name']}"
            lines.append(
                f"| {formatted_date} | {asset_link(release, '.pdf')} | "
                f"{asset_link(release, '.epub')} | [View]({release_url}) |"
            )
        if not issues:
            lines.append("| — | — | — | — |")
        lines.append("")

    lines.extend([f"_Total issues: {total}._", ""])
    return "\n".join(lines)


def main():
    repository = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REPOSITORY")
    output_path = sys.argv[2] if len(sys.argv) > 2 else "INDEX.md"
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not repository or not token:
        raise SystemExit("Repository and GH_TOKEN are required.")

    releases = fetch_releases(repository, token)
    content = render_index(repository, releases)
    with open(output_path, "w", encoding="utf-8") as output:
        output.write(content)
    print(f"Generated {output_path} from {len(releases)} releases.")


if __name__ == "__main__":
    main()
