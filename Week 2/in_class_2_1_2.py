import mimetypes
import os

path = "/foo/bar.txt"
def get_file_ext(path):
    return os.path.splitext(path)[1]

def get_mime_type(path):
    type = mimetypes.guess_type(path)[0]
    return type

print(get_file_ext(path))
print(get_mime_type(path))