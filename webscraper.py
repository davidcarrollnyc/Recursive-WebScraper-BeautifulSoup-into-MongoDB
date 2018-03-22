from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

html = urllib.request.urlopen('http://www.nytimes.com').read()
print(text_from_html(html))



html = urllib.request.urlopen('http://www.nytimes.com').read()
bs = BeautifulSoup(html, "html.parser")
possible_links = bs.select('a[href^="http"]')

for link in possible_links:
    if link.has_attr('href'):
        print (link.attrs['href'])

        try:
            checkFor200 = urllib.request.urlopen(link.attrs['href'])
            html2 = checkFor200.read()
            print(html2)
        except HTTPError as e:
            continue
        print("")
        print(text_from_html(html2))