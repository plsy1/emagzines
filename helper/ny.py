import os
import re
from datetime import datetime


def books():
    # Loop through each file in the directory
    books_dir = "converted_ebooks"
    date_str = ''
    for filename in os.listdir(books_dir):
        # Define the regular expression pattern to match the date in the format: dd MMM yyyy
        match = re.search(r"\[([A-Za-z]{3})\s(\d{2})\]", filename)

        if match:
            month_str = match.group(1)
            day = match.group(2)
            year = str(datetime.now().year)
            # Convert the month abbreviation to a number
            month = datetime.strptime(month_str, "%b").month

            # Create a date string in the format yyyymmdd
            date_str = f"{year}{month:02d}{day}"

            # Get the file extension
            extension = os.path.splitext(filename)[1]

            # Create the new filename
            new_filename = f"{date_str} - The New Yorker Magazine{extension}"

            # Construct the full paths for renaming
            old_file_path = os.path.join(books_dir, filename)
            os.mkdir(f"{books_dir}/{date_str}")
            new_file_path = os.path.join(f"{books_dir}/{date_str}", new_filename)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Book Renamed: {filename} -> {new_filename}")
            
    return f"{books_dir}/{date_str}", date_str


def cover(newDir):
    cover_dir = "cover"
    old_file_path = os.path.join(cover_dir, "cover.jpg")
    new_file_path = os.path.join(newDir, "cover.jpg")
    os.rename(old_file_path, new_file_path)
    print(f"Cover Renamed: {old_file_path} -> {new_file_path}")

newDir,date = books()
cover(newDir)
print(f"echo 'DATE={date}' >> $GITHUB_ENV")