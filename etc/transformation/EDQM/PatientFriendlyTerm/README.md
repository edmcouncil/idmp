# Minimum Requirements

1. Install Docker. Follow https://docs.docker.com/get-docker instructions.
1. Retrieve EDQM data as described in README for API.
1. Copy the JSON file (`EDQM-PFT.json`) to this folder (i.e. `etc/transformation/EDQM/PatientFriendlyTerm`).

# Transformation

Instructions for transforming the EDQM data.

## Local

1. Run `./transform-local.sh` from the terminal console.

## Accurids

1. Upload `edqm-patient-friendly-term.rqg` & the corresponding JSON file to Accurids https://pistoiaalliance.dev.accurids.com.
