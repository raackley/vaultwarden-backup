# vaultwarden-backup

## Description
This project allows for easy backup from Vaultwarden, deployed to a kubernetes cluster, to Oracle Cloud Object Storage.  Oracle Cloud Object Storage was chosen over Amazon AWS S3 simply becasue Oracle gives you a good amount of Object Storage for free, so why not.  Support for the more popular Amazon AWS S3 might be considered in the future.

This backup application is designed to run on a Kubernetes cluster, and it is designed to backup Vaultwarden running on that same Kubernetes cluster, in the same namespace.  Therefore, as a prereq, you must already be running Vaultwarden on Kubernetes.  This is tested against this [Vaultwarden helm chart](https://charts.gabe565.com/charts/vaultwarden/).

This application is packaged into a Helm chart for ease of use.  It is a Kubernetes Cronjob with a configurable schedule.  See below for instructions and values.

## Prerequisites

* Vaultwarden deployed to a Kubernetes cluster using SQLite
* An Oracle Cloud (OCI) account with an Object Storage buck and an API key that can access it

## Installation
Create secret `oci-key` in the namespace where vaultwarden is already installed, using the OCI key for your user with Object Storage permissions.

```
kubectl create secret generic oci-key --from-file=key.pem=/path/to/key.pem -n <your vaultwarden namespace>
```


Add and update the Helm repo.

```
helm repo add raackley-charts https://charts.ryanackley.com
```

```
helm repo update
```

Install (Helm v3).

```
helm install <release name> -n <your vaultwarden namespace> raackley-stable/vaultwarden-backup
```

## Helm Values
| Parameter | Description | Default Value | Required? |
| --- | --- | --- | --- |
| cron_schedule | Schedule in Cron syntax | "0 5 * * 5" | N |
| oci_user_id | OCI User ID | <none> | Y |
| oci_key_fingerprint | OCI API Key Fingerprint | <none> | Y |
| oci_tenancy | OCI Tenancy ID | <none> | Y |
| oci_region | OCI region | <none> | Y |
| oci_compartment_id | OCI Compartment ID | <none> | Y |
| oci_bucket_name | OCI Bucket Name | <none> | Y |
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