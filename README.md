# trufflehog-url-parser
Uses trufflehog to parse a file containing target URLs

# Operation
Using the command line, call the python file with a list of URLs (one line per URL). This script will use the filesystem argument with trufflehog. It uses the requests module to make the request every 2 seconds with a 5 second timout, and only parses status codes of 200. After going through the list of URLs, 4 files will be created:

- output_data: contains the unparsed unverified data from running: trufflehog filesystem [url]

![image](https://github.com/user-attachments/assets/0b99b1d2-28cb-4a09-8fdc-c19436a7b95f)

- output_urls: contains the urls that had a finding from the list of urls

![image](https://github.com/user-attachments/assets/7bb5f40f-79b7-4e2d-b62c-640f58651e5b)
  
- output_verified_data: contains the verified data found from trufflehog

![image](https://github.com/user-attachments/assets/76aa5a40-2707-469f-8e0f-270c358e887c)

- output_results: contains only the detector type and raw results from the output_data file

![image](https://github.com/user-attachments/assets/da115d44-89cc-4793-aec6-3374edee266b)

# Progress
The program displays progress to the user by adding # signs after every request, and if any data is found, the URL is displayed on the screen.

![image](https://github.com/user-attachments/assets/d7c8c3b0-bcfb-4ec5-aad8-7d6c021013b8)

# Completion
Once the script is done executing, the total number of verified and unverified secrets are displayed.

![image](https://github.com/user-attachments/assets/be2bb2e6-80b9-44cf-b970-e1c1aa7d099c)

# Execute
python3 trufflehog_script.py urls

# Example URL file
One URL per line:

![image](https://github.com/user-attachments/assets/27b9263f-9f14-499e-a26f-4de377954f83)
