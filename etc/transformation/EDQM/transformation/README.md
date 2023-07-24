Transformation scripts for [EDQM](https://standardterms.edqm.eu/) datasets.

# Minimum Requirements

1. Install Docker. Follow https://docs.docker.com/get-docker instructions.
1. Get EDQM ressource you want to tranform (follow instructions in /transformation/EDQM folder)
1. Copy EDQM .json file you want to transform to the same folder like the generic_transformation file (generic_transformation.rqg).
1. Open `generic_transformation.rqg` file (inside this folder), replace `<?source>` with the name of the file you want to transform (e.g. `edqm-pdf.json`) and save it.
1. Open `transform-local.sh` file (inside this folder), replace `<CHANGE ME !!!!>` with the EDQM class you want to transform (e.g. `edqm-pdf`) and save it.
1. Transform data by running `transform.local.sh`.
