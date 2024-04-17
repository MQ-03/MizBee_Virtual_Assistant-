from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import platform
import icalendar
import subprocess
import datetime
import os.path
import main

# Replace 'your_calendar.ics' with the path to your actual iCalendar file
ical_file_path = '/path/Calendar.ics'

def open_spotify():
    system_platform = platform.system().lower()

    if system_platform == "darwin":  # macOS
        try:
            subprocess.run(["open", "-a", "Spotify"])
            print("MizBee: Spotify is opening...")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Unsupported operating system. This function is designed for macOS.")

def open_photos():
    system_platform = platform.system().lower()

    if system_platform == "darwin":  # macOS
        try:
            subprocess.run(["open", "-a", "Photos"])
            print("MizBee: Photos is opening...")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Unsupported operating system. This function is designed for macOS.")

def open_safari():
    system_platform = platform.system().lower()

    if system_platform == "darwin":  # macOS
        try:
            subprocess.run(["open", "-a", "Safari"])
            print("MizBee: Safari is opening...")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Unsupported operating system. This function is designed for macOS.")

def open_chrome():
    system_platform = platform.system().lower()

    if system_platform == "darwin":  # macOS
        try:
            subprocess.run(["open", "-a", "Google Chrome"])
            print("MizBee: Google Chrome is opening...")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Unsupported operating system. This function is designed for macOS.")

def open_settings():
    system_platform = platform.system().lower()

    if system_platform == "darwin":  # macOS
        try:
            subprocess.run(["open", "-a", "System Settings"])
            print("MizBee: System Settings is opening...")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Unsupported operating system. This function is designed for macOS.")
#open whatsapp app in macOS
def open_whatsapp():
    system_platform = platform.system().lower()

    if system_platform == "darwin":  # macOS
        try:
            subprocess.run(["open", "-a", "WhatsApp"])
            print("MizBee: WhatsApp is opening...")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Unsupported operating system. This function is designed for macOS.")

def open_terminal():
    system_platform = platform.system().lower()

    if system_platform == "darwin":  # macOS
        try:
            subprocess.run(["open", "-a", "Terminal"])
            print("MizBee: Terminal is opening...")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Unsupported operating system. This function is designed for macOS.")

def display_calendar_events(ical_file_path):
    with open(ical_file_path, 'rb') as f:
        cal_data = f.read()

    cal = icalendar.Calendar.from_ical(cal_data)

    for event in cal.walk('vevent'):
        summary = event.get('summary')
        start_time = event.get('dtstart').dt
        end_time = event.get('dtend').dt

        print(f"Event: {summary}")
        main.speak(f"Event: {summary}")
        print(f"Start Time: {start_time}")
        main.speak(f"Start Time: {start_time}")
        print(f"End Time: {end_time}")
        main.speak(f"End Time: {end_time}")

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

date_time = datetime.datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")

def cal_events():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  try:
    service = build("calendar", "v3", credentials=creds)
    
    # Call the Calendar API
    now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])
      x = f'{start, event["summary"]}'
      main.speak(x)


  except HttpError as error:
    print(f"An error occurred: {error}")
