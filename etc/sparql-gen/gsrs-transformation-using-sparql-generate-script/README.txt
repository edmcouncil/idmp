1. Open the GSRS release notes at https://gsrs.ncats.nih.gov/#/release and click the 'Download public data' button. The downloaded archive will have the 'gsrs' extension. Extract data from the downloaded archive
2. Double-check that extracted file has no extension and has the 'public_data' name. If not, rename it to 'public_data'
3. Move the 'public_data' file into the current 'gsrs-transformation-using-sparql-generate-script' folder
4. Create the 'gsrs-transformed' folder in the current directory
5. Run the 'transform-data.sh' script using the following options:
5.1 On Windows: 
  - Open 'Git Bash' and type the './transform-data.sh' command
  - Or use the 'Cygwin' tool and run the 'sh transform-data.sh' command
5.2 On Linux: 
  - Set execute permission on your script using the 'chmod +x transform-data.sh' command and run the './transform-data.sh' command
5.3 On MacOS:
  - Run the transform-data.sh using macOS bash
6. Navigate to the 'gsrs-transformed' folder and use the 'gsrs-transformed.ttl' based on your needs