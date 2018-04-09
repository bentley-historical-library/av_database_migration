from av_database_migration_scripts.config import FMPRO_NSMAP, beal_dir, beal_export_dir
from av_database_migration_scripts.shared.utils import extract_text_from_element
import csv
from lxml import etree
import os

descriptive_elements = {"Item_Identifier": "CollItemNo",
                        "PartIdentifier": "DigFile_Calc",
                        "ItemPart": "ItemPart",
                        "PartTitle": "ItemPartTitle",
                        "PartSegment": "ItemPart_Segment",
                        "ProgramTitle": "ProgramTitle",
                        "Title": "ItemTitle",
                        "ItemDate": "ItemDate",
                        "Abstract": "NoteContent",
                        "TechnicalNote": "NoteTechnical",
                        }

items_to_titles = {}

export_dir = os.path.join(beal_dir, "lib")
items_with_multiple_titles_file = os.path.join(export_dir, "items_with_multiple_titles.csv")
avdigpres_filepath = os.path.join(beal_export_dir, "AVDIGPRES.xml")
tree = etree.parse(avdigpres_filepath)
rows = tree.xpath("//fmpro:ROW", namespaces=FMPRO_NSMAP)
for row in rows:
    item_identifier = extract_text_from_element(row.xpath("./fmpro:CollItemNo", namespaces=FMPRO_NSMAP)[0])
    digfile_calc = extract_text_from_element(row.xpath("./fmpro:DigFile_Calc", namespaces=FMPRO_NSMAP)[0])
    item_title = extract_text_from_element(row.xpath("./fmpro:ItemTitle", namespaces=FMPRO_NSMAP)[0])
    if item_identifier not in items_to_titles:
        items_to_titles[item_identifier] = {}
    if item_title not in items_to_titles[item_identifier]:
        items_to_titles[item_identifier][item_title] = []
    items_to_titles[item_identifier][item_title].append(digfile_calc)

duplicates = [item_identifier for item_identifier, titles in items_to_titles.items() if len(titles.keys()) > 1]
most_titles = max([len(titles.keys()) for item_identifier, titles in items_to_titles.items()])

data = []
for duplicate in duplicates:
    item_data = [duplicate]
    for title, digfile_calcs in items_to_titles[duplicate].items():
        item_data.append(title)
        item_data.append("\n".join(digfile_calcs))
    data.append(item_data)

headers = ["Item_Identifier"]
for i in range(most_titles):
    headers.append("title_{}".format(i+1))
    headers.append("digfile_calcs_{}".format(i+1))

with open(items_with_multiple_titles_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)

