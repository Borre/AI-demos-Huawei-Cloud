"""
Huawei Cloud Image Recognition Demo

This script demonstrates how to use Huawei Cloud's Image Recognition service
to analyze images and extract information like tags, categories, and other
image attributes.

Requirements:
- Python 3.6+
- Huawei Cloud account with Image Recognition service enabled
- Access credentials (AK/SK) for Huawei Cloud
"""

import os
import sys
from dotenv import load_dotenv
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkimage.v2 import ImageClient
from huaweicloudsdkimage.v2.region.image_region import ImageRegion
import requests


def load_config():
    """Load configuration from environment variables or .env file"""
    load_dotenv()
    
    # Load credentials from environment variables
    ak = os.getenv('HUAWEI_CLOUD_ACCESS_KEY')
    sk = os.getenv('HUAWEI_CLOUD_SECRET_KEY')
    region = os.getenv('HUAWEI_CLOUD_REGION', 'cn-north-4')
    
    if not ak or not sk:
        print("Error: Please set HUAWEI_CLOUD_ACCESS_KEY and HUAWEI_CLOUD_SECRET_KEY environment variables")
        print("You can also create a .env file with these variables:")
        print("HUAWEI_CLOUD_ACCESS_KEY=your_access_key")
        print("HUAWEI_CLOUD_SECRET_KEY=your_secret_key")
        sys.exit(1)
    
    return ak, sk, region


def create_image_client(ak, sk, region):
    """
    Create and return an ImageClient instance for Huawei Cloud Image Recognition service
    
    Args:
        ak (str): Access Key
        sk (str): Secret Key
        region (str): Huawei Cloud region
    
    Returns:
        ImageClient: Configured client for Image Recognition service
    """
    credentials = BasicCredentials(ak, sk)
    # Updated to use the correct method for specifying region in newer SDK versions
    region_obj = ImageRegion.value_of(region)
    client = ImageClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(region_obj) \
        .build()
    return client


def download_image(image_url, local_path):
    """
    Download an image from a URL to a local file
    
    Args:
        image_url (str): URL of the image to download
        local_path (str): Local path to save the image
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        with open(local_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False


def recognize_image(client, image_path):
    """
    Perform image recognition on a local image file
    
    Args:
        client (ImageClient): Huawei Cloud Image Recognition client
        image_path (str): Path to the image file
    
    Returns:
        dict: Recognition results or None if error
    """
    try:
        # For demo purposes, we'll use the tag recognition API
        # You can extend this to use other APIs like scene detection, etc.
        from huaweicloudsdkimage.v2.model import RunImageTaggingRequest
        from huaweicloudsdkimage.v2.model import ImageTaggingReq
        import base64
        
        # Read and encode the image as base64
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Create the request with the base64 encoded image
        # Set language to 'en' for English results
        request_body = ImageTaggingReq(image=image_data, language='en')
        request = RunImageTaggingRequest(body=request_body)
        
        response = client.run_image_tagging(request)
        return response.to_dict()
    
    except exceptions.ClientRequestException as e:
        print(f"Client request error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def print_results(results):
    """
    Print the image recognition results in a formatted way
    
    Args:
        results (dict): Results from the image recognition API
    """
    if not results:
        print("No results to display")
        return
    
    print("\n=== Image Recognition Results ===")
    
    if 'result' in results and 'tags' in results['result']:
        tags = results['result']['tags']
        print(f"\nFound {len(tags)} tags:")
        for tag in tags:
            tag_name = tag.get('tag', 'Unknown')
            confidence = float(tag.get('confidence', 0))
            # Normalize confidence if it seems to be in a different scale
            if confidence > 100:
                confidence = confidence / 100
            print(f"  - {tag_name}: {confidence:.2f}% confidence")
    else:
        print("No tags found in results")


def main():
    """
    Main function to run the image recognition demo
    """
    print("Huawei Cloud Image Recognition Demo")
    print("=" * 40)
    
    # Load configuration
    ak, sk, region = load_config()
    
    # Create client
    try:
        client = create_image_client(ak, sk, region)
        print(f"Successfully connected to Huawei Cloud Image Recognition service in region {region}")
    except Exception as e:
        print(f"Error creating client: {e}")
        sys.exit(1)
    
    # Get image path from command line or use default
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Default image for demo
        image_path = "sample.jpg"
        print(f"\nNo image specified. Using default: {image_path}")
        print("Downloading sample image for demo...")
        
        # Download a sample image if it doesn't exist
        if not os.path.exists(image_path):
            sample_url = "https://images.unsplash.com/photo-1500462918059-b1a0cb512f1d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80"
            if not download_image(sample_url, image_path):
                print("Failed to download sample image. Please provide your own image.")
                sys.exit(1)
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found")
        sys.exit(1)
    
    print(f"\nAnalyzing image: {image_path}")
    
    # Perform image recognition
    results = recognize_image(client, image_path)
    
    # Print results
    print_results(results)
    
    print("\nDemo completed!")


if __name__ == "__main__":
    main()