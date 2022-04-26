"""
=====================================================================
@author:        Orion Humphrey
Project:     	Discord Tag Bot
Date:           Nov 11, 2021
Version:        1
Description:    Methods to process keyword tags for the Discord bot.
Notes:
=====================================================================
"""

# Used by BeautifulSoup to speed up parsing
import cchardet
import nltk
from bs4 import BeautifulSoup

# Download required packages for processing
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


def scrape(response) -> list:
    """Function to scrape the title and entire text of a web page.

    Args:
        url (str): URL to scrape
        header (str): User agent information

    Returns:
        list: Returns strings of the scraped title and text.
    """
    # Scrape webpage with lxml parser because it is often the fastest parser
    scraped_content = BeautifulSoup(response.content, "lxml")
    # Get string of first head > title on page
    title = scraped_content.find("head").find("title").get_text()
    # Get text from entire webpage
    text = scraped_content.get_text()

    return [title, text]


def count_occurrences(word_list: list) -> list:
    """Function to count the occurrence of each word in a body of text.
    Words get sorted from most to least frequent and any word that doesn't
    occur more than twice gets removed. The most frequent words are returned
    with a minimum of zero and a maximum of seven.

    Args:
        word_list (list): Takes in list of tuples (str,str). Words tagged with
                          parts of speech.

    Returns:
        list: Final tags (strings).
    """
    # Create dictionary of words with the default value of 0
    word_dict = {word_list[0]: 0 for word_list in word_list}
    # If there is more than one occurrence of a word, add 1 to the value
    for i in word_list:
        if i[0] in word_dict:
            word_dict[i[0]] += 1

    # NOTE Use for seeing number of word occurrences
    # print(sorted(word_dict.items(), key=lambda x: x[1], reverse=True))

    # Delete any keys that don't have a value greater than 2 unless tag list
    # is short (<3 tags). This reduces the tags to important ones.
    for key, val in list(word_dict.items()):
        if val <= 2:
            del word_dict[key]

    # Generate list from dictionary of words sorted from most occurrences to least
    tags = sorted(word_dict, key=word_dict.get, reverse=True)
    # Return 7 tags
    return tags[:7]


def sort_title(words: list) -> list:
    """Function to sort through text and sort the words by parts of speech.
    A string of text from a title is sorted to have propper nouns at the
    beginning of the list, then regular nouns, and then adjectives. The
    words returned can range from a minimum of zero to a maximum of three.

    Args:
        words (list): Takes in list of tuples (str,str). Words tagged with
                      parts of speech.

    Returns:
        list: Final tags (strings).
    """
    order = ["NNPS", "NNP", "NNS", "NN", "JJS"]
    # Sort list of words by the oder list.
    # This is to put more relevant tags (IMO) in the beginning of the list.
    sorted_tags = sorted(words, key=lambda i: order.index(i[1]))
    # Remove parts of speech tags
    sorted_words = [word[0] for word in sorted_tags]
    # Only return 3 title tags
    return sorted_words[:3]


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
    # NN noun, singular "desk", NNS noun plural "desks", NNP proper noun,
    # singular "Harrison", NNPS proper noun, plural "dogs", JJS adjective, superlative "biggest"
    parts_of_speech = ["NN", "NNS", "NNP", "NNPS", "JJS"]

    # Tokenize text
    tok_list = nltk.word_tokenize(words)
    # Tag words in list with their parts of speech
    tagged_word_list = nltk.pos_tag(tok_list)
    # Remove every word that does not match the parts of speech in the parts of speech list
    reduced_tagged_list = [
        word for word in tagged_word_list if word[1] in parts_of_speech
    ]
    # Capitalization affects the tagging process so this comes last.
    # convert words to lower case and remove punctuation and numbers.
    # Also remove words longer than 21 characters "Incomprehensibilities"
    final_tagged_list = [
        (word[0].lower(), word[1])
        for word in reduced_tagged_list
        if word[0].isalpha() and len(word[0]) < 21
    ]

    return final_tagged_list


def create_tags(text: list) -> str:
    """Function to process a web page into keywords from that page. Keyword
    tags are sorted by importance. Up to three tags from the title of the page
    in propper noun, noun, adjective order. Up to seven tags from the entire
    page in most frequent to least frequent order.

    Args:
        list[str,str]: List of strings containing title and body text

    Returns:
        str: Formatted string of keywords or tags
    """
    # Title
    title_tags = sort_title(process_words(text[0]))
    # Text
    text_tags = count_occurrences(process_words(text[1]))

    # Remove duplicates and prioritize title tag location
    for i in title_tags:
        if i in text_tags:
            text_tags.remove(i)

    # Title and main body text tags combined
    final_tag_list = title_tags + text_tags

    if len(final_tag_list) == 0:
        return "No tags were found."

    # Capitalize first letter for looks
    final_tag_list = [word.capitalize() for word in final_tag_list]
    # Convert to string
    final_tags = ", ".join(final_tag_list)

    return final_tags
