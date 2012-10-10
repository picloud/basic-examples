"""
Queries your s3 bucket from your local machine, and from PiCloud.
You'll need to fill in your AWS Access Credentials.
"""

import boto

AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''

def list_of_all_buckets():
    conn = boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    buckets = conn.get_all_buckets()
    return [bucket.name for bucket in buckets]

print 'Running locally', list_of_all_buckets()

jid = cloud.call(list_of_all_buckets)
print 'Running on the cloud', cloud.result(jid)

