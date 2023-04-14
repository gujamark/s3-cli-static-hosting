from botocore.exceptions import ClientError
from pathlib import Path
import magic

def static_web_page_file(aws_s3_client, bucket_name, filename):

    #Check if bucket exists
    try:
        response = aws_s3_client.head_bucket(Bucket=bucket_name)
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code == 200:
            bucket_location = aws_s3_client.get_bucket_location(Bucket=bucket_name)["LocationConstraint"]
            bucket_location = "us-east-1" if bucket_location == None else bucket_location # if bucket location is None/null, it means bucket is located in us-east-2
    except ClientError:
        print("Bucket doesn't exist")
        return False

    root = Path(f'{filename}').expanduser().resolve()

    def __handle_directory(file_folder):
        if file_folder.is_file():
            __upload_static_web_files(aws_s3_client, bucket_name, file_folder, filename)
            return
            
        for each_path in file_folder.iterdir():
            if each_path.is_dir():
                __handle_directory(each_path)
            if each_path.is_file():
                __upload_static_web_files(aws_s3_client, bucket_name, each_path, str(each_path.relative_to(root)))

    __handle_directory(root)

    # public URL
    return "http://{0}.s3-website-{1}.amazonaws.com".format(
        bucket_name,
        bucket_location
    )

def __upload_static_web_files(aws_s3_client, bucket_name, file_path, filename):
    uploaded = {}

    mime_type = magic.from_file(file_path, mime=True)

    allowed_types = {
        ".html": "text/html",
        ".css": "text/plain",
        ".svg" : 'image/svg+xml',
        ".png" : "image/png"
    }

    content_type = mime_type if mime_type in allowed_types.values() else None

    if ".css" == file_path.suffix:
        content_type = "text/css"

    if content_type:
        aws_s3_client.upload_file(
            file_path,
            bucket_name,
            filename,
            ExtraArgs={'ContentType': content_type}
        )
        uploaded[file_path] = filename
        print(content_type, mime_type)


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-static-web-host.html
def set_bucket_website_policy(aws_s3_client, bucket_name, switch):
    website_configuration = {
        # 'ErrorDocument': {'Key': 'error.html'},
        "IndexDocument": {"Suffix": "index.html"},
    }

    response = None

    if switch:
        response = aws_s3_client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration=website_configuration)
    else:
        response = aws_s3_client.delete_bucket_website(Bucket=bucket_name)

    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if status_code == 200:
        return True
    return False
