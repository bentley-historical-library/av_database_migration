from av_database_migration_scripts.config import FMPRO_NSMAP

import re


def extract_text_from_element(element):
    if element.text is not None:
        return element.text.strip().replace('“', '"').replace('”', '"')
    else:
        return ""


def combine_elements_from_row(row, element_names, separator=""):
    element_values = []
    for element_name in element_names:
        element = row.xpath("./fmpro:{}".format(element_name), namespaces=FMPRO_NSMAP)[0]
        element_value = extract_text_from_element(element)
        element_values.append(element_value)
    return "{}".format(separator).join(element_values)


def regex_replacement(row, element_name, regex_match, replacement):
    element = row.xpath("./fmpro:{}".format(element_name), namespaces=FMPRO_NSMAP)[0]
    element_text = extract_text_from_element(element)
    element.text = re.sub(regex_match, replacement, element_text)