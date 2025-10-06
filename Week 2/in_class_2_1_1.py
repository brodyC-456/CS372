from urllib.parse import urlparse

def url_Parse(url):
    parsedurl = urlparse(url)
    return parsedurl.path

target_url = "https://example.com/baz/foo/bar.git"
print(url_Parse(target_url))