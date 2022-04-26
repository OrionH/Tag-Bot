"""
=====================================================================
@author:        Orion Humphrey
Project:     	Discord Tag Bot
Date:           Apr 25, 2022
Version:        1
Description:    Methods to test processing of keywords.
Notes:          I'm not checking input validation.
=====================================================================
"""
import os
import sys

import requests
from requests_file import FileAdapter
from tagbot.process_tags import (
    count_occurrences,
    create_tags,
    process_words,
    scrape,
    sort_title,
)

# Uncomment for local testing. Needs to go above tagbot imports.
# Pytest adds project folder to path when using python -m pytest.
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def test_scrape():
    """Function to test the scraping of a title and text from a webpage
    response object.
    """
    session = requests.Session()
    session.mount("file://", FileAdapter())

    path = os.path.dirname(os.path.realpath(__file__))
    path = path.replace("\\", "/")

    response = session.get("file:///" + path + "/test.html")

    assert scrape(response) == [
        "This is the title to be scraped.",
        "\n\nThis is the title to be scraped.\n\nThis is the body of the html file to be scraped.\n",
    ]


def test_count_occurrences():
    """Function to test oder tagged words by frequency and remove non-
    important words.
    """

    # Empty input
    tag_list1 = []
    # Multiple occurrences of words
    tag_list2 = [
        ("text", "NN"),
        ("body", "NN"),
        ("webpage", "NN"),
        ("word", "NN"),
        ("webpage", "NN"),
        ("times", "NNS"),
        ("webpage", "NN"),
        ("tags", "NN"),
        ("instances", "NNS"),
        ("text", "NN"),
        ("tags", "NN"),
        ("webpage", "NN"),
        ("body", "NN"),
        ("tags", "NNS"),
    ]
    # One of each parts of speech
    tag_list3 = [
        ("text", "NN"),
        ("us", "NNP"),
        ("americans", "NNPS"),
        ("undergraduates", "NNS"),
        ("best", "JJS"),
    ]

    assert count_occurrences(tag_list1) == []
    assert count_occurrences(tag_list2) == ["webpage", "tags"]
    assert count_occurrences(tag_list3) == []


def test_sort_title():
    """Function to test word odering from tagged text. Tests for empty list."""

    # Empty input
    tag_list1 = []
    # Out of order tagged words
    tag_list2 = [
        ("americans", "NNPS"),
        ("text", "NN"),
        ("best", "JJS"),
        ("undergraduates", "NNS"),
        ("us", "NNP"),
    ]
    # Out of oder tagged parts of speech that weren't in tag_list2
    tag_list3 = [("biggest", "JJS"), ("ask", "NN"), ("hers", "NNS")]

    assert sort_title(tag_list1) == []
    assert sort_title(tag_list2) == ["americans", "us", "undergraduates"]
    assert sort_title(tag_list3) == ["hers", "ask", "biggest"]


def test_process_words():
    """Function to test the processing of words function. This tagging parts
    of speed, empty strings, text where each word only occurs once, long
    words that should be filtered out, removing words with numbers or
    symbols, and filtering parts of speech.
    """

    # Empty input
    text1 = ""
    # Regular example of an input
    text2 = """This is test text to simulate a body of a webpage. I will use
     the word webpage multiple times so webpage shows up in the tags. There
     will also be instances of, " text ", " tags ", " webpage ", " body " and " tags "
     again."""
    # Each word only occurs once
    text3 = "This text has each word only occuring one time."
    # Capitalization affects tagging.
    # Test with all parts of speech able to be tagged by nltk.
    text4 = """and but & , () [] {} ' " US — . ! ? : ; ... one-tenth another
     there gemeinshaft among out on pre-war braver closer calmest closest AA. F
     can dare  shed slide Escobar Shannon Americans Angels undergraduates
     clubs all both John's 's hers me one mine our occasionally swiftly out
     apart % * = U.S.S.R to Dang Jeepers further grander best biggest about
     ask avoid dipped soaked focusing judging factored primed wrap grab
     seals weaves that which who whose how where
    """
    # Words that contain or are numbers
    text5 = "Text with numbers 1 12 0 98 4567 234-2 4,956 6.78"
    # Super long words
    text6 = "Incomprehensibilities Pneumonoultramicroscopicsilicovolcanoconiosis Thyroparathyroidectomized"

    assert process_words(text1) == []
    assert process_words(text2) == [
        ("text", "NN"),
        ("body", "NN"),
        ("webpage", "NN"),
        ("word", "NN"),
        ("webpage", "NN"),
        ("times", "NNS"),
        ("webpage", "NN"),
        ("tags", "NN"),
        ("instances", "NNS"),
        ("text", "NN"),
        ("webpage", "NN"),
        ("body", "NN"),
    ]
    assert process_words(text3) == [("text", "NN"), ("word", "NN"), ("time", "NN")]
    assert process_words(text4) == [
        ("us", "NNP"),
        ("gemeinshaft", "NN"),
        ("braver", "NN"),
        ("calmest", "NN"),
        ("closest", "NN"),
        ("aa", "NNP"),
        ("f", "NNP"),
        ("escobar", "NNP"),
        ("shannon", "NNP"),
        ("americans", "NNPS"),
        ("angels", "NNPS"),
        ("undergraduates", "NNS"),
        ("john", "NNP"),
        ("hers", "NNS"),
        ("dang", "NNP"),
        ("jeepers", "NNP"),
        ("grander", "NN"),
        ("best", "JJS"),
        ("biggest", "JJS"),
        ("ask", "NN"),
        ("avoid", "NN"),
        ("judging", "NN"),
        ("wrap", "NN"),
        ("grab", "NN"),
        ("seals", "NNS"),
    ]
    assert process_words(text5) == [("text", "NN"), ("numbers", "NNS")]
    assert process_words(text6) == []


def test_create_tags():
    """Function to test the creation of a string of tags from a list of tagged
    words generated from a title and body of text. Tests for empty tags.
    """

    # Empty input
    text1 = ["", ""]
    # Duplicate tags in title and body
    text2 = [
        "This is a title",
        "This is a body of text. It has duplicate words like title title tile and text text text \
        to check for duplicate removal and adding one tag from the body.",
    ]
    # Text only in body
    text3 = ["", "This test only has a body. Test test test."]
    # Text only in title
    text4 = ["This test only has a title. Title title title.", ""]

    assert create_tags(text1) == "No tags were found."
    assert create_tags(text2) == "Title, Text"
    assert create_tags(text3) == "Test"
    assert create_tags(text4) == "Title, Test, Title"
