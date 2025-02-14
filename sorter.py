import os
import shutil
import zipfile
import tarfile


""" TODO:
Maybe split these on several files. Instead all on sorter.py

"""


#  --- Variables ----
downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")

FILE_TYPES = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.ppt', '.pptx', '.xls', '.xlsx'],
    'videos': ['.mp4', '.mkv', '.avi', '.mov'],
    'music': ['.mp3', '.wav', '.aac', '.flac'],
    'scripts': ['.py']
}

# These assume the standard directories exist in the user's home folder.
DEFAULT_DIRS = {
    'images': os.path.join(os.path.expanduser("~"), "Pictures"),
    'documents': os.path.join(os.path.expanduser("~"), "Documents"),
    'scripts': os.path.join(os.path.expanduser("~"), "Documents/Scripts"),
    'videos': os.path.join(os.path.expanduser("~"), "Videos"),
    'music': os.path.join(os.path.expanduser("~"), "Music"),
}

ZIP_EXTENSIONS = ('.zip',)
TAR_EXTENSIONS = ('.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2')


# ---- Unzip files ----
# TODO: Maybe combine with the sorting function.

for filename in os.listdir(downloads_dir):
    lower_name = filename.lower()
    if lower_name.endswith(ZIP_EXTENSIONS + TAR_EXTENSIONS):
        file_path = os.path.join(downloads_dir, filename)
        try:
            # Define a helper function to handle extraction logic
            def extract_and_cleanup(archive, members, target_folder):
                if len(members) == 1:
                    archive.extractall(downloads_dir)
                    print(f"Extracted '{filename}' directly into '{downloads_dir}'")
                else:
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)
                    archive.extractall(target_folder)
                    print(f"Extracted '{filename}' into folder '{target_folder}'")
            
            if lower_name.endswith(ZIP_EXTENSIONS):
                with zipfile.ZipFile(file_path, 'r') as archive:
                    # Exclude directory entries (they typically end with '/')
                    members = [entry for entry in archive.namelist() if not entry.endswith('/')]
                    target_folder = os.path.join(downloads_dir, os.path.splitext(filename)[0])
                    extract_and_cleanup(archive, members, target_folder)
            
            elif lower_name.endswith(TAR_EXTENSIONS):
                with tarfile.open(file_path, 'r:*') as archive:
                    members = [member for member in archive.getmembers() if member.isfile()]
                    target_folder = os.path.join(downloads_dir, os.path.splitext(filename)[0])
                    extract_and_cleanup(archive, members, target_folder)
            
            # After successful extraction, delete the archive file
            os.remove(file_path)
            print(f"Deleted archive file: {file_path}")
        except Exception as e:
            print(f"Failed to extract '{filename}': {e}")


# ---- Sort files ----

# Mapping of categories to their default target directories

# Loop through all files in the Downloads folder
for filename in os.listdir(downloads_dir):
    file_path = os.path.join(downloads_dir, filename)

    # Ensure we're working with a file (skip directories)
    if os.path.isfile(file_path):
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        moved = False

        # Check if the file's extension matches one of our categories
        for category, extensions in FILE_TYPES.items():
            if ext in extensions:
                # Get the default directory for this category
                target_dir = DEFAULT_DIRS.get(category)
                # Create the target directory if it doesn't exist
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                shutil.move(file_path, os.path.join(target_dir, filename))
                print(f"Moved {filename} to {target_dir}")
                moved = True
                break  # Stop checking once the file is moved


# ---- Delete empty folders ----
# Walk the directory tree from bottom up
for root, dirs, files in os.walk(downloads_dir, topdown=False):
    for d in dirs:
        folder_path = os.path.join(root, d)
        # Check if the folder is empty
        if not os.listdir(folder_path):
            os.rmdir(folder_path)
            print(f"Deleted empty folder: {folder_path}")
