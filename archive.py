import os
import zipfile
import uuid
import sys


def zipdir(paths, ziph):
    # ziph is zipfile handle
    for path in paths:
        empty_paths = []
        if not (os.path.exists(path)):
            empty_paths.append(path)

        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                                           os.path.join(path, '..')))
        if (len(empty_paths) != 0):
            raise NameError("some folders did not exist!")


# folder принимает arhive.py как аргумент.
folders1 = sys.argv[1:]
folders = []
for path in folders1:
    folders.append('img/' + path)
# Рандомное название строки для того чтобы не было повторов.
std = str(uuid.uuid4()) + ".zip"

with zipfile.ZipFile(std, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(folders, zipf)
