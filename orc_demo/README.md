# Huawei Cloud OCR Demo

This is a simple Python script demonstrating how to use Huawei Cloud OCR service to extract text from images.

## Prerequisites

1. Python 3.6 or later
2. A Huawei Cloud account with OCR service enabled
3. Access Key (AK) and Secret Key (SK) for authentication
4. An image file for OCR testing

## Setup

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Huawei Cloud credentials using one of these methods:

   **Method 1: Environment variables**
   ```bash
   export HUAWEICLOUD_SDK_AK="your_access_key"
   export HUAWEICLOUD_SDK_SK="your_secret_key"
   export HUAWEICLOUD_SDK_REGION="AP_SOUTHEAST_1"  # Optional, defaults to AP_SOUTHEAST_1
   ```

   **Method 2: Using the .env file**
   Copy the `.env.example` file to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

## Usage

### Method 1: Using the Python script directly
```bash
python ocr_demo.py path/to/your/image.jpg
```

### Method 2: Using the run script
```bash
./run_ocr.sh path/to/your/image.jpg
```

## Code Structure

- `ocr_demo.py`: Main script demonstrating OCR functionality
- `run_ocr.sh`: Bash script for easier execution with validation
- `create_test_image.py`: Script to create a test image
- `requirements.txt`: Required Python packages
- `README.md`: This file
- `.env.example`: Template for environment variables

## Configuration

The script uses the following environment variables:

- `HUAWEICLOUD_SDK_AK`: Your Access Key (required)
- `HUAWEICLOUD_SDK_SK`: Your Secret Key (required)
- `HUAWEICLOUD_SDK_REGION`: Region for the OCR service (optional, defaults to AP_SOUTHEAST_1)

Available regions:
- `AP_SOUTHEAST_1`: Asia Pacific (Hong Kong)
- `AP_SOUTHEAST_2`: Asia Pacific (Singapore)
- `AP_SOUTHEAST_3`: Asia Pacific (Sydney)

## Huawei Cloud OCR Documentation

For more information about Huawei Cloud OCR service, visit:
https://www.huaweicloud.com/product/ocr.html

## Troubleshooting

1. **Authentication Error**: Make sure your AK/SK are correct and have appropriate permissions for OCR service.
2. **Region Error**: Ensure the region in the code matches your Huawei Cloud account region.
3. **Image Format Error**: Supported formats include JPG, PNG, and BMP.

## License

This demo is provided as-is without any warranty. Use at your own risk.