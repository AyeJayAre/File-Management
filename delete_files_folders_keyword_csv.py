"""
Reads in a CSV of keywords and deletes all files
and folders with those keywords.
"""
import os
import shutil
import csv


input_csv="keyworkds.csv"
input_directory="C:\\test\\"

def read_words_from_csv(csv_path):
    """
    Reads in a CSV of keywords
    """
    words = []
    try:
        with open(csv_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                words.extend(row)  # Assuming each row contains words separated by commas
        return words
    except FileNotFoundError:
        print(f"CSV file not found: {csv_path}")
        return []
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return []

def search_and_delete(base_directory, words):
    try:
        for root, dirs, files in os.walk(base_directory, topdown=False):
            # Check and delete matching files
            for file_name in files:
                if any(word.lower() in file_name.lower() for word in words):
                    file_path = os.path.join(root, file_name)
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except Exception as e:
                        print(f"Failed to delete file {file_path}: {e}")

            # Check and delete matching directories
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
