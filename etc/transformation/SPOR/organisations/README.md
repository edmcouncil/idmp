# Minimum Requirements

1. Install Docker. Follow https://docs.docker.com/get-docker instructions.
1. Download the `organisations` dataset from https://spor.ema.europa.eu/omswi/#/searchOrganisations by clicking the `Export All Organisations` link. The downloaded file will be in ZIP format (eg: `locations.zip`).
1. Extract/unzip the zip file (eg: `locations.zip`). The extracted file will be in CSV format (eg: `locations.csv`).
1. Make sure the CSV filename is `locations.csv`.
1. Copy `locations.csv` file to this folder (i.e. `etc/transformation/SPOR/organisations`).

## Cleanup Data

Unfortunately this `locations.csv` require some cleanup before we can use it.

1. Remove entry in line `14364` (i.e. `Organisation ID: ORG-100011833`). Reason: Data is too long.
1. Update entry with Alternative Name `"Ośrodek Diabetologiczny "Popula" Elżbieta Popławska, Grażyna Laszewska Sp. j."` to `"Ośrodek Diabetologiczny 'Popula' Elżbieta Popławska, Grażyna Laszewska Sp. j."`. Reason: Invalid double quote.
1. Update entry with Alternative Name `""Pharmamagist" Gyógyszeripari, Kereskedelmi És Szolgáltató kft.¦Pharmamagist Ltd."` to `"'Pharmamagist' Gyógyszeripari, Kereskedelmi És Szolgáltató kft.¦Pharmamagist Ltd."`. Reason: Invalid double quote.

# Transformation

Instructions for transforming the SPOR organisations data.

## Local

1. Run `./transform-local.sh` from the terminal console.

## Accurids

1. Upload `locations.csv`, and `spor-organisations.rqg` files to Accurids https://pistoiaalliance.dev.accurids.com.
