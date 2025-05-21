#!/usr/bin/env python3
"""
AstroVista OneSignal Notification Sender

This script sends push notifications through the OneSignal API.
"""

import os
import json
import requests
from dotenv import load_dotenv

def load_credentials():
    """Load OneSignal credentials from .env file"""
    load_dotenv()
    app_id = os.getenv("ASTRO_VISTA_ONESIGNAL_APP_ID")
    api_key = os.getenv("ASTRO_VISTA_ONESIGNAL_API_KEY")
    
    if not app_id or not api_key:
        raise ValueError("OneSignal credentials not found in .env file")
    
    return app_id, api_key

def send_notification(app_id, api_key, name=None, heading="AstroVista Notification", 
                     message=None, url=None, segment="All", big_picture=None, show_rate_button=False, data=None):
    """
    Send a push notification through OneSignal API
    
    Args:
        app_id (str): OneSignal App ID
        api_key (str): OneSignal REST API Key
        name (str, optional): Name of the notification for tracking purposes. Defaults to None.
        heading (str, optional): Notification title. Defaults to "AstroVista Notification".
        message (str): Notification message content
        url (str, optional): URL to open when notification is clicked. Defaults to None.
        segment (str, optional): Target audience segment. Defaults to "All".
        big_picture (str, optional): URL of the image to display in the notification. Defaults to None.
        show_rate_button (bool, optional): Whether to show a Rate button. Defaults to False.
        data (dict, optional): Additional data to include. Defaults to None.
    
    Returns:
        dict: API response
    """
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "app_id": app_id,
        "contents": {"en": message},
        "headings": {"en": heading},
        "included_segments": [segment],
        # Target only Android devices
        "isAndroid": True,
        "isIos": False,
        "isAnyWeb": False,
        "isHuawei": False,
        "isAdm": False,
        "isChrome": False,
        "isFirefox": False,
        "isSafari": False,
        "isWP_WNS": False
    }
    
    # Add Rate button if enabled
    if show_rate_button:
        payload["buttons"] = [
            {"id": "rate", "text": "Rate"}
        ]
    
    # Add optional parameters if provided
    if url:
        payload["url"] = url
    
    if data:
        payload["data"] = data
        
    if big_picture:
        # Add big picture for Android only
        payload["big_picture"] = big_picture
    
    if name:
        payload["name"] = name
    
    response = requests.post(
        "https://onesignal.com/api/v1/notifications",
        headers=headers,
        json=payload
    )
    
    return response.json()

def save_config_to_json(config, json_file_path="astro_vista_onesignal.json"):
    """
    Save notification configuration to a JSON file with UTF-8 encoding
    
    Args:
        config (dict): Configuration parameters
        json_file_path (str): Path to the JSON configuration file
    """
    try:
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=2, ensure_ascii=False)
        print(f"Configuration saved to {json_file_path}")
    except Exception as e:
        raise ValueError(f"Failed to save configuration to {json_file_path}: {e}")

def load_config_from_json(json_file_path="astro_vista_onesignal.json"):
    """
    Load notification configuration from a JSON file
    
    Args:
        json_file_path (str): Path to the JSON configuration file
        
    Returns:
        dict: Configuration parameters
    """
    try:
        # Explicitly use UTF-8 encoding to handle emoji and special characters
        with open(json_file_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        
        # Validate required fields
        required_fields = ['name', 'heading', 'message', 'url', 'segment', 'big_picture', 'show_rate_button']
        missing_fields = [field for field in required_fields if field not in config]
        
        if missing_fields:
            raise ValueError(f"Missing required fields in JSON configuration: {', '.join(missing_fields)}")
            
        if not config['message']:
            raise ValueError("Message field cannot be empty in the JSON configuration")
            
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {json_file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in configuration file: {json_file_path}")
    except UnicodeDecodeError as e:
        raise ValueError(f"Character encoding error in configuration file: {e}. Please ensure the file is saved with UTF-8 encoding.")

def main():
    """Main function to send a notification"""
    try:
        app_id, api_key = load_credentials()
        
        print("\n=== AstroVista OneSignal Notification Sender ===")
        print("Loading configuration from JSON file...")
        
        # Load configuration from JSON file
        config = load_config_from_json()
        
        # Extract parameters from config
        name = config.get('name')
        heading = config.get('heading')
        message = config['message']
        url = config.get('url')
        segment = config.get('segment')
        big_picture = config.get('big_picture')
        show_rate_button = config.get('show_rate_button')
        
        print(f"Notification Name: {name}")
        print(f"Notification Title: {heading}")
        print(f"Message: {message}")
        print(f"URL: {url if url else 'None'}")
        print(f"Segment: {segment}")
        print(f"Image URL: {big_picture}")
        print(f"Show Rate Button: {show_rate_button}")
        
        # Send the notification
        print("\nSending notification...")
        response = send_notification(
            app_id=app_id,
            api_key=api_key,
            name=name,
            heading=heading,
            message=message,
            url=url,
            segment=segment,
            big_picture=big_picture,
            show_rate_button=show_rate_button
        )
        
        # Display the response
        print("\nAPI Response:")
        print(json.dumps(response, indent=2))
        
        if response.get("id"):
            print(f"\nSuccess! Notification sent with ID: {response['id']}")
        else:
            print(f"\nFailed to send notification. Error: {response.get('errors', ['Unknown error'])}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()