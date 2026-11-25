# vaultwarden-backup

## Description
This project allows for easy backup from Vaultwarden, deployed to a kubernetes cluster, to AWS S3 (or compatible) buckets, and/or to Oracle Cloud Object Storage.  Oracle Cloud Object Storage provides a generous amount of Object Storage for free, so it can be a good option for these backups.

This backup application is designed to run on a Kubernetes cluster, and it is designed to backup Vaultwarden running on that same Kubernetes cluster, in the same namespace.  Therefore, as a prereq, you must already be running Vaultwarden on Kubernetes.  This is tested against this [Vaultwarden helm chart](https://charts.gabe565.com/charts/vaultwarden/).

This application is packaged into a Helm chart for ease of use.  It is a Kubernetes Cronjob with a configurable schedule.  See below for instructions and values.

## Prerequisites

* Vaultwarden deployed to a Kubernetes cluster using SQLite
* An Oracle Cloud (OCI) account with an Object Storage buck and an API key that can access it

## Installation
### When using OCI Object Storage
Create secret `oci-key` in the namespace where vaultwarden is already installed, using the OCI key for your user with Object Storage permissions.

```
kubectl create secret generic oci-key --from-file=key.pem=/path/to/key.pem -n <your vaultwarden namespace>
```

### When using AWS S3 Object Storage
Create secret `s3-key` in the namespace where vaultwarden is already installed.

```
kubectl create secret generic s3-key --from-literal=AWS_ACCESS_KEY_ID=<your key id> --from-literal=AWS_SECRET_ACCESS_KEY=<your secret key> -n <your vaultwarden namespace>
```

### Install with Helm

Charts are published as OCI artifacts to the GitHub Container Registry (no login or
repository setup required).

Install the latest published version (check
https://github.com/raackley?tab=packages for available versions):

​```
helm install vaultwarden-backup \
  oci://ghcr.io/raackley/charts/vaultwarden-backup \
  --version 1.0.0
​```

To upgrade later:

​```
helm upgrade vaultwarden-backup \
  oci://ghcr.io/raackley/charts/vaultwarden-backup \
  --version 1.0.1
​```

## Helm Values
| Parameter | Description | Default Value | Required? |
| --- | --- | --- | --- |
| cron_schedule | Schedule in Cron syntax | "0 5 * * 5" | N |
| oci_enabled | Upload to OCI storage or not | "not_enabled" | N |
| s3_enabled | Upload to S3 storage or not | "not_enabled" | N |
| oci_user_id | OCI User ID | <none> | N |
| oci_key_fingerprint | OCI API Key Fingerprint | <none> | N |
| oci_tenancy | OCI Tenancy ID | <none> | N |
| oci_region | OCI region | <none> | N |
| oci_compartment_id | OCI Compartment ID | <none> | N |
| oci_bucket_name | OCI Bucket Name | <none> | N |
| s3_bucket_name | S3 Bucket Name | <none> | N |
| s3_endpoint_url | S3 Endpoint URL | "s3.amazonaws.com" | N |
| s3_region_name | S3 Region | "us-east-1" | N |
| data_mountpath | Where Vaultwarden's data is | "/data" | N |
| secret_key_mountpath | Where your Secret key file gets mounted | "/oci" | N |
| data_pvc_name | The name of your Vaultwarden PVC | "vaultwarden-data" | N |

## What gets backed up?
The following files and directories are backed up with this project.  This is in accordance with the recommendations from the [Vaultwarden wiki](https://github.com/dani-garcia/vaultwarden/wiki/Backing-up-your-vault).

* db.sqlite3 (SQLite database dump)
* `attachments` directory
* `sends` directory
* `config.json` file

### Files NOT backed up
* `rsa_key*` files
* `icon_cache` directory