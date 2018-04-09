from av_database_migration_scripts.config import EXPECTED_BEAL_EXPORTS, FMPRO_NSMAP, COLLECTIONID_NORMALIZATION, beal_export_dir
from av_database_migration_scripts.shared.utils import extract_text_from_element, combine_elements_from_row, regex_replacement
from lxml import etree
import operator
import os
import sys


remove_data_elements = ["COLLECTION_INFO.xml", "COLDROOM 2.xml"]

disallowed_values = {
    "AVDIGPRES.xml": {
                    "CollectionID": ["Collection ID", "Collection Id."],
                    "CollItemNo": ["-", "-SR-", "-105", "8730-"],
                    "ItemPartTitle": ["Delete This"],
                    "NoteTechnical": ["Tape does not exist."]
                    },
    "AUDIO_ITEMCHAR.xml": {
                    "ColltemNo": ["coll item number"]
                    }
}

conditional_requirements = {
    "AVDIGPRES.xml": [
        {
            "if": ("CollItemNo", "2014106-37"),
            "then": ("MiVideoID", "1_qa9gbz0a")
        },
        {
            "if": ("CollItemNo", "9618-19"),
            "then": ("AvItemID", "10431")
        },
        {
            "if": ("CollItemNo", "85193-66"),
            "then": ("AvItemID", "6226")
        },
        {
            "if": ("CollItemNo", "2011174-1"),
            "then": ("AvItemID", "6142")
        },
        {
            "if": ("CollItemNo", "2010215-SR-17"),
            "then": ("AvItemID", "2843")
        },
        {
            "if": ("CollItemNo", "8738-SR-24-1"),
            "then": ("AvItemID", "2366")
        }
    ]
}

conditional_normalization = {
    "AVDIGPRES.xml": [
        {
            "element_name": "DigFile_Calc",
            "conditional_function": str.startswith,
            "conditional_argument": "-SR",
            "normalization_type": "combine_elements",
            "normalization_arguments": ["CollectionID", "DigFile_Calc"]
        },
        {
            "element_name": "CollItemNo",
            "conditional_function": operator.eq,
            "conditional_argument": "2009018-1",
            "normalization_type": "regex_replacement",
            "normalization_arguments": ("ItemTitle", r"\(tape \d\)$", "(tapes 1-6)")
        }
    ]
}

normalized_values = {
    "AVDIGPRES.xml": {"CollectionID": COLLECTIONID_NORMALIZATION},
    "COLLECTION_INFO.xml": {"CollectionID": COLLECTIONID_NORMALIZATION}
}

mandatory_fields = {'Audio_dig_workflow.xml': [],
                    'Audio_Genre_LK.xml': [],
                    'AUDIO_ITEMCHAR.xml': [],
                    'Audio_Item_Genre.xml': [],
                    'Audio_Item_Subjects.xml': [],
                    'AUDIO_Playback.xml': ["AudioPlaybackID", "EquipmentName"], 
                    'Audio_Subjects_LK.xml': [],
                    'AVDIGPRES.xml': [],
                    'AVType.xml': [],
                    'AV_Med1a_BrandLK.xml': [], 
                    'AV_Media_Brand.xml': [],
                    'COLDROOM 2.xml': ["Coll_Itemno"],
                    'Digital_Vendor.xml': []
                }

for filename in EXPECTED_BEAL_EXPORTS:
    filepath = os.path.join(beal_export_dir, filename)
    if not os.path.exists(filepath):
        print("{} not found".format(filepath))
        sys.exit()

for filename in os.listdir(beal_export_dir):
    filepath = os.path.join(beal_export_dir, filename)
    tree = etree.parse(filepath)
    if filename in remove_data_elements:
        data_elements = tree.xpath("//fmpro:DATA", namespaces=FMPRO_NSMAP)
        for data_element in data_elements:
            data_element_text = extract_text_from_element(data_element)
            data_element_parent = data_element.getparent()
            data_element_parent_text = extract_text_from_element(data_element_parent)
            data_element_parent.remove(data_element)
            if not data_element_parent_text:
                data_element_parent.text = data_element_text
            elif data_element_parent_text != data_element_text:
                data_element_parent.text = data_element_parent_text + "; " + data_element_text
            else:
                continue
    if filename in mandatory_fields.keys():
        rows = tree.xpath("//fmpro:ROW", namespaces=FMPRO_NSMAP)
        for row in rows:
            for field in mandatory_fields[filename]:
                for element in row.xpath("./fmpro:{}".format(field), namespaces=FMPRO_NSMAP):
                    if not extract_text_from_element(element):
                        row.getparent().remove(row)
    if filename in conditional_requirements.keys():
        rows = tree.xpath("//fmpro:ROW", namespaces=FMPRO_NSMAP)
        for row in rows:
            for conditional_requirement in conditional_requirements[filename]:
                if_field, if_value = conditional_requirement["if"]
                if_element = row.xpath("./fmpro:{}".format(if_field), namespaces=FMPRO_NSMAP)[0]
                if extract_text_from_element(if_element) == if_value:
                    then_field, then_value = conditional_requirement["then"]
                    then_element = row.xpath("./fmpro:{}".format(then_field), namespaces=FMPRO_NSMAP)[0]
                    if not extract_text_from_element(then_element) == then_value:
                        row.getparent().remove(row)
    if filename in normalized_values.keys():
        rows = tree.xpath("//fmpro:ROW", namespaces=FMPRO_NSMAP)
        for row in rows:
            for field in normalized_values[filename]:
                for element in row.xpath("./fmpro:{}".format(field), namespaces=FMPRO_NSMAP):
                    element_text = extract_text_from_element(element)
                    if normalized_values[filename][field].get(element_text):
                        element.text = normalized_values[filename][field][element_text]
    if filename in disallowed_values.keys():
        rows = tree.xpath("//fmpro:ROW", namespaces=FMPRO_NSMAP)
        for row in rows:
            for field in disallowed_values[filename]:
                for element in row.xpath("./fmpro:{}".format(field), namespaces=FMPRO_NSMAP):
                    if extract_text_from_element(element) in disallowed_values[filename][field]:
                        row.getparent().remove(row)
    if filename in conditional_normalization.keys():
        for normalization_rule in conditional_normalization[filename]:
            normalization_element_name = normalization_rule["element_name"]
            conditional_function = normalization_rule["conditional_function"]
            conditional_argument = normalization_rule["conditional_argument"]
            normalization_elements = tree.xpath("//fmpro:{}".format(normalization_element_name), namespaces=FMPRO_NSMAP)
            for normalization_element in normalization_elements:
                normalization_element_text = extract_text_from_element(normalization_element)
                if conditional_function(normalization_element_text, conditional_argument):
                    if normalization_rule["normalization_type"] == "combine_elements":
                        row = normalization_element.getparent()
                        normalization_arguments = normalization_rule["normalization_arguments"]
                        normalization_element.text = combine_elements_from_row(row, normalization_arguments)
                    elif normalization_rule["normalization_type"] == "regex_replacement":
                        row = normalization_element.getparent()
                        element_name, regex_match, replacement = normalization_rule["normalization_arguments"]
                        regex_replacement(row, element_name, regex_match, replacement)        
            
    with open(filepath, "wb") as f:
        f.write(etree.tostring(tree, encoding="utf-8", pretty_print=True))
