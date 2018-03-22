from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

from pymongo import MongoClient

client = MongoClient("mongodb://XXXXX:XXXXX@ds117489.mlab.com:17489/heroku_XXXXX")

data_base_name : 'HTML_content'
mydb = client['heroku_XXXXX']

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


url = 'http://www.nytimes.com'

html = urllib.request.urlopen(url).read()
bs = BeautifulSoup(html, "html.parser")
possible_links = bs.select('a[href^="http"]')

for link in possible_links:
    if link.has_attr('href'):
        print (link.attrs['href'])

        try:
            checkFor200 = urllib.request.urlopen(link.attrs['href'])
            html2 = checkFor200.read()
            print(html2)

            myrecord = {
                "link": link.attrs['href'],
                "content": text_from_html(html2)
            }

            record_id = mydb.mytable.insert(myrecord)
            print(record_id)
            print(mydb.collection_names())

        except HTTPError as e:
            continue
        print("")
        print(text_from_html(html2))
