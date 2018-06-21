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

export_dir = os.path.join(beal_dir, "lib")
item_descriptions_file = os.path.join(export_dir, "item_descriptions.csv")
avdigpres_filepath = os.path.join(beal_export_dir, "AVDIGPRES.xml")
tree = etree.parse(avdigpres_filepath)
rows = tree.xpath("//fmpro:ROW", namespaces=FMPRO_NSMAP)
data = []
for row in rows:
    item_metadata = {}
    for field, element_path in descriptive_elements.items():
        element = row.xpath("./fmpro:{}".format(element_path), namespaces=FMPRO_NSMAP)[0]
        item_metadata[field] = extract_text_from_element(element)
    data.append(item_metadata)

headers = ["Item_Identifier", "PartIdentifier", "ProgramTitle", "Title", "ItemPart", "PartTitle", "PartSegment", "ItemDate", "Abstract", "TechnicalNote"]

with open(item_descriptions_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)
