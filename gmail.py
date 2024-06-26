
# Importing required libraries
import os
import base64
from bs4 import BeautifulSoup
import dateutil.parser as parser
import main
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
def get_mail():
	# Creating a storage.JSON file with authentication details
	SCOPES = 'https://www.googleapis.com/auth/gmail.modify' # we are using modify and not readonly, as we will be marking the messages Read
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists("gmail.json"):
		creds = Credentials.from_authorized_user_file("gmail.json", SCOPES)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
			"credential.json", SCOPES
		)
		creds = flow.run_local_server(port=0)
	# Save the credentials for the next run
	with open("gmail.json", "w") as token:
		token.write(creds.to_json())
	GMAIL = build("gmail", "v1", credentials=creds)

	user_id =  'me'
	label_id_one = 'INBOX'
	label_id_two = 'UNREAD'

	# Getting all the unread messages from Inbox
	# labelIds can be changed accordingly
	unread_msgs = GMAIL.users().messages().list(userId='me',labelIds=[label_id_one, label_id_two]).execute()

	# We get a dictonary. Now reading values for the key 'messages'
	mssg_list = unread_msgs['messages']

	print ("Total unread messages in inbox: ", str(len(mssg_list)))
	x = f"Total unread messages in inbox: ", str(len(mssg_list))
	main.speak(f"{x}")

	final_list = []


	for mssg in mssg_list:
		temp_dict = { }
		m_id = mssg['id'] # get id of individual message
		message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute() # fetch the message using API
		payld = message['payload'] # get payload of the message 
		headr = payld['headers'] # get header of the payload


		for one in headr: # getting the Subject
			if one['name'] == 'Subject':
				msg_subject = one['value']
				temp_dict['Subject'] = msg_subject
			else:
				pass


		for two in headr: # getting the date
			if two['name'] == 'Date':
				msg_date = two['value']
				date_parse = (parser.parse(msg_date))
				m_date = (date_parse.date())
				temp_dict['Date'] = str(m_date)
			else:
				pass

		for three in headr: # getting the Sender
			if three['name'] == 'From':
				msg_from = three['value']
				temp_dict['Sender'] = msg_from
			else:
				pass

		temp_dict['Message'] = message['snippet'] # fetching message snippet


		try:
			
			# Fetching message body
			mssg_parts = payld['parts'] # fetching the message parts
			part_one  = mssg_parts[0] # fetching first element of the part 
			part_body = part_one['body'] # fetching body of the message
			part_data = part_body['data'] # fetching data from the body
			clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
			clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
			clean_two = base64.b64decode (bytes(clean_one, 'UTF-8')) # decoding from Base64 to UTF-8
			soup = BeautifulSoup(clean_two , "lxml" )
			mssg_body = soup.body()
			# mssg_body is a readible form of message body
			# depending on the end user's requirements, it can be further cleaned 
			# using regex, beautiful soup, or any other method
			temp_dict['Message_body'] = mssg_body

		except :
			pass

		print (temp_dict)
		main.speak(f"{temp_dict}")
		final_list.append(temp_dict) # This will create a dictonary item in the final list
		
		# This will mark the messagea as read
		GMAIL.users().messages().modify(userId=user_id, id=m_id,body={ 'removeLabelIds': ['UNREAD']}).execute() 
		



	print ("Total messaged retrived: ", str(len(final_list)))

	y = "Total messaged retrived: ", str(len(final_list))
	main.speak(f"{y}")

	'''

	The final_list will have dictionary in the following format:

	{	'Sender': '"email.com" <name@email.com>', 
		'Subject': 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet', 
		'Date': 'yyyy-mm-dd', 
		'Snippet': 'Lorem ipsum dolor sit amet'
		'Message_body': 'Lorem ipsum dolor sit amet'}


	The dictionary can be exported as a .csv or into a databse
	'''

	#exporting the values as .csv
	with open('Gmail.csv', 'w', encoding='utf-8', newline = '') as csvfile: 
		fieldnames = ['Sender','Subject','Date','Snippet','Message_body']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter = ',')
		writer.writeheader()
		for val in final_list:
			writer.writerow(val)
