from pytube import YouTube

import boto3
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# import list
import csv
import os
from decouple import config

s3 = boto3.client('s3')
bucket_name = config('BUCKET_NAME')


def backup(input_file, start_id):
	current_link = 0

	with open(input_file, newline='') as f:
		reader = csv.reader(f)
		data = list(reader)

	total_link = len(data)

	for link in data[start_id:]:
		print(link)
		current_link += 1
		try:
			yt = YouTube(link[0])
			#Title of video
			print("Title:", yt.title)
			#Number of views of video
			print(yt.streams.filter(progressive=True))
			ys = yt.streams.get_highest_resolution()
			ys = yt.streams.get_by_itag('22')

			yt_title = yt.title
			filename = ''.join(e for e in yt_title if e.isalnum())
			print("Downloading...[{}/{}]".format(current_link, total_link))
			try:
				print(filename)
				ys.download(filename = filename)

				print("Download completed!!")

				filename += '.mp4'
				s3.upload_file(filename, bucket_name, filename)

				if os.path.exists(filename):
					os.remove(filename)
				else:
					print("The file does not exist")

			except:
				print('Failed to download, continue')
				with open('fail_to_backup.csv', newline='') as f:
					reader = csv.reader(f)
					data = list(reader)
		except:
				print('File deleted, continue')
				with open('suspected_deleted.csv', newline='') as f:
					reader = csv.reader(f)
					data = list(reader)

backup('url.csv', 0)


