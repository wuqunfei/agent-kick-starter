import pulumi
from pulumi_gcp import storage
bucket = storage.Bucket('agent-bucket')
pulumi.export('bucket_name', bucket.name)
