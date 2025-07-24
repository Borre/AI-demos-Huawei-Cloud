#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Create a simple test image with text for OCR testing.
"""

import os

from PIL import Image, ImageDraw, ImageFont


def create_test_image():
    # Create a new image with white background
    width, height = 400, 200
    image = Image.new('RGB', (width, height), color='white')
    
    # Draw some text on the image
    draw = ImageDraw.Draw(image)
    
    # Try to use a basic font, or fallback to default
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
    
    # Add text to the image
    text = "Hello, Huawei Cloud OCR!"
    
    # Handle different Pillow versions for text size calculation
    try:
        # For newer versions of Pillow
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        # For older versions of Pillow
        text_width, text_height = draw.textsize(text, font=font)
    
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, fill='black', font=font)
    
    # Save the image
    image.save('test_image.jpg')
    print("Test image 'test_image.jpg' created successfully!")

if __name__ == "__main__":
    # Check if PIL is installed
    try:
        from PIL import Image, ImageDraw, ImageFont
        create_test_image()
    except ImportError:
        print("Pillow is not installed. Please install it with: pip install Pillow")
        print("Creating a text file instead as a placeholder...")
        
        # Create a text file as a placeholder
        with open('test_image.jpg', 'w') as f:
            f.write("This is a placeholder for an image file. Replace with an actual image for OCR testing.")
        print("Placeholder file 'test_image.jpg' created. Please replace with an actual image file.")