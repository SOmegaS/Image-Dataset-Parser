"""
Archiver microservice
"""
import os
import zipfile
import uuid
import sys


def zipdir(paths, zip_file):
    """
    Archives files to zip
    """
    for path in paths:
        empty_paths = []
        if not os.path.exists(path):
            empty_paths.append(path)

        for root, _, files in os.walk(path):
            for file in files:
                zip_file.write(os.path.join(root, file),
                               os.path.relpath(os.path.join(root, file),
                                               os.path.join(path, '..')))

        if len(empty_paths) != 0:
            raise NameError("some folders did not exist!")


def get_folders(folders):
    """
    Gets paths from system args and renames them
    """
    if not folders:
        folders = sys.argv[1:]
    for key, path in enumerate(folders):
        folders[key] = 'img/' + path


def main(folders=None):
    """
    Main function
    """
    if folders is None:
        folders = []
    get_folders(folders)
    zip_name = str(uuid.uuid4()) + ".zip"

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zipdir(folders, zip_file)


if __name__ == '__main__':
    main()
