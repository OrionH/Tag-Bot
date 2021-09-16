import discord
from functools import wraps
import time
import html2text as h2t
from bs4 import BeautifulSoup
from urllib import request
import requests
#speeds up bs4
import cchardet
import nltk
from nltk.corpus import stopwords


#Create client object
client = discord.Client()


def timeit(my_func):
    @wraps(my_func)
    def timed(*args, **kw):
        tstart = time.time()
        output = my_func(*args, **kw)
        tend = time.time()

        print('"{}" took {:.3f} ms to execute\n'.format(my_func.__name__, (tend - tstart) * 1000))
        return output
    return timed

def repeat(_func=None, *, numTimes=2):
    def decoratorRepeat(func):
        def wrapperRepeat(*args, **kwargs):
            for _ in range(numTimes):
                value = func(*args, **kwargs)
            return value
        return wrapperRepeat

    if _func is None:
        return decoratorRepeat
    else:
        return decoratorRepeat(_func)

# class Person:
#   def __init__(self, name, age=None):
#     self.name = name
#     self.age = age

# class People:
#     def __init__(self, name):
#         self.name = name

# p2 = People("B")
# p1 = Person("A", 36)

# @timeit
# @repeat(numTimes=100000)
# def printy(p1, p2):
#     if p1.age:
#         pass
#     else:
#         pass
#     if p1.age:
#         pass
#     else:
#         pass

#     #print(hasattr(p1, "age"))
#     #print(hasattr(p2, "age"))


# printy(p1,p2)


def make_dict(wl):
    #wordDict = dict.fromkeys(wl, 1)
    wordDict = {wl[0]: 0 for wl in wl}
    for i in wl:
        if i[0] in wordDict:
            wordDict[i[0]] +=1
    
    for key,val in list(wordDict.items()):
        if val <= 2:
            del wordDict[key]
    wordDict2 = sorted(wordDict.items(), key=lambda x: x[1], reverse=True)
    wordDict3 = sorted(wordDict, key=wordDict.get, reverse=True)

    #print(wordDict2[:20])

header = {"User-Agent": "Mozilla/5.0 (Macintosh;U;PPC Mac OS X 10_4_11;ja-jp) AppleWebKit/533.19.4 (KHTML	like Gecko) Version/4.1.3 Safari/533.19.4"}

url = 'https://www.theguardian.com/world/2021/sep/10/afghanistan-flight-kabul-doha-lands-foreign-passengers'
@timeit
#@repeat(numTimes=10)
def gethtml(url, header):
    #FASTER but all in one block of text

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, 'lxml')
    #find is faster than select in my testing
    title = soup.find('head').find('title').get_text()
    
    print(title)
    x = soup.get_text()
    #print(x)
    wl = nltk.word_tokenize(title)
    #convert words to lower case and remove punctuation and number. Also remove words longer than 21 characters 'Incomprehensibilities'
    wl = [word.lower() for word in wl if word.isalpha() and len(word) < 21]
    print(wl)

    #print('\n\n\n\n\n')
    # stop_words = set(stopwords.words('english'))
    # wl = [word for word in wl if not word in stop_words]
    #print(wl)

    tl = nltk.pos_tag(wl)
    print(tl)
    #filter tags
    tags = ['NN', 'NNS', 'NNP', 'NNPS','JJS']
    #get rid of any words that aren't nouns and 
    tl = [word for word in tl if not word[1] not in tags]
    order = ['NNPS','NNP','NNS','NN', 'JJS']
    tx = sorted(tl, key = lambda i: order.index(i[1]))
    print(tx)

    make_dict(tl)

    #SLOWER but cleaner
    # obj = request.urlopen(url)
    # html = obj.read()
    # text = h2t.HTML2Text()
    # text.ignore_links = True
    # x= text.handle(html.decode(encoding='UTF-8',errors='strict'))
    # print(x)





gethtml(url, header)


