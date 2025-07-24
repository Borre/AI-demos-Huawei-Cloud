#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Huawei Cloud OCR Demo Script

This script demonstrates how to use Huawei Cloud OCR service to extract text from images.
Before running this script, make sure to:
1. Install the required packages: pip install -r requirements.txt
2. Set up your Huawei Cloud credentials (AK/SK) as environment variables:
   - HUAWEICLOUD_SDK_AK: Your Access Key
   - HUAWEICLOUD_SDK_SK: Your Secret Key
3. Update the region and project_id according to your Huawei Cloud account settings

For more information about Huawei Cloud OCR service, visit:
https://www.huaweicloud.com/product/ocr.html
"""

import os
import sys
from typing import Optional

# Load environment variables from .env file if it exists
if os.path.exists('.env'):
    from dotenv import load_dotenv
    load_dotenv()

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkocr.v1 import OcrClient
from huaweicloudsdkocr.v1.model import *
from huaweicloudsdkocr.v1.region.ocr_region import OcrRegion


def init_ocr_client() -> Optional[OcrClient]:
    """
    Initialize the OCR client with credentials.
    
    Returns:
        OcrClient: Initialized OCR client or None if initialization fails.
    """
    # Get credentials from environment variables
    ak = os.getenv('HUAWEICLOUD_SDK_AK')
    sk = os.getenv('HUAWEICLOUD_SDK_SK')
    region = os.getenv('HUAWEICLOUD_SDK_REGION', 'AP_SOUTHEAST_1')
    project_id = os.getenv('HUAWEICLOUD_SDK_PROJECT_ID')  # Optional project ID
    
    if not ak or not sk:
        print("Error: Please set HUAWEICLOUD_SDK_AK and HUAWEICLOUD_SDK_SK environment variables")
        return None
    
    # Configure credentials
    credentials = BasicCredentials(ak, sk)
    if project_id:
        credentials = BasicCredentials(ak, sk, project_id)
    
    # Initialize OCR client
    # You may need to change the region according to your Huawei Cloud account settings
    # For Hong Kong, consider using AP_SOUTHEAST_1, AP_SOUTHEAST_2, or AP_SOUTHEAST_3
    # Convert region string to proper format
    region = region.upper().replace('-', '_')
    try:
        ocr_region = getattr(OcrRegion, region)
    except AttributeError:
        print(f"Warning: Invalid region '{region}', using AP_SOUTHEAST_1 as default")
        ocr_region = OcrRegion.AP_SOUTHEAST_1
    
    client_builder = OcrClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(ocr_region)
    
    client = client_builder.build()
    
    return client


def recognize_text_from_image(client: OcrClient, image_path: str) -> Optional[GeneralTextResult]:
    """
    Recognize text from an image using Huawei Cloud OCR.
    
    Args:
        client (OcrClient): Initialized OCR client
        image_path (str): Path to the image file
        
    Returns:
        GeneralTextResult: OCR result or None if recognition fails
    """
    try:
        # Check if image file exists
        if not os.path.exists(image_path):
            print(f"Error: Image file {image_path} not found")
            return None
            
        # Read image file as binary
        with open(image_path, 'rb') as f:
            image_data = f.read()
            
        # Encode image data as base64
        import base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        # Create request
        request = RecognizeGeneralTextRequest()
        request.body = GeneralTextRequestBody(image=image_base64)
        
        # Call OCR API
        response = client.recognize_general_text(request)
        
        return response.result
        
    except exceptions.ClientRequestException as e:
        print(f"Client request error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def print_ocr_result(result: GeneralTextResult):
    """
    Print OCR result in a formatted way.
    
    Args:
        result (GeneralTextResult): OCR result to print
    """
    if not result:
        print("No OCR result to display")
        return
        
    print("OCR Result:")
    print("-" * 50)
    print(f"Direction: {result.direction}")
    print(f"Words Block Count: {result.words_block_count}")
    print("\nRecognized Text:")
    
    if result.words_block_list:
        for i, word_block in enumerate(result.words_block_list, 1):
            print(f"{i}. {word_block.words} (Confidence: {word_block.confidence:.4f})")
    else:
        print("No text recognized in the image")


def main():
    """Main function to run the OCR demo."""
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python ocr_demo.py <image_path>")
        print("Example: python ocr_demo.py sample.jpg")
        sys.exit(1)
        
    image_path = sys.argv[1]
    
    # Initialize OCR client
    client = init_ocr_client()
    if not client:
        sys.exit(1)
        
    # Perform OCR
    print(f"Performing OCR on image: {image_path}")
    result = recognize_text_from_image(client, image_path)
    
    # Print result
    print_ocr_result(result)


if __name__ == "__main__":
    main()