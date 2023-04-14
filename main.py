import logging
from botocore.exceptions import ClientError
from auth import init_client
import argparse
from static_hosting.host import static_web_page_file, set_bucket_website_policy
from static_hosting.permissions import set_static_hosting_permissions

parser = argparse.ArgumentParser(
  description="CLI program that helps with S3 buckets.",
  prog='main.py',
  epilog='DEMO APP FOR BTU_AWS')

subparsers = parser.add_subparsers(dest="command")
host_subparser = subparsers.add_parser("host")

host_subparser.add_argument("bucket_name",type=str,help="Bucket")
host_subparser.add_argument("-s","--source",type=str, required=True)

def main():
  s3_client = init_client()
  args = parser.parse_args()

  if args.command == "host":
    set_bucket_website_policy(s3_client,args.bucket_name,True)
    set_static_hosting_permissions(s3_client, args.bucket_name)
    print(static_web_page_file(s3_client,args.bucket_name,args.source))

if __name__ == "__main__":
  try:
    main()
  except ClientError as e:
    logging.error(e)