# S3 Bucket CLI Program

This is a command-line interface (CLI) program that helps with Amazon S3 buckets. It allows users to host static web pages on an S3 bucket and set the required website policies and permissions.

## Getting Started

Prerequisites
To use this program, you need to have Python installed on your computer. You also need to have an AWS account and have the necessary credentials set up on your machine.

## Installing

- Clone the repository.
- Install the required dependencies by running `pip3 install -r requirements.txt` or `poetry install`
- Rename .env.example file to .env and add your AWS credentials.

## Examples

### Host a static website

Without poetry:
```
python3 main.py host BUCKET_NAME -s /path/to/my/static/website
```

With poetry:
```
poetry run python main.py host BUCKET_NAME -s /path/to/my/static/website
```

### Arguments:

- bucket_name: Name of the S3 bucket where you want to host your static web page.
- -s or --source: Path to the directory containing your static web page files.
