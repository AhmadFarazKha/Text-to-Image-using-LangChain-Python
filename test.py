import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

def generate_image(prompt: str):
    """
    Generate an image from text prompt using Eden AI
    """
    headers = {
        "Authorization": f"Bearer {os.getenv('EDENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "providers": "stabilityai",
        "text": prompt,
        "resolution": "512x512",
        "num_images": 1
    }
    
    response = requests.post(
        "https://api.edenai.run/v2/image/generation",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['stabilityai']['items'][0]['image_resource_url']
    return None

def display_and_save_image(url: str, filename: str):
    """
    Display the image and save it
    """
    # Download the image
    response = requests.get(url)
    if response.status_code == 200:
        # Create image from downloaded data
        image = Image.open(BytesIO(response.content))
        
        # Display the image
        image.show()
        
        # Save the image
        image.save(filename)
        return True
    return False

# Create images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Get prompt and generate image
prompt = input("Enter your image description: ")
print("Generating image...")

image_url = generate_image(prompt)
if image_url:
    filename = f"images/generated_image.png"
    display_and_save_image(image_url, filename)
    print(f"Image saved as: {filename}")