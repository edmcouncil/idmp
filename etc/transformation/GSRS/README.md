# Minimum Requirements

1. Install Docker. Follow https://docs.docker.com/get-docker instructions.
1. Open the GSRS release notes at https://gsrs.ncats.nih.gov/#/release and click the `public data` button in `Download public data` section. The downloaded archive will have the `gsrs` extension.
1. Double-check that file, it must have the name `public_data.gsrs` name. If not, rename it to `public_data.gsrs`.
1. Copy `public_data.gsrs` file to this folder (i.e. `etc/transformation/GSRS`).

# Transformation

Instructions for transforming the GSRS data.

## Local

1. Run `./transform-local.sh` from the terminal console.

## Accurids

1. Run `./transform-accurids.sh` from the terminal console.
1. Upload `public_data.json`, `gsrs-public-data-substances.rqg`, `gsrs-public-data-relationships.rqg`, `gsrs-public-data-names.rqg`, and `gsrs-public-data-identifiers.rqg` files to Accurids https://pistoiaalliance.dev.accurids.com.
