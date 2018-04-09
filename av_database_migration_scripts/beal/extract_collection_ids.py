from av_database_migration_scripts.config import FMPRO_NSMAP, beal_dir, beal_export_dir
from lxml import etree
import os

collection_ids = []
export_dir = os.path.join(beal_dir, "lib")
collection_id_file = os.path.join(export_dir, "collection_ids.txt")
collection_info_filepath = os.path.join(beal_export_dir, "COLLECTION_INFO.xml")
tree = etree.parse(collection_info_filepath)
collection_id_elements = tree.xpath("//fmpro:CollectionID", namespaces=FMPRO_NSMAP)
for collection_id_element in collection_id_elements:
    if collection_id_element.text is not None and collection_id_element.text.strip() not in collection_ids:
        collection_ids.append(collection_id_element.text.strip())

with open(collection_id_file, "w") as f:
    f.write("\n".join(collection_ids))

