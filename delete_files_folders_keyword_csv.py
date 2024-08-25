"""
Reads in a CSV of keywords and deletes all files
and folders with those keywords.
"""
import os
import shutil
import random
import csv

def read_words_from_csv(KEYWORD_CSV):
    """
    Reads in a CSV of keywords
    """
    words = []
    try:
        with open(KEYWORD_CSV, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                words.extend(row)
        return words
    except FileNotFoundError:
        print(f"CSV file not found: {KEYWORD_CSV}")
        return []
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return []

def search_and_delete(BASE_DIR, words):
    """
    Iterate through a base directory and all sub-directories
    for files and directories with keywords and delete them.
    """
    try:
        for root, dirs, files in os.walk(BASE_DIR, topdown=False):
            for file_name in files:
                if any(word.lower() in file_name.lower() for word in words):
                    file_path = os.path.join(root, file_name)
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except Exception as e:
                        print(f"Failed to delete file {file_path}: {e}")

            for dir_name in dirs:
                if any(word.lower() in dir_name.lower() for word in words):
                    dir_path = os.path.join(root, dir_name)
                    try:
                        shutil.rmtree(dir_path)
                        print(f"Deleted directory: {dir_path}")
                    except Exception as e:
                        print(f"Failed to delete directory {dir_path}: {e}")

    except Exception as e:
        print(f"An error occurred while searching the directory: {e}")

def move_files_with_extensions(source_directory, DEST_DIR, extensions):
    """
    Iterate through a base directory and all sub-directories
    for files with specific extensions and move them to 
    a different directory.
    """
    try:
        if not os.path.exists(DEST_DIR):
            os.makedirs(DEST_DIR)

        for root, dirs, files in os.walk(source_directory):
            for file_name in files:
                if any(file_name.lower().endswith(ext) for ext in extensions):
                    source_file_path = os.path.join(root, file_name)
                    destination_file_path = os.path.join(DEST_DIR, file_name)

                    # If a file with the same name exists, add a random 5-digit suffix
                    if os.path.exists(destination_file_path):
                        base_name, ext = os.path.splitext(file_name)
                        random_suffix = random.randint(10000, 99999)
                        destination_file_path = os.path.join(DEST_DIR, f"{base_name}_{random_suffix}{ext}")

                    try:
                        shutil.move(source_file_path, destination_file_path)
                        print(f"Moved file: {source_file_path} to {destination_file_path}")
                    except Exception as e:
                        print(f"Failed to move file {source_file_path}: {e}")

        # After moving the files, delete all remaining files in the source directory
        for root, dirs, files in os.walk(source_directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    os.remove(file_path)
                    print(f"Deleted remaining file: {file_path}")
                except Exception as e:
                    print(f"Failed to delete remaining file {file_path}: {e}")

        # Finally, delete all directories in the source directory
        for root, dirs, files in os.walk(source_directory, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    print(f"Deleted directory: {dir_path}")
                except Exception as e:
                    print(f"Failed to delete directory {dir_path}: {e}")

    except Exception as e:
        print(f"An error occurred while moving files: {e}")

def main(KEYWORD_CSV, BASE_DIR, DEST_DIR):
    """
    Main function to read in a CSV to create a keyword array,
    delete any files/directories with those keywords, then move all remaining
    files with specific extensions to a new directory.
    """
    words = read_words_from_csv(KEYWORD_CSV)
    if words:
        search_and_delete(BASE_DIR, words)
    else:
        print("No words found to search for.")

    extensions = ['.mp4', '.mov', '.mkv', '.avi', '.jpg', '.png']
    move_files_with_extensions(BASE_DIR, DEST_DIR, extensions)

if __name__ == "__main__":
    KEYWORD_CSV = r"C:\\test\\keywords.csv"
    BASE_DIR = r"C:\\test\\TestFolder"
    DEST_DIR = r"C:\\test\\Destination"
    main(KEYWORD_CSV, BASE_DIR, DEST_DIR)
