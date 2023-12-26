import oci
import os

# Get environment variables
oci_user_id = os.environ.get("OCI_USER_ID")
oci_key_file_path = os.environ.get("OCI_KEY_FILE_PATH")
oci_key_file_fingerprint = os.environ.get("OCI_KEY_FILE_FINGERPRINT")
oci_tenancy = os.environ.get("OCI_TENANCY")
oci_region = os.environ.get("OCI_REGION")
oci_compartment_id = os.environ.get("OCI_COMPARTMENT_ID")
oci_bucket_name = os.environ.get("OCI_BUCKET_NAME")

# Set your Oracle Cloud credentials and configuration
config = {
    "user": oci_user_id,
    "key_file": oci_key_file_path,
    "fingerprint": oci_key_file_fingerprint,
    "tenancy": oci_tenancy,
    "region": oci_region,
    "compartment": oci_compartment_id
}

# Create a client
object_storage = oci.object_storage.ObjectStorageClient(config)

# Specify the file to be uploaded
file_to_upload = "/path/to/test.txt"

# Create a stream for the file
with open(file_to_upload, "rb") as file:
    object_data = file.read()

# Specify the object name (file name in the bucket)
object_name = os.path.basename(file_to_upload)

# Get the namesapce
object_storage_namesapce = object_storage.get_namespace().data

# Upload the file to the bucket
object_storage.put_object(
    namespace_name=object_storage_namesapce,
    bucket_name=oci_bucket_name,
    object_name=object_name,
    put_object_body=object_data
)

print(f"File {object_name} uploaded to {oci_bucket_name} bucket.")
