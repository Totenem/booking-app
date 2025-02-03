# API Documentation

## Overview

This API allows users to manage bookings stored in a Google Sheet. It provides endpoints to create, read, update, and delete bookings, as well as search for specific bookings based on name and date.

## API Endpoints

### 1. Get All Bookings
- **Endpoint**: `GET /bookings`
- **Description**: Retrieves all bookings from the Google Sheet.
- **Response**:
  ```json
  {
      "Total Bookings": <number>,
      "Booking Details": [
          {
              "Booking ID": <id>,
              "Details": {
                  "Timestamp": <timestamp>,
                  "Name": <name>,
                  "Email": <email>,
                  "Phone Number": <phone>,
                  "Date": <date>,
                  "Time": <time>
              }
          },
          ...
      ]
  }
  ```

### 2. Get Specific Booking
- **Endpoint**: `GET /bookings/{index}`
- **Description**: Retrieves a specific booking by its index (1-based).
- **Response**:
  ```json
  {
      "Booking ID": <id>,
      "Details": {
          "Timestamp": <timestamp>,
          "Name": <name>,
          "Email": <email>,
          "Phone Number": <phone>,
          "Date": <date>,
          "Time": <time>
      }
  }
  ```

### 3. Update Booking
- **Endpoint**: `PUT /bookings/{index}`
- **Description**: Updates the details of an existing booking.
- **Request Body**:
  ```json
  {
      "Timestamp": <timestamp>,
      "Name": <name>,
      "Email": <email>,
      "Phone Number": <phone>,
      "Date": <date>,
      "Time": <time>
  }
  ```
- **Response**:
  ```json
  {
      "message": "Booking updated successfully"
  }
  ```

### 4. Delete Booking
- **Endpoint**: `DELETE /bookings/{index}`
- **Description**: Deletes a specific booking by its index.
- **Response**:
  ```json
  {
      "message": "Booking deleted successfully"
  }
  ```

### 5. Search Bookings
- **Endpoint**: `GET /search_bookings`
- **Description**: Searches for bookings based on name and/or date.
- **Query Parameters**:
  - `name`: The name to search for.
  - `date`: The date to search for.
- **Response**:
  ```json
  {
      "Search Results": [
          {
              "Booking ID": <id>,
              "Details": {
                  "Timestamp": <timestamp>,
                  "Name": <name>,
                  "Email": <email>,
                  "Phone Number": <phone>,
                  "Date": <date>,
                  "Time": <time>
              }
          },
          ...
      ]
  }
  ```

## Conclusion

This API provides a simple interface to manage bookings stored in a Google Sheet. For further assistance, refer to the Google Sheets API documentation or the FastAPI documentation.
