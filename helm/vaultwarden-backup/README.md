# Vaultwarden Backup

This chart deploys a Kubernetes cronjob that backs up vaultwarden if it is deployed on your cluster.

## Installation
Create secret `oci-key` in the namespace where vaultwarden is already instealled, using the OCI key for your user with Object Storage permissions.

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
