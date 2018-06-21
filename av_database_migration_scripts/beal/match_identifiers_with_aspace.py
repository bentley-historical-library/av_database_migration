from aspaceapi import ASpaceAPIClient as AS

from av_database_migration_scripts.config import FMPRO_NSMAP, beal_dir, beal_export_dir
from av_database_migration_scripts.shared.utils import extract_text_from_element

import csv
from lxml import etree
import os
from tqdm import tqdm

export_dir = os.path.join(beal_dir, "lib")
aspace_uris_file = os.path.join(export_dir, "reconciled_identifiers.csv")
avdigpres_filepath = os.path.join(beal_export_dir, "AVDIGPRES.xml")
tree = etree.parse(avdigpres_filepath)
rows = tree.xpath("//fmpro:ROW", namespaces=FMPRO_NSMAP)

identifiers = []
for row in rows:
    item_identifier = extract_text_from_element(row.xpath("./fmpro:CollItemNo", namespaces=FMPRO_NSMAP)[0])
    part_identifier = extract_text_from_element(row.xpath("./fmpro:DigFile_Calc", namespaces=FMPRO_NSMAP)[0])
    if item_identifier:
        identifiers.append({"type": "item_identifier", "value": item_identifier})
    if part_identifier:
        identifiers.append({"type": "part_identifier", "value": part_identifier})

aspace = AS()
for identifier in tqdm(identifiers):
    value = identifier["value"]
    reconcilation = aspace.resolve_component_id(value)
    status, result = [(status, result) for status, result in reconcilation.items()][0]
    identifier["status"] = status
    identifier["result"] = result

headers = ["type", "value", "status", "result"]
with open(aspace_uris_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(identifiers)
