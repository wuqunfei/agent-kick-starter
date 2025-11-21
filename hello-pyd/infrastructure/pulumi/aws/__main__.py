import pulumi
from pulumi_aws import s3
bucket = s3.Bucket('agent-bucket')
pulumi.export('bucket_name', bucket.id)
