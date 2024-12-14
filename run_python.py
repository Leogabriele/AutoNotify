import gspread
from twilio.rest import Client
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('file.json', scope)  # Adjust the path to your JSON file
client_gs = gspread.authorize(creds)

# Open the Google Sheet using its URL
spreadsheet = client_gs.open_by_url("https://docs.google.com/spreadsheets/################################")
sheet = spreadsheet.sheet1  # Accessing the first sheet

# Twilio setup
account_sid = 'AC577#######################'
auth_token = '3c712########################'
client = Client(account_sid, auth_token)

# Check dates
tomorrow = datetime.now() + timedelta(days=1)

# Your WhatsApp number (where all messages will be sent)
my_whatsapp_number = "whatsapp:+1########"  # Your personal number to receive messages

# Iterate over rows in the Google Sheet
for row in sheet.get_all_values()[1:]:  # Skipping the header row
    user_id, name, expiry_date_str = row  # Extracting the columns: user_id, name, and expiry_date
    try:
        # Convert expiry_date string to datetime
        expiry_date = datetime.strptime(expiry_date_str, '%d-%b,%y').date()  # Ensure correct date format
        if expiry_date == tomorrow.date():
            # Twilio WhatsApp message setup
            message = client.messages.create(
                body=f"Reminder: User ID: {user_id} - {name}'s package is expiring tomorrow ({expiry_date}).",
                from_='whatsapp:+14155238886',  # Twilio Sandbox WhatsApp number
                to=my_whatsapp_number  # Always send to your WhatsApp number
            )
            print(f"Message sent: Reminder for {name} with User ID {user_id}")
    except Exception as e:
        print(f"Error processing row {row}: {e}")
