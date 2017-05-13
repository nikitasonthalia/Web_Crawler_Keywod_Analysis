from html.parser import HTMLParser  
import requests
from bs4 import BeautifulSoup
from collections import Counter,defaultdict
import re
import sys
import time

"""
Developed by : Nikita Sonthalia
Date : 5/13/2017
purpose: Given any page (URL), be able to classify the page, and return a list of relevant topics or keyword.

"""
""" This class is a HTMLParser class which handles all the porcessing of HTML page parsing. """
class LinkParser(HTMLParser):

    """ This function that HTMLParser normally has to parse the links """
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]


    """This new function to get links and open that link and get html text from that."""
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        try:
            response = requests.get(url)
        except:
            print("URL is not proper. Not able to get requests response: Try again!")
            sys.exit()
        if  'text/html' in response.headers['Content-Type']:
            htmlBytes = response.text
            htmlString = htmlBytes
            return htmlString, self.links
        else:
            return "",[]

"""
# This function checks the visiblity of the element on the web page.
# Input : Takes the element 
# Output: Return true if it visible on page else return false
"""
def visible(element):
    if element.parent.name in ['style', 'script', '[document]']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True


"""
# This function parses the text and removes all the escape sequences, digits and spaces etc from the text.
# Input: Get Text
# Output: Return new text by removing all the unwanted character
"""
def parseText(txt):
    txt = txt.encode('utf-8','ignore')
    txt = bytes(str(txt), "utf-8").decode("unicode_escape") 
    txt = txt.lower()
    txt = re.sub(r'([^\s\w]|_|\n|\t|\r)+', ' ', str(txt))
    txt = re.sub(' +',' ',str(txt))
    if not txt.isdigit():
        return txt
    

"""
# This function gets the list of ingored words from the file and make a list of it.
# Output: Return list of words
"""
def getingoreword():
    words=[]
    try:
        f = open("notrequiredword.txt")
        for line in f.readlines():
            words.append(line.strip('\n'))
        return words
    except (OSError, IOError,StopIteration) as e:
        print(e)
        sys.exit()



"""
# This function removes the ingored words from the list.
# Input:  List of words
# OutputL Return new list of words
"""
def removeingoreword(txt,stopwords):
    # newlst = []
    # for b in lst:
    if txt != ' ' or b is not None:
        lb=txt.split(" ")
        if  len(lb) >=2 and lb[1] != '' and len(lb[1])>1:
            if lb[1] not in stopwords :
                    # print(lb[1])
                    # newlst.append(lb[1])
                return True
    return False   
    # return newlst

    
"""
#  This function takes the url and processes it throught the end result
# Input: URL
# output: List the Keyword.
"""
def myspider(url):
    try:
        parser=LinkParser()
        data, links = parser.getLinks(url)
    except (ValueError,IOError) as e :
        print(e)
        sys.exit()
    stopwords = getingoreword()
    parsed_html = BeautifulSoup(data,'html.parser')
    # parsed_html = BeautifulSoup(data)
    # print(parsed_html.prettify())
    texts = parsed_html.findAll(text=True)
    visible_texts = filter(visible, texts)
    meta=parsed_html.find_all("meta")
    title=parsed_html.title.string
    lst1 = [parseText(x) for x in visible_texts]
    lst8 = [parseText(x.string) for x in meta if x.string is not None]
    lst7 = [parseText(x)  for x in title.split(" ")]
    lst=lst1+lst7
    wordlst=[]
    for x in lst:
        word= [ parseText(i) for i in x.split(" ")]
        wordlst+=word
    newlst= filter(lambda txt: removeingoreword(txt,stopwords), wordlst) 
    lst7=filter(lambda txt: removeingoreword(txt,stopwords), lst7) 
    counter = Counter(newlst)
    occs = dict(counter)
    finallist=sorted(occs, key=occs.get)
    finalset=set(finallist[-5:]).union(set(lst7))
    finallist=[" ".join(x.split(" ")[1:]) for x in list(finalset)]
    return(finallist)



"""
# Run main program here
# Take a url as system argument and call the HTML parser function.
"""
if(len(sys.argv) == 1 ): 
    print('Usage : python main.py [url]')
    sys.exit()
try:
    starttime = int(round(time.time()))
    finalkeyword= myspider(sys.argv[1])
    print("List of words are: ", finalkeyword)
    finishtime= int(round(time.time()))
    print("Total time (second ) taken." , str(finishtime-starttime))

except (ValueError,IOError) as e :
    print(e)
    sys.exit()

