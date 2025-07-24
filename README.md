# AI Demos for Huawei Cloud LATAM AI Training

This repository contains AI demo applications developed for the Huawei Cloud LATAM AI training program. These demos showcase various AI services available on the Huawei Cloud platform.

## Repository Maintainer

Eduardo Hernandez Cansino

## Demos Included

1. **DeepSeek SQL Demo** - A natural language to SQL converter using the DeepSeek API
2. **Image Recognition Demo** - Uses Huawei Cloud's Image Recognition service to analyze images
3. **OCR Demo** - Optical Character Recognition using Huawei Cloud's OCR service

## Prerequisites

1. Python 3.6 or higher
2. A Huawei Cloud account with the respective services enabled
3. Access credentials (Access Key and Secret Key) for Huawei Cloud services
4. For the DeepSeek SQL demo, you'll also need a DeepSeek API key and a MySQL database

## Setup

### Credentials Configuration

All demos require specific credentials to function. To simplify setup, we've consolidated all required credentials into a single `.env` file in the root directory.

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and fill in your credentials for each demo:
   ```bash
   # Edit with your preferred text editor
   nano .env
   ```

The `.env` file contains sections for each demo with explanations of what credentials are needed.

### Installing Dependencies

Each demo has its own `requirements.txt` file. Install the dependencies for each demo you want to run:

```bash
# For DeepSeek SQL demo
pip install -r deepseek-sql/requirements.txt

# For Image Recognition demo
pip install -r image_recognition_demo/requirements.txt

# For OCR demo
pip install -r orc_demo/requirements.txt
```

## Running the Demos

Navigate to each demo directory and run the respective Python script:

### DeepSeek SQL Demo
```bash
cd deepseek-sql
python demo.py
```

### Image Recognition Demo
```bash
cd image_recognition_demo
python image_recognition_demo.py
```

### OCR Demo
```bash
cd orc_demo
python ocr_demo.py test_image.jpg
```

## Repository Structure

```
.
├── deepseek-sql/           # Natural language to SQL converter demo
├── image_recognition_demo/ # Image recognition service demo
├── orc_demo/               # Optical character recognition demo
├── .env.example            # Template for credentials (copy to .env)
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## Security Note

Never commit your `.env` file to version control as it contains sensitive credentials. The `.gitignore` file in this repository is configured to exclude all `.env` files.

## License

These demos are provided as-is for educational purposes. Use at your own risk.