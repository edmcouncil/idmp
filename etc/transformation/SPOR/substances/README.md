# Minimum Requirements

1. Install Docker. Follow https://docs.docker.com/get-docker instructions.
1. Download the `substances` dataset from https://spor.ema.europa.eu/smswi/#/ by clicking the `Download SMS Export` link. The downloaded file will be in CSV format.
1. Rename the file to become `sms-substances-list.csv`.
1. Change the header name inside `sms-substances-list.csv` from `#SMS_ID` to `SMS_ID`.
1. Copy `sms-substances-list.csv` file to this folder (i.e. `etc/transformation/SPOR/substances`).

# Transformation

Instructions for transforming the SPOR substances data.

## Local

1. Run `./transform-local.sh` from the terminal console.

## Accurids

1. Upload `sms-substances-list.csv`, and `spor-substances.rqg` files to Accurids https://pistoiaalliance.dev.accurids.com.
