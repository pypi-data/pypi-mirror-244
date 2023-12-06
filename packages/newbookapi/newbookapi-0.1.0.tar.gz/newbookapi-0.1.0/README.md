# Py-Newbook API Interaction

This project is about interacting with the Newbook API. It provides methods to authenticate, test the API, manage guests, sites and bookings.

## Class: NewbookApi

This class is used to interact with the Newbook API.

### Methods

#### __init__(self, base_url: str,username: str, password: str , region: str) -> None

Initialize the NewbookApi class.

Parameters:
- username (str): The username for the API.
- password (str): The password for the API.
- region (str): The region for the API.

#### get_api_keys(self) -> dict

Get the API keys.

Returns:
- dict: The response from the API.

#### auth_test(self, api_key: str) -> dict

Test the authentication with the API.

Parameters:
- api_key (str): The API key to test.

Returns:
- dict: The response from the API.

#### get_guests_lists(self) -> dict

Get the guests lists.

Returns:
- dict: The response from the API.

#### create_new_guest(self, new_guest) -> dict

Create a new guest.

Parameters:
- new_guest (dict): The new guest details.

Returns:
- dict: The response from the API.

#### update_existing_guest(self, updated_guest) -> dict

Update an existing guest.

Parameters:
- updated_guest (dict): The updated guest details.

Returns:
- dict: The response from the API.

#### get_sites_list(self) -> dict

Get the sites list.

Returns:
- dict: The response from the API.

#### get_bookings_list(self, booking) -> dict

Get the bookings list.

Parameters:
- booking (dict): The booking details.

Returns:
- dict: The response from the API.

#### create_new_booking(self, new_booking) -> dict

Create a new booking.

Parameters:
- new_booking (dict): The new booking details.

Returns:
- dict: The response from the API.

#### update_existing_booking(self, existing_booking) -> dict

Update an existing booking.

Parameters:
- existing_booking (dict): The existing booking details.

Returns:
- dict: The response from the API.
