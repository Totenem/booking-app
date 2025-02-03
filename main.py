import gspread
from google.oauth2.service_account import Credentials
from fastapi import FastAPI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Construct the credentials dictionary
credentials = {
    "type": "service_account",
    "project_id": os.getenv("GOOGLE_PROJECT_ID"),
    "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
    "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("GOOGLE_UNIVERSE_DOMAIN")
}

# Check for missing environment variables
if None in credentials.values():
    raise ValueError("One or more environment variables are missing.")

# Set up Google Sheets API client
scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(credentials, scopes=scope)
client = gspread.authorize(creds)

sheet_id = "1wVYuhapdpez_48j_N-T9UJEZdz--1LINBb5NZ1IBTHo"
sheet = client.open_by_key(sheet_id)

# values_list = sheet.sheet1.row_values(2)
# print(values_list)

app = FastAPI()
bookings = []  

@app.get("/bookings")
def booking():
    global bookings  
    all_rows = sheet.sheet1.get_all_values()  # getting all

    bookings.clear()  # Clear the existing bookings before populating

    for index, row in enumerate(all_rows[1:], start=1):  # Skip header row
        booking = {
            "Booking ID": index,
            "Details": {
                "Timestamp": row[0],
                "Name": row[1],
                "Email": row[2],
                "Phone Number": row[3],
                "Date": row[4],
                "Time": row[5]
            }
        }
        bookings.append(booking)

    return {"Total Bookings": len(bookings),"Booking Details": bookings}

@app.get("/bookings/{index}")
def specific_booking(index: int):
    global bookings  

    # Check if the requested booking index is valid
    if 1 <= index <= len(bookings):
        return bookings[index - 1]  # Return the specific booking
    else:
        return {"error": "Booking ID not found"}, 404

@app.put("/bookings/{index}")
def update_booking(index: int, updated_details: dict):
    # Update the details of an existing booking.
    # Parameters:
    # - index: The index of the booking to update (1-based).
    # - updated_details: A dictionary containing the updated booking details.
    # Returns:
    # - A success message if the booking is updated.
    # - An error message if the booking ID is not found.
    
    global sheet
    # Check if the requested booking index is valid
    if 1 <= index <= len(sheet.sheet1.get_all_values()) - 1:  # Adjust for header row
        # Prepare the row to update (index + 1 for header row)
        row_to_update = index + 1
        # Update the row in the Google Sheet
        # Assuming updated_details is now coming from the request body
        sheet.sheet1.update(f'A{row_to_update}:F{row_to_update}', [list(updated_details.values())])
        return {"message": "Booking updated successfully"}
    else:
        return {"error": "Booking ID not found"}, 404

@app.delete("/bookings/{index}")
def delete_booking(index: int):
    
    # Delete a specific booking by its index.

    # Parameters:
    # - index: The index of the booking to delete (1-based).

    # Returns:
    # - A success message if the booking is deleted.
    # - An error message if the booking ID is not found.
    
    global sheet
    # Check if the requested booking index is valid
    if 1 <= index <= len(sheet.sheet1.get_all_values()) - 1:  # Adjust for header row
        # Prepare the row to delete (index + 1 for header row)
        row_to_delete = index + 1
        # Delete the row in the Google Sheet
        sheet.sheet1.delete_rows(row_to_delete)
        return {"message": "Booking deleted successfully"}
    else:
        return {"error": "Booking ID not found"}, 404

@app.get("/search_bookings")
def search_bookings(name: str = None, date: str = None):
    
    # Search for bookings based on name and/or date.

    # Parameters:
    # - name: The name to search for in the bookings.
    # - date: The date to search for in the bookings.

    # Returns:
    # - A list of bookings that match the search criteria.
    
    global bookings
    results = []
    for booking in bookings:
        if (name and name.lower() in booking["Details"]["Name"].lower()) or \
           (date and date in booking["Details"]["Date"]):
            results.append(booking)
    return {"Search Results": results}

    