# quay-away

This project showcases an example for air-gapped k8s installations. This especially replaces quay.io images with a registry of the users choice. Simply edit the `DOCKER_REGISTRY` variable in `webhook-base.yml` to your needs.

### Quickstart

```bash
kubectl apply -f webhook-base.yaml
./gen-self-cert.sh
```
put the output CABundle certificate in webhook-configuration.yaml (each REPLACE_CERT_HERE iteration)

```bash
kubectl apply -f webhook-configuration.yaml
```

### Usage

Newly created Pods will now automatically be redirected from quay.io to your registry.
