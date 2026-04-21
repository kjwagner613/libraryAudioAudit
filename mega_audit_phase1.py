import os
import csv
import unicodedata
from collections import defaultdict

ROOT = r"D:\Music MP3"
REPORT_CSV = "mega_audit_report.csv"

ILLEGAL_CHARS = set('\\/:*?"<>|')
SYSTEM_FILES = {"Thumbs.db", ".DS_Store", "desktop.ini", "ehthumbs.db"}

def canonicalize(name):
    # Lowercase
    name = name.lower()
    # Unicode normalize
    name = unicodedata.normalize("NFKD", name)
    # Remove punctuation
    cleaned = "".join(c for c in name if c.isalnum() or c.isspace())
    # Collapse whitespace
    cleaned = " ".join(cleaned.split())
    return cleaned

def main():
    issues = []
    artist_map = defaultdict(list)
    album_map = defaultdict(list)

    for artist in os.listdir(ROOT):
        artist_path = os.path.join(ROOT, artist)
        if not os.path.isdir(artist_path):
            continue

        artist_key = canonicalize(artist)
        artist_map[artist_key].append(artist_path)

        # Scan albums
        for album in os.listdir(artist_path):
            album_path = os.path.join(artist_path, album)
            if not os.path.isdir(album_path):
                continue

            album_key = canonicalize(album)
            album_map[(artist_key, album_key)].append(album_path)

    # Detect duplicate artists
    for key, paths in artist_map.items():
        if len(paths) > 1:
            for p in paths:
                issues.append(("DuplicateArtist", p))

    # Detect duplicate albums
    for (artist_key, album_key), paths in album_map.items():
        if len(paths) > 1:
            for p in paths:
                issues.append(("DuplicateAlbum", p))

    # Write CSV
    with open(REPORT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["IssueType", "FullPath"])
        for issue_type, full_path in issues:
            writer.writerow([issue_type, full_path])

    print("Audit complete.")
    print(f"Report written to: {REPORT_CSV}")
    print(f"Total issues: {len(issues)}")

if __name__ == "__main__":
    main()
