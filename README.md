# quay-away

This project enabled air-gapped k8s helm installations. Simply edit the `REGISTRY_REGEX` environment variable in `webhook-base.yml`
to specify replacements.



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

Replacements are specified in the following format: `search|replacement`

Multiple replacements may be specified separated by a space. Python syntax is used so replacements can access captured groups by doing `\1`.

Example: `^quay\\.io/.*/(.*)$|local-registry.de/quay/\\1`. This will rewrite all quay.io images to `local-registry.de/quay/name`. E.g. `quay.io/calico/node` becomes `local-registry.de/quay/node`.