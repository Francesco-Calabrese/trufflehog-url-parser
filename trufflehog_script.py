#!/usr/python3
#This program uses trufflehog and a supplied list of URLs to search for any verified or unverified secrets.
#Supply a file containing URLs as a command line argument. Will not evaluate image/audio/svg files.
#Uses a time delay of 2 seconds between sending requests.
#Outputs the results in 4 files - verified data, unverified data, results (parsed from detector type and 
#raw results), and urls
import sys
import os
import subprocess
import requests
import time

#parses the results of trufflehog to get the detector type and the raw results. saves
#the ouput as output_results
def get_all_detectors(p):
	results_dict = {}
	output_results = open("output_results", "a")

	items = p.split(":")
	det_flag = False
	res_flag = False
	det_value = ""
	res_value = ""
	for item in items:
		#detector type is found, store next item to variable
		if det_flag:
			det_value = item.strip().split()[0]
			det_flag = False
		if "Detector Type" in item:
			det_flag = True

		#results are found, store next item to variable
		if res_flag:
			res_value = item.strip().split()[0]
			res_flag = False

			#adds keys and values to dictionary from the saved variables
			if det_value not in results_dict:
				results_dict[det_value] = []
			results_dict[det_value].append(res_value)
		if "Raw result" in item:
			res_flag = True

	#removes any duplicates in the results and detector list values
	for key in results_dict.keys():
		results_dict[key] = list(set(results_dict[key]))

	#writes each dictionary key/value (non duplicates) to file
	output_results.write(url)
	for key,values in results_dict.items():
		for i in range(len(values)):
			output_results.write("Detector Type: {}\tRaw Results: {}\n".format(key, results_dict[key][i]))

	#closes file
	output_results.write("\n\n")
	output_results.close()


#writes the unparsed data to a file and calls a function to parse data and save to file
def write_to_file(verified, url, p):
	if verified == True:
		output_verified_data.write("URL: {}\nData:\n{}\n\n".format(url.strip(), p))
		print("\nVERIFIED SECRET FOUND on page: {}".format(url.strip()))
	else:
		output_urls.write(url)
		output_data.write("URL: {}\nData:\n{}\n\n".format(url.strip(), p))
		print("\nSECRET FOUND on page: {}".format(url.strip()))
	get_all_detectors(p)



try:
	file_list = sys.argv[1]
	time_delay = 2
	progress = "#"
	count = [0, 0]
	print("running the command: trufflehog filesystem [list_of_urls] with the time delay of {} seconds\n".format(time_delay))

	#creates an empty results file
	output_results = open("output_results", "w")
	output_results.write("")
	output_results.close()

	#Creates the temporary file holding HTML data retrieved from the URL
	if not os.path.exists("html_data"):
		f = open("html_data", "x")
		f.close()

	#Goes through the list of URLs making the GET request and running trufflehog against the URL
	with open(file_list, "r") as file, open("html_data", "r+") as html_data, open("output_urls", "w") as output_urls, open("output_data", "w") as output_data, open("output_verified_data", "w") as output_verified_data:
		for url in file:

			#does not analyze audio or video or graphics files
			if (".mp4" in url) or (".mp3" in url) or (".jpg" in url) or (".jpeg" in url) or (".svg" in url) or (".png" in url):
				continue

			#makes the request and runs trufflehog
			r = requests.get(url.strip(), timeout=5)

			#skips non 200 response codes
			if r.status_code != 200:
				#creates progress bar of #
				sys.stdout.write('\r')
				sys.stdout.write("{}".format(progress))
				sys.stdout.flush()
				progress += "#"

				time.sleep(time_delay)
				continue
			html_data.write(r.text)
			p = subprocess.check_output(["trufflehog", "filesystem", "html_data"], stderr=subprocess.STDOUT, text=True)

			#checks if any verified or unverified secrets are found
			if ('"unverified_secrets": 0' in p) and ('"verified_secrets": 0' in p):
				pass
			elif 'Found verified result' in p:
				count[0] += 1
				write_to_file(True, url, p)
			else:
				count[1] += 1
				write_to_file(False, url, p)

			#creates progress bar of #
			sys.stdout.write('\r')
			sys.stdout.write("{}".format(progress))
			sys.stdout.flush()
			progress += "#"

			time.sleep(time_delay)

	#Closing files and displaying ending info
	print("\n\nClosing all files")
	file.close()
	html_data.close()
	os.remove("html_data")
	output_urls.close()
	output_data.close()
	output_verified_data.close()
	print("Done. Files saved as output_urls, output_data and output_verified_data. Found {} verified secrets and {} unverified secrets".format(count[0], count[1]))

except Exception as e:
#	print("exception:", e)
	print("format is [file].py [list_of_urls]")
