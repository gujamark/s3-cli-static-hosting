import json
from botocore.exceptions import ClientError
import logging

def set_static_hosting_permissions(aws_s3_client, bucket_name):
    try:
        # Uncheck "Block All Public Acess"
        response = aws_s3_client.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
            }
        )

        response = aws_s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicReadGetObject",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": [
                            "s3:GetObject"
                        ],
                        "Resource": [
                            f"arn:aws:s3:::{bucket_name}/*"
                        ]
                    }
                ]
            })
        )
    except ClientError as e:
        logging.error(e)