import os
from dotenv import load_dotenv
from models import UserProfile

# Load environment variables from the .env file
load_dotenv()

class UserManager:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Client ID or Client Secret is missing in the environment variables.")
        
        # Initialize with a default user profile
        self.user_profile = UserProfile(id="1", name="John Doe", email="john@example.com", phone="123456789", address="123 Main St")

    def get_user_profile(self):
        return self.user_profile

    def update_user_profile(self, profile: UserProfile):
        self.user_profile = profile
        return self.user_profile
    
    # Example method that could use client_id and client_secret
    def authenticate_user(self, auth_code):
        # Use self.client_id and self.client_secret to interact with an OAuth2 provider (e.g., Google)
        pass
