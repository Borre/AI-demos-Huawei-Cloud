# Huawei Cloud Image Recognition Demo

This is a simple Python application that demonstrates how to use the Huawei Cloud Image Recognition service to analyze images and extract tags and other information.

## Prerequisites

1. Python 3.6 or higher
2. A Huawei Cloud account with Image Recognition service enabled
3. Access credentials (Access Key and Secret Key) for Huawei Cloud

## Setup

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Huawei Cloud credentials:
   Create a `.env` file in the project directory with your credentials:
   ```
   HUAWEI_CLOUD_ACCESS_KEY=your_access_key_here
   HUAWEI_CLOUD_SECRET_KEY=your_secret_key_here
   HUAWEI_CLOUD_REGION=cn-north-4  # Optional, defaults to cn-north-4
   ```

   Alternatively, you can set these as environment variables:
   ```bash
   export HUAWEI_CLOUD_ACCESS_KEY=your_access_key_here
   export HUAWEI_CLOUD_SECRET_KEY=your_secret_key_here
   ```

## Usage

Run the demo with:
```bash
python image_recognition_demo.py
```

By default, the script will download and analyze a sample image. You can also provide your own image path:
```bash
python image_recognition_demo.py path/to/your/image.jpg
```

## Features

- Connects to Huawei Cloud Image Recognition service
- Downloads a sample image if none is provided
- Performs image tagging analysis
- Displays results with confidence scores

## Code Structure

- `image_recognition_demo.py`: Main application code
- `requirements.txt`: Python dependencies
- `.env`: Configuration file (you need to create this)

## API Documentation

For more information about the Huawei Cloud Image Recognition service, see:
https://support.huaweicloud.com/intl/en-us/product-image.html

## Troubleshooting

1. **Authentication errors**: Verify your Access Key and Secret Key are correct
2. **Connection errors**: Check your internet connection and firewall settings
3. **Image format errors**: The service supports JPG, PNG, and BMP formats

## License

This demo is provided as-is without any warranty.