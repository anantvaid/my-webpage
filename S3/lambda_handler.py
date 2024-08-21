import boto3
import requests
import json
import os

def lambda_handler(event, context):
    # Lambda Handler for updating S3 bucket policy.
    try: 
        response = requests.get("https://api.cloudflare.com/client/v4/ips")
        json_val = response.json()

        BUCKET = os.environ["BUCKET_NAME"]
        result = json_val["result"]
        ipv4_list = result["ipv4_cidrs"]
        ipv6_list = result["ipv6_cidrs"]
        ip_list = [*ipv4_list, *ipv6_list]

        s3_bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{BUCKET}/*",
                    "Condition": {
                        "IpAddress": {
                            "aws:SourceIp": 
                                ip_list
                        }
                    }
                }
            ]
        }

        s3_bucket_policy = json.dumps(s3_bucket_policy)
        
        client = boto3.client('s3')

        response = client.put_bucket_policy(
            Bucket = BUCKET,
            Policy = s3_bucket_policy,
        )

        return {
            'statusCode': 200,
            'body': json.dumps('S3 bucket policy updated successfully')
        }
        
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error updating S3 bucket policy')
        }