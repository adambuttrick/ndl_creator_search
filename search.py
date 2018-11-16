import re
import csv
import sys
import os
from collections import defaultdict


def exclude(s, excluded_chars):
    fixed = ''.join(char for char in s if char not in excluded_chars)
    return fixed


def parse_date(date, era, adjustment):
    extraneous = ["〔", "〕", "[", "]"]
    if any(e in date for e in extraneous):
        date = ''.join([s for s in date if s not in extraneous])
    if "-" in date:
        date = date.split(era)[1]
        dates = date.split("-")
        dates = [str(int(d) + adjustment) for d in dates]
        date = '-'.join(dates)
    elif "." in date:
        date = date.split(era)[1]
        dates = date.split(".")
        dates = [str(int(dates[0]) + adjustment), dates[1]]
        date = '.'.join(dates)
    else:
        date = date.split(era)[1]
        date = int(date) + adjustment
    return date


def convert_date(date):
    meiji = "明"
    taisho = "大正"
    showa = "昭和"

    if meiji in date:
        date = parse_date(date, meiji, 1867)
    elif taisho in date:
        date = parse_date(date, taisho, 1911)
    elif showa in date:
        date = parse_date(date, showa, 1925)

    return date


def parse_creators(creators):
    creators_dict = {
        "author": "",
        "illustrator": "",
        "translator": "",
        "editor": ""
    }
    excluded = [" ", "著", "原著", "絵", "訳", "編"]
    if "||" in creators:
        creators = creators.split("||")
        if not any("著" in x for x in creators):
            creators_dict["author"] = "no author tagged"
        if not any("絵" in x for x in creators):
            creators_dict["illustrator"] = "no illustrator tagged"
        for creator in creators:
            if " 文" in creator:
                creators_dict["author"] = exclude(creator, excluded)

            if " 著" in creator:
                creators_dict["author"] = exclude(creator, excluded)

            if " 原著" in creator:
                creators_dict["author"] = exclude(creator, excluded)

            if " 絵" in creator:
                creators_dict["illustrator"] = exclude(creator, excluded)

            if " 訳" in creator:
                creators_dict["translator"] = exclude(creator, excluded)

            if "編" in creator:
                creators_dict["editor"] = exclude(creator, excluded)
    else:
        creators_dict["author"] = exclude(creators, excluded)

    creators = list(creators_dict.values())

    return creators


def compare_files(txt_file, csv_file):
    results = []
    header = [
        "URL",
        "title",
        "volume",
        "series",
        "edition",
        "creator",
        "author",
        "illustrator",
        "translator",
        "editor",
        "publisher",
        "date_issued",
        "translated_date_issued",
        "ISBN",
        "extent",
        "access_restrictions",
        "ndc_subject_number"
        "ndc8_subject_id",
        "ndc9_subject_id",
        "ndlc_subject_id",
        "ndlsh_subject"
    ]
    with open(txt_file) as f_in:
        entries = list(set([line.strip() for line in f_in]))

    with open(csv_file) as f_in:
        reader = csv.reader(f_in, dialect="excel-tab")
        for row in reader:
            for entry in entries:
                author = row[5]
                if entry in author:
                    authors = parse_creators(row[5])
                    new_row = row[0:6] + authors + row[6:]
                    new_row.insert(12, convert_date(row[7]))
                    results.append(new_row)

    return [results, header]


def write_results(results, header):
    file_name = os.getcwd() + "/results.csv"
    with open(file_name, 'w') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(header)
        for result in results:
            writer.writerow(result)


if __name__ == '__main__':
    results = compare_files(sys.argv[1], sys.argv[2])
    write_results(results[0], results[1])
