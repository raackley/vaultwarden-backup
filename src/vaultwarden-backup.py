import oci
import os
import shutil
import tarfile
from datetime import datetime

# Get environment variables
oci_user_id = os.environ.get("OCI_USER_ID")
oci_key_file_path = os.environ.get("OCI_KEY_FILE_PATH")
oci_key_file_fingerprint = os.environ.get("OCI_KEY_FILE_FINGERPRINT")
oci_tenancy = os.environ.get("OCI_TENANCY")
oci_region = os.environ.get("OCI_REGION")
oci_compartment_id = os.environ.get("OCI_COMPARTMENT_ID")
oci_bucket_name = os.environ.get("OCI_BUCKET_NAME")

# Get the current date and time
current_datetime = datetime.now()

# Format the date and time as per your requirement
formatted_date_time = current_datetime.strftime("%Y%m%d-%H%M")

# Paths and file names
source_dir = "/data"
backup_file_name = f"db-{formatted_date_time}.sqlite3"
backup_dir = f"/backups/{formatted_date_time}"
backup_archive_file = f"{backup_dir}/vaultwarden-backup-{formatted_date_time}.tar.gz"

# Backup running db to /backups
os.system(f"mkdir -p {backup_dir}") 
os.system(f"sqlite3 {source_dir}/db.sqlite3 \".backup '{backup_dir}/{backup_file_name}'\"")

# Copy extra directories and files, attachments, sends, config.json
shutil.copytree(f"{source_dir}/attachments", f"{backup_dir}/attachments")
shutil.copytree(f"{source_dir}/sends", f"{backup_dir}/sends")
shutil.copyfile(f"{source_dir}/config.json", f"{backup_dir}/config.json")

# Compress directory into archive
tar = tarfile.open(backup_archive_file, "w:gz")
tar.add(backup_dir)
tar.close()

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

# Create a stream for the file
with open(backup_archive_file, "rb") as file:
    object_data = file.read()

# Specify the object name (file name in the bucket)
object_name = os.path.basename(backup_archive_file)

# Get the namespace
object_storage_namespace = object_storage.get_namespace().data

# Upload the file to the bucket
object_storage.put_object(
    namespace_name=object_storage_namespace,
    bucket_name=oci_bucket_name,
    object_name=object_name,
    put_object_body=object_data
)

print(f"File {object_name} uploaded to {oci_bucket_name} bucket.")
