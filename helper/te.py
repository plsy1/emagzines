import os
import re
from datetime import datetime
import subprocess

books_dir = "converted_ebooks"

def move_books(books_dir):
    date_str = ""
    for filename in os.listdir(books_dir):
        if filename == "cover.jpg":
            continue

        match = re.search(r"The\sEconomist\s\[(\w+)\s(\d{1,2}),\s(\d{4})\]", filename)

        if match:
            month_str = match.group(1)
            day = int(match.group(2))
            year = match.group(3)

            month = datetime.strptime(month_str, "%b").month

            date_str = f"{year}{month:02d}{day:02d}"

            extension = os.path.splitext(filename)[1]

            new_filename = f"{date_str} - The Economist{extension}"

            old_file_path = os.path.join(books_dir, filename)

            date_dir = os.path.join(books_dir, date_str)
            if not os.path.exists(date_dir):
                os.mkdir(date_dir)

            new_file_path = os.path.join(date_dir, new_filename)

            os.rename(old_file_path, new_file_path)
            print(f"Book Renamed: {filename} -> {new_filename}")

    return f"{books_dir}/{date_str}", date_str


def move_cover(newDir):
    old_file_path = os.path.join(books_dir, "cover.jpg")
    new_file_path = os.path.join(newDir, "cover.jpg")
    os.rename(old_file_path, new_file_path)
    print(f"Cover Renamed: {old_file_path} -> {new_file_path}")

newDir,date = move_books()
move_cover(newDir)
subprocess.run(f"echo 'DATE={date}' >> $GITHUB_ENV", shell=True)
