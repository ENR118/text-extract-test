import requests, re, nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup

# if running for the first time, run this:
# nltk.download('stopwords')

# sends a get request based on url
# if it succeeds, return parsed HTML text content
def get_webpage(url):
    response = requests.get(url)

    # successful get
    if (response.status_code == 200):
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    else:
        return None

# generate a list of words and frequencies given text
def index_words(soup):
    index = {}
    words = re.findall(r'\w+', soup.get_text())
    for word in words:
        # standardize words to lowercase
        word = word.lower()

        # keep track of word frequencies
        if word in index:
            index[word] += 1
        else:
            index[word] = 1
    return index

# clean up index by excluding stop words using NLTK
def exclude_stop_words(index):
    stop_words = set(stopwords.words("english"))

    # convert index to list to avoid dictionary size change (returns error)
    for word in list(index):
        if word in stop_words:
            del index[word]
    return index

# reduce all words to roots using NLTK
def stem_words(index):
    stemmer = PorterStemmer()
    stemmed_index = {}
    for word, count in index.items():
        stemmed_word = stemmer.stem(word)
        if stemmed_word in stemmed_index:
            stemmed_index[stemmed_word] += count
        else:
            stemmed_index[stemmed_word] = count
    return stemmed_index

# accept query, extract words in query
# then refer to index and add any index words (with frequencies) to results
def search(query, index):
    query_words = re.findall(r'\w+', query.lower())
    results = {}
    for word in query_words:
        if word in index:
            results[word] = index[word]
    return results

def search_engine(url, query):
    soup = get_webpage(url)
    if soup is None:
        return None
    index = index_words(soup)
    index = exclude_stop_words(index)
    index = stem_words(index)
    results = search(query, index)
    return results

# enter URL and query below
url = "https://brickipedia.fandom.com/wiki/497_Galaxy_Explorer"
query = "spaceship"
results = search_engine(url, query)
print (results)

