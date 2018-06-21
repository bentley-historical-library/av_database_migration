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

programs_to_titles = {}

export_dir = os.path.join(beal_dir, "lib")
program_titles_file = os.path.join(export_dir, "program_titles.csv")
avdigpres_filepath = os.path.join(beal_export_dir, "AVDIGPRES.xml")
tree = etree.parse(avdigpres_filepath)
rows = tree.xpath("//fmpro:ROW", namespaces=FMPRO_NSMAP)
for row in rows:
    program_title_path = row.xpath("./fmpro:ProgramTitle", namespaces=FMPRO_NSMAP)
    if program_title_path and extract_text_from_element(program_title_path[0]):
        item_identifier = extract_text_from_element(row.xpath("./fmpro:CollItemNo", namespaces=FMPRO_NSMAP)[0])
        program_title = extract_text_from_element(program_title_path[0])
        item_title = extract_text_from_element(row.xpath("./fmpro:ItemTitle", namespaces=FMPRO_NSMAP)[0])
        if program_title not in programs_to_titles:
            programs_to_titles[program_title] = {}
        if item_title not in programs_to_titles[program_title]:
            programs_to_titles[program_title][item_title] = []
        programs_to_titles[program_title][item_title].append(item_identifier)

most_items = max([len(item_titles.keys()) for _, item_titles in programs_to_titles.items()])

data = []
for program_title in programs_to_titles.keys():
    program_data = [program_title]
    for item_title, item_identifiers in programs_to_titles[program_title].items():
        program_data.append(item_title)
        program_data.append("\n".join(item_identifiers))
    data.append(program_data)

headers = ["program_title"]
for i in range(most_items):
    headers.append("item_title_{}".format(i+1))
    headers.append("item_identifiers_{}".format(i+1))

with open(program_titles_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)
