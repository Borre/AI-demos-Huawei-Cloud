#!/bin/bash

# Enhanced OCR script for Huawei Cloud OCR

echo "Huawei Cloud OCR Demo"
echo "====================="

# Check if required environment variables are set
if [[ -z "$HUAWEICLOUD_SDK_AK" || -z "$HUAWEICLOUD_SDK_SK" ]]; then
    # Try to load from .env file
    if [[ -f ".env" ]]; then
        source .env
    fi
    
    # Check again after sourcing .env
    if [[ -z "$HUAWEICLOUD_SDK_AK" || -z "$HUAWEICLOUD_SDK_SK" ]]; then
        echo "Error: Please set HUAWEICLOUD_SDK_AK and HUAWEICLOUD_SDK_SK environment variables"
        echo "Example:"
        echo "  export HUAWEICLOUD_SDK_AK=your_access_key"
        echo "  export HUAWEICLOUD_SDK_SK=your_secret_key"
        echo ""
        echo "Alternatively, copy .env.example to .env and fill in your credentials"
        exit 1
    fi
fi

# Check if image file is provided
if [[ -z "$1" ]]; then
    echo "Usage: $0 <image_path>"
    echo "Example: $0 test_image.jpg"
    exit 1
fi

# Check if image file exists
if [[ ! -f "$1" ]]; then
    echo "Error: Image file $1 not found"
    exit 1
fi

# Get region or use default
REGION=${HUAWEICLOUD_SDK_REGION:-AP_SOUTHEAST_1}

# Show project ID if set
if [[ -n "$HUAWEICLOUD_SDK_PROJECT_ID" ]]; then
    echo "Using project ID: $HUAWEICLOUD_SDK_PROJECT_ID"
fi

echo "Performing OCR on image: $1"
echo "Using region: $REGION"
python ocr_demo.py "$1"