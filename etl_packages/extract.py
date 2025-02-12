import boto3
import json
import xml.etree.ElementTree as ET

s3_client = boto3.client("s3")

def load_metadata(metadata_path):
    """Load metadata.json from S3."""
    s3_client = boto3.client("s3")
    bucket_name, key = metadata_path.replace("s3://", "").split("/", 1)
    
    response = s3_client.get_object(Bucket=bucket_name, Key=key)
    metadata = json.loads(response["Body"].read().decode("utf-8"))
    
    return metadata

def extract_from_s3(bucket_name, metadata_path):
    """Extract data dynamically from S3 using metadata.json."""
    metadata = load_metadata(metadata_path)
    files_metadata = metadata["files"]
    
    extracted_data = []

    for file_key, details in files_metadata.items():
        file_pattern = details["file_pattern"]
        response = s3_client.get_object(Bucket=bucket_name, Key=file_pattern)
        content = response["Body"].read().decode("utf-8")

        if file_pattern.endswith(".json"):
            extracted_data.extend(json.loads(content))

        elif file_pattern.endswith(".xml"):
            extracted_data.extend(parse_xml(content))

    return extracted_data

def parse_xml(xml_string):
    """Parse XML into a list of dictionaries."""
    root = ET.fromstring(xml_string)
    data_list = []
    
    for entry in root.findall("record"):
        data_dict = {child.tag: child.text for child in entry}
        data_list.append(data_dict)
    
    return data_list
