import requests
from requests.auth import HTTPBasicAuth


class NewbookApi():
    """
    This class is used to interact with the Newbook API.
    It provides methods to authenticate and test the API.
    """

    # this is the key that will be used for all requests,
    # it has to be setup beforehand
    active_key = ""

    def __init__(self, base_url: str, username: str, password: str, region: str) -> None:
        """
        Initialize the NewbookApi class.
        
        Parameters:
        username (str): The username for the API.
        password (str): The password for the API.
        region (str): The region for the API.
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.region = region

    def get_api_keys(self) -> dict:
        """
        Get the API keys.
        
        Returns:
        dict: The response from the API.
        """
        response = requests.post(
            f"{self.base_url}/rest/api_keys",
            auth=HTTPBasicAuth(self.username, self.password),
            json={"region": self.region}
        )
        # print(response.json())
        return response.json()

    def auth_test(self, api_key: str) -> dict:
        """
        Test the authentication with the API.
        
        Parameters:
        api_key (str): The API key to test.
        
        Returns:
        dict: The response from the API.
        """
        response = requests.post(
            f"{self.base_url}/auth_test",
            auth=HTTPBasicAuth(self.username, self.password),
            json={
                "region": self.region,
                "api_key": api_key
            }
        )
        print(response.json())
        return response.json()
    
    def get_guests_lists (self):
        """
        Get the guests lists.
        
        Returns:
        dict: The response from the API.
        """
        response = requests.post(
            f"{self.base_url}/rest/guests_list",
            auth=HTTPBasicAuth(self.username, self.password),
            json={
                "region": self.region,
                "api_key": self.active_key
            }
        )
        return response
    
    def create_new_guest (self, new_guest):
        """
        Create a new guest.
        
        Returns:
        dict: The response from the API.
        """

        # Include API key and region in the data
        new_guest['api_key'] = self.active_key
        new_guest['region'] = self.region

        # Check if required fields are present
        required_fields = ['firstname', 'lastname', 'contact_phone']
        for field in required_fields:
            if field not in new_guest:
                return {"error": f"Missing required field '{field}' in the request", 'success': False}, 400
   
        response = requests.post(
            f"{self.base_url}/rest/guests_create",
            auth=HTTPBasicAuth(self.username, self.password),
            json=new_guest
        )

        return response.json()
    
    def update_existing_guest (self, updated_guest):
        """
        Update an exisiting guest.
        
        Returns:
        dict: The response from the API.
        """

        # Include API key and region in the data
        updated_guest['api_key'] = self.active_key
        updated_guest['region'] = self.region

        # Check if required fields are present
        required_fields = ['guest_id']
        for field in required_fields:
            if field not in updated_guest:
                return {"error": f"Missing required field '{field}' in the request", 'success': False}, 400
  
        response = requests.post(
            f"{self.base_url}/rest/guests_update",
            auth=HTTPBasicAuth(self.username, self.password),
            json=updated_guest
        )

        return response.json()
    
    def get_sites_list (self):
        """
        Get the sites list.
        
        Returns:
        dict: The response from the API.
        """
        response = requests.post(
            f"{self.base_url}/rest/sites_list",
            auth=HTTPBasicAuth(self.username, self.password),
            json={
                "region": self.region,
                "api_key": self.active_key
            }
        )
        return response
    
    def get_bookings_list (self, booking):
        """
        Get the bookings list.
        
        Returns:
        dict: The response from the API.
        """

        # Include API key and region in the data
        booking['api_key'] = self.active_key
        booking['region'] = self.region

        # Check if required fields are present
        required_fields = ['period_from','period_to', 'list_type']
        for field in required_fields:
            if field not in booking:
                return {"error": f"Missing required field '{field}' in the request", 'success': False}, 400

           
        response = requests.post(
            f"{self.base_url}/rest/bookings_list",
            auth=HTTPBasicAuth(self.username, self.password),
            json=booking
        )

        return response.json()
    

    def create_new_booking (self, new_booking):
        """
        Create a new booking.
        
        Returns:
        dict: The response from the API.
        """

        # Include API key and region in the data
        new_booking['api_key'] = self.active_key
        new_booking['region'] = self.region

        # Check if required fields are present
        required_fields = ["period_from", "period_to", "category_id", "site_id"]
        for field in required_fields:
            if field not in new_booking:
                return {"error": f"Missing required field '{field}' in the request",'success':False}, 400
        
        response = requests.post(
            f"{self.base_url}/rest/bookings_create",
            auth=HTTPBasicAuth(self.username, self.password),
            json=new_booking
        )

        return response.json()
    


    def update_existing_booking (self, existing_booking):
        """
        Update an existing booking.
        
        Returns:
        dict: The response from the API.
        """

        # Include API key and region in the data
        existing_booking['api_key'] = self.active_key
        existing_booking['region'] = self.region

        # Check if required fields are present
        required_fields = ["booking_id"]
        for field in required_fields:
            if field not in existing_booking:
                return {"error": f"Missing required field '{field}' in the request",'success':False}, 400
        
        response = requests.post(
            f"{self.base_url}/rest/bookings_update",
            auth=HTTPBasicAuth(self.username, self.password),
            json=existing_booking
        )

        return response.json()