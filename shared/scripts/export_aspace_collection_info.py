from av_database_migration.config import aspace_data_dir
from ASpaceAPI import ASpace
import csv
import os
from tqdm import tqdm

aspace = ASpace()
resource_ids = aspace.list_resources()
data = []
for resource_id in tqdm(resource_ids):
    resource_info = {}
    resource = aspace.get_resource(resource_id)
    resource_info["aspace_uri"] = resource["uri"]
    resource_info["title"] = aspace.make_display_string(resource).encode("utf-8")
    resource_info["creator"] = aspace.get_resource_creator(resource).encode("utf-8")
    resource_info["ead_id"] = resource.get("ead_id")
    resource_info["collection_id"] = aspace.get_collection_id(resource)
    if any([instance for instance in resource["instances"] if instance["instance_type"] == "digital_object"]):
        dspace_handles = aspace.get_digital_object_instance_links(resource, match_pattern="hdl.handle.net")
        resource_info["dspace_handle"] = "; ".join(dspace_handles)
    else:
        resource_info["dspace_handle"] = ""
    data.append(resource_info)

aspace_collection_info_csv = os.path.join(aspace_data_dir, "collection_info.csv")
headers = ["collection_id", "ead_id", "title", "creator", "aspace_uri", "dspace_handle"]
with open(aspace_collection_info_csv, "wb") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)



    

