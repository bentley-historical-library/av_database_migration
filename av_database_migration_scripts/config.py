import os

COLLECTIONID_NORMALIZATION = {
    "852178.5": "852178",
    "852178_5": "852178"
}

FMPRO_NSMAP = {"fmpro": "http://www.filemaker.com/fmpdsoresult"}
EXPECTED_BEAL_EXPORTS = [
                        'Audio_dig_workflow.xml',
                        'Audio_Genre_LK.xml',
                        'AUDIO_ITEMCHAR.xml',
                        'Audio_Item_Genre.xml',
                        'Audio_Item_Subjects.xml',
                        'AUDIO_Playback.xml',
                        'Audio_Subjects_LK.xml',
                        'AVDIGPRES.xml',
                        'AVType.xml',
                        'AV_Med1a_BrandLK.xml',
                        'AV_Media_Brand.xml',
                        'COLDROOM 2.xml',
                        'COLLECTION_INFO.xml',
                        'Digital_Vendor.xml'
                        ]

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, "data")
beal_dir = os.path.join(data_dir, "beal")
beal_export_dir = os.path.join(beal_dir, "exports")
shared_dir = os.path.join(data_dir, "shared")
aspace_data_dir = os.path.join(shared_dir, "aspace_exports")
kaltura_data_dir = os.path.join(shared_dir, "kaltura_exports")
