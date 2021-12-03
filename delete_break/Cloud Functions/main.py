import re
from google.cloud import storage

storage_client = storage.Client()

def hello_gcs(event, context):
    old_str = "\n"
    new_str = ""
    new_data = ""
    bucket_name = event['bucket']
    object_name = event['name']

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    with blob.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.replace(old_str,new_str)
            if re.search('[0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9] --> [0-9][0-9]:[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9]', line):
                line = '\n' + line
                line = line + '\n'
            elif re.search('^[0-9]+$', line):
                line = '\n\n' + line
            new_data += line
    with blob.open("w", encoding="utf-8") as f:
        f.write(new_data)
