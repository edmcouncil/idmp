1. Open the GSRS release notes at https://gsrs.ncats.nih.gov/#/release and click the 'Download public data' button. The downloaded archive will have the 'gsrs' extension. Extract data from the downloaded archive
2. Double-check that extracted file has no extension and has the 'public_data' name. If not, rename it to 'public_data'
3. Move the 'public_data' file into the current 'gsrs-transformation-using-accurids' folder
4. Run the 'convert-file-json.sh' script using the following options:
4.1 On Windows: 
  - Open 'Git Bash' and type the './convert-file-to-json.sh' command
  - Or use the 'Cygwin' tool and run the 'sh convert-file-to-json.sh' command
4.2 On Linux: 
  - Set execute permission on your script using the 'chmod +x convert-file-to-json.sh' command and run the './convert-file-to-json.sh' command
4.3 On MacOS:
  - Run the convert-file-to-json.sh using macOS bash
6. Upload public_data.json and the gsrs-public-data-substances.rqg, gsrs-public-data-relationships.rqg, gsrs-public-data-names.rqg and gsrs-public-data-identifiers.rqg migration files to Accurids https://pistoiaalliance.dev.accurids.com/