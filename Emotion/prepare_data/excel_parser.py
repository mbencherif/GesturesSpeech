# coding=utf-8

from __future__ import unicode_literals
import os
import win32com.client as win32
from pprint import pprint
import time
from unidecode import unidecode


def get_description_path():
    """
    :return: path to description.xls
    """
    return os.path.join(os.path.dirname(__file__), 'description.xls')


def init_unique_emotion_classes():
    """
    :return: labels of unique emotion classes
    """
    classes = {
        u"улыбка",
        u"закрыл глаза",
        u"пренебрежение",
        u"ярость",
        u"боль",
        u"ужас",
        u"озадаченность",
        u"удивление",
        u"плакса",
    }
    return classes


def translate_unicode(unicode_basket):
    """
    :param unicode_basket: a dict with unicode keys
    :return: the same dict with ascii keys instead
    """
    ru_en = {
        u"улыбка": "smile",
        u"закрыл глаза": "closed_eyes",
        u"пренебрежение": "disregard",
        u"ярость": "rage",
        u"боль": "pain",
        u"ужас": "horror",
        u"озадаченность": "perplexity",
        u"удивление": "amazement",
        u"плакса": "crybaby",
    }
    ascii_basket = {}
    for key, value in unicode_basket.items():
        if key is None:
            ascii_name = None
        elif key in ru_en:
            ascii_name = ru_en[key]
        else:
            ascii_name = unidecode(key)
        ascii_basket[ascii_name] = value
    return ascii_basket


def get_authors():
    authors = {
        "volodymyr",
        "oleksandr",
        "alexandr"
    }
    return authors


def init_container(set_of_labels):
    """
    :param set_of_labels: set of emotions/authors
    :return: an empty dic to gather example file names
    """
    container = {}
    for label in set_of_labels:
        container[label] = []
    return container


def find_valid_label(cell_val):
    """
    :param cell_val: cell value, read from xlsx file
    :return: its unique class label
    """
    class_labels = init_unique_emotion_classes()
    valid_label = None
    for label in class_labels:
        if label in cell_val:
            valid_label = label
    return valid_label


def upd_column(col_name, values):
    """
     Update cell_name column in missed_data.xlsx
    :param col_name: excel column name
    :param values: info list
    """
    path = os.path.join(os.path.dirname(__file__), r"missed_data.xlsx")
    assert os.path.exists(path), "set up path to missed_data.xlsx"
    time.sleep(1)   # waiting to close prev events
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(path)
    ws = wb.Worksheets("missed")
    ws.Range(col_name + ":" + col_name).ClearContents()
    for i, info in enumerate(values):
        pointer = col_name + str(i + 2)
        ws.Range(pointer).Value = str(info)
    wb.Save()
    wb.Close()


def verify_excel_file():
    """
     Checks for not overlapping cell values in xlsx file.
    """
    assert os.path.exists(get_description_path()), "set up path to description.xls"
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(get_description_path())
    ws = wb.Worksheets(u"границы сегментов")
    col = "H"
    row = 3
    cell_pointer = col + str(row)
    valid_labels = init_unique_emotion_classes()

    while ws.Range(cell_pointer).Value is not None:
        this_val = ws.Range(cell_pointer).Value
        unique = 0
        for label in valid_labels:
            if label in this_val:
                unique += 1
        assert unique <= 1, "xlsx file has overlapping cell values"
        row += 1
        cell_pointer = col + str(row)
    wb.Close()
    print("verify_excel_file: \tOKAY. Ready to parse xls.")


def parse_whole_xls():
    """
    Supplementary function to check out missed data.
    :returns:
        (1) a collection of file names for each emotion class
        (2) a collection of authors for each emotion class
        (3) a collection of (begin, end) for some emotion file names
    """
    verify_excel_file()

    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(get_description_path())
    ws = wb.Worksheets(u"границы сегментов")
    my_labels_col = "H"
    firsname_col = "I"
    secondname_col = "J"
    author_col = "AB"
    row = 3
    cell_pointer = my_labels_col + str(row)

    emotions_basket = init_container(init_unique_emotion_classes())
    authors_basket = init_container(get_authors())
    boundaries_basket = {}

    while ws.Range(cell_pointer).Value is not None:
        cell_val = ws.Range(cell_pointer).Value
        valid_label = find_valid_label(cell_val)
        firsname_val = str(int(ws.Range(firsname_col + str(row)).Value))
        secondname_val = str(ws.Range(secondname_col + str(row)).Value)
        secondname_val = secondname_val.replace("s", "-")
        secondname_val = secondname_val.replace("e", "-")
        joined_fname = firsname_val + secondname_val
        author = str(ws.Range(author_col + str(row)))
        if valid_label not in emotions_basket:
            # it is not a valid label anymore, actually
            emotions_basket[valid_label] = []
        emotions_basket[valid_label].append(joined_fname)
        authors_basket[author].append(joined_fname)
        boundaries_basket[joined_fname] = ws.Range("K" + str(row)).Value
        row += 1
        cell_pointer = my_labels_col + str(row)
    wb.Close()

    emotions_basket = translate_unicode(emotions_basket)

    return emotions_basket, authors_basket, boundaries_basket


def parse_xls():
    """
    Main function to parse unique emotions (classes) in description.xls
    :returns:
        (1) a collection of file names for each emotion class
        (2) a collection of authors for each emotion class
        (3) a collection of (begin, end) for some emotion file names
    """
    verify_excel_file()

    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(get_description_path())
    ws = wb.Worksheets(u"границы сегментов")
    my_labels_col = "H"
    firsname_col = "I"
    secondname_col = "J"
    author_col = "AB"
    row = 3
    cell_pointer = my_labels_col + str(row)

    emotions_basket = init_container(init_unique_emotion_classes())
    authors_basket = init_container(get_authors())
    boundaries_basket = {}

    while ws.Range(cell_pointer).Value is not None:
        cell_val = ws.Range(cell_pointer).Value
        valid_label = find_valid_label(cell_val)

        firsname_val = str(int(ws.Range(firsname_col + str(row)).Value))
        secondname_val = str(ws.Range(secondname_col + str(row)).Value)
        secondname_val = secondname_val.replace("s", "-")
        secondname_val = secondname_val.replace("e", "-")
        joined_fname = firsname_val + secondname_val
        author = str(ws.Range(author_col + str(row)))

        if valid_label is not None:
            # we do not account for labels we are not interested in
            emotions_basket[valid_label].append(joined_fname)
            authors_basket[author].append(joined_fname)
            boundaries_basket[joined_fname] = ws.Range("K" + str(row)).Value

        row += 1
        cell_pointer = my_labels_col + str(row)

    wb.Close()

    # you can turn off transliteration in case you use Python 3.x
    emotions_basket = translate_unicode(emotions_basket)

    return emotions_basket, authors_basket, boundaries_basket


def how_many_examples_we_have():
    """
     Prints out how many emotion examples we have per one class.
    """
    emotions_basket, _, _ = parse_whole_xls()
    for key in emotions_basket:
        print(key, len(emotions_basket[key]))


if __name__ == "__main__":
    em_basket, auth_basket, bound = parse_xls()
    pprint(em_basket)
