"""
=====================================================================
Name:           Orion Humphrey
Project:     	Discord Tag Bot
Date:           Sept 9, 2021
Version:        1
Description:    Methods to process keyword tags for the Discord bot.
Notes:
=====================================================================
"""

import requests
from bs4 import BeautifulSoup
import nltk
# Used by BeautifulSoup to speed up parsing
import cchardet


def scrape(url: str, header: dict) -> list:
    """Function to scrape the title and entire text of a web page.

    Args:
        url (str): URL to scrape
        header (str): User agent information

    Returns:
        list: Returns strings of the scraped title and text.
    """
    # Get response object of webpage
    response = requests.get(url, headers=header)
    # Scrape webpage with lxml parser because it is often the fastest parser
    scrapedContent = BeautifulSoup(response.content, 'lxml')
    # Get string of first head > title on page
    title = scrapedContent.find('head').find('title').get_text()
    # Get text from entire webpage
    text = scrapedContent.get_text()

    return [title, text]


def count_occurrences(word_list: list) -> list:
    """Function to count the occurrence of each word in a body of text.
    Words get sorted from most to least frequent and any word that doesn't
    occur more than twice gets removed. The most frequent words are returned
    with a minimum of zero and a maximum of seven.

    Args:
        word_list (list): Takes in list of tuples (str,str). Words tagged with parts of speech.

    Returns:
        list: Final tags (strings).
    """
    # Create dictionary of words with the default value of 0
    wordDict = {word_list[0]: 0 for word_list in word_list}
    # If there is more than one occurrence of a word, add 1 to the value
    for i in word_list:
        if i[0] in wordDict:
            wordDict[i[0]] += 1

    # NOTE Use for seeing number of word occurrences
    # print(sorted(wordDict.items(), key=lambda x: x[1], reverse=True))

    # Delete any keys that don't have a value greater than 2.
    # This reduces the tags to important ones
    for key, val in list(wordDict.items()):
        if val <= 2:
            del wordDict[key]
    # Generate list from dictionary of words sorted from most occurrences to least
    tags = sorted(wordDict, key=wordDict.get, reverse=True)

    # Return 7 tags
    return tags[:7]


def sort_title(words: list) -> list:
    """Function to sort through text and sort the words by parts of speech.
    A string of text from a title is sorted to have propper nouns at the
    beginning of the list, then regular nouns, and then adjectives. The
    words returned can range from a minimum of zero to a maximum of three.

    Args:
        words (list): Takes in list of tuples (str,str). Words tagged with parts of speech.

    Returns:
        list: Final tags (strings).
    """
    order = ['NNPS', 'NNP', 'NNS', 'NN', 'JJS']
    # Sort list of words by the oder list.
    # This is to put more relevant tags (IMO) in the beginning of the list.
    sortedTags = sorted(words, key=lambda i: order.index(i[1]))
    # Remove pos tags
    sortedWords = [word[0] for word in sortedTags]
    # Only return 3 title tags
    return sortedWords[:3]


def process_words(words: str) -> list:
    """Function to tokenize a string, tag the words with parts of speech,
    remove punctuation and excessively long words (often junk words), and
    remove all parts of speech not desired.

    Args:
        words (str): Takes in a string of text.

    Returns:
        list: List of tuples (str,str). Words tagged with parts of speech.
    """
    # list of NLTK parts of speech for creating tags.
    # NN noun, singular 'desk', NNS noun plural 'desks', NNP proper noun,
    # singular 'Harrison', NNPS proper noun, plural 'Americans', JJS adjective, superlative 'biggest'
    pos = ['NN', 'NNS', 'NNP', 'NNPS', 'JJS']

    # Tokenize text
    tok_words = nltk.word_tokenize(words)
    # convert words to lower case and remove punctuation and numbers.
    # Also remove words longer than 21 characters 'Incomprehensibilities'
    word_list = [word.lower()
                 for word in tok_words if word.isalpha() and len(word) < 21]
    # Tag words in list with their parts of speech
    tagged_list = nltk.pos_tag(word_list)
    # Remove every word that does not match the parts of speech in the pos list
    reduced_tagged_list = [
        word for word in tagged_list if not word[1] not in pos]

    return reduced_tagged_list


def create_tags(url: str, header: dict) -> str:
    """Function to process a web page into keywords from that page. Keyword
    tags are sorted by importance. Up to three tags from the title of the page in
    propper noun, noun, adjective order. Up to seven tags from the entire page in
    most frequent to least frequent order.

    Args:
        url (str): URL to scrape
        header (str): User agent information

    Returns:
        str: Formatted string of keywords or tags
    """
    # Get title and text body
    content = scrape(url, header)
    # Title
    title_tags = sort_title(process_words(content[0]))
    # Text
    text_tags = count_occurrences(process_words(content[1]))

    # Remove duplicates and prioritize title tag location
    for i in title_tags:
        if i in text_tags:
            text_tags.remove(i)

    # Title and main body text tags combined
    final_tag_list = title_tags + text_tags

    # Capitalize first letter for looks
    final_tag_list = [word.capitalize() for word in final_tag_list]
    # Convert to string
    final_tags = ', '.join(final_tag_list)

    return final_tags
