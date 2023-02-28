# Minimum Requirements

1. Install Docker. Follow https://docs.docker.com/get-docker instructions.
1. Login to https://spor.ema.europa.eu/. The login button is located in the top right corner. Create one if you don't have an account.
1. Download the `referentials` dataset from https://spor.ema.europa.eu/rmswi/#/lists.
    1. Choose the list that you want to transform (eg: `Age Range`).
    1. Click the `Export` icon on the right side in the `Actions` column.
    1. A popup will show, choose format CSV and click the `Export` button.
    1. The downloaded file will be in ZIP format (eg: `export-100000000001.zip`).
1. Extract/unzip the zip file (eg: `export-100000000001.zip`). The extracted file will be in CSV format (eg: `100000000001.csv`).
1. Copy the CSV file (eg: `100000000001.csv`) to this folder (i.e. `etc/transformation/SPOR/referentials`).

## Create an Ontology File
1. Create a new CSV file inside of this folder (i.e. `etc/transformation/SPOR/referentials`), and named it using the same list ID from the previous task (eg: `100000000001-ontology.csv`).
1. Inside the CSV file create a header like below:
    ```
    Identifier,Name,Owner,Domain,Status,Modified on,Created on,Version
    ```
1. Add additional metadata information from the list. This information can be seen in the https://spor.ema.europa.eu/rmswi/#/lists by clicking the right arrow icon on the left of a list. Example metadata for list `Age Range`:
    ```
    100000000001,"Age Range",EMA,Human and Veterinary use,CURRENT,2022-03-23T11:05:54,2007-09-12T00:00:00,75
    ```
1. So the final file of `100000000001-ontology.csv` will look like this:
    ```
    Identifier,Name,Owner,Domain,Status,Modified on,Created on,Version
    100000000001,"Age Range",EMA,Human and Veterinary use,CURRENT,2022-03-23T11:05:54,2007-09-12T00:00:00,75
    ```

## Update spor-referentials.rqg File
1. Open the `spor-referentials.rqg` file.
1. Find the line:
    ```
    ITERATOR iter:CSV(?ontology_source) AS
    ```
    Change it with the ontology file that we created from the previous task (eg: `100000000001-ontology.csv`).
    ```
    ITERATOR iter:CSV(<100000000001-ontology.csv>) AS
    ```
1. Find the line:
    ```
    ITERATOR iter:CSV(?source) AS
    ```
    Change it with the extracted CSV file (eg: `100000000001.csv`).
    ```
    ITERATOR iter:CSV(<100000000001.csv>) AS
    ```

# Transformation

Instructions for transforming the SPOR referentials data.

## Local

1. Run `./transform-local.sh` from the terminal console.

## Accurids

1. Upload `spor-referentials.rqg` & the CSV files (eg: `100000000001.csv` & `100000000001-ontology.csv`) files to Accurids https://pistoiaalliance.dev.accurids.com.
