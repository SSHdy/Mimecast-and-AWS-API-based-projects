import base64
import hashlib
import hmac
import uuid
import datetime
import requests
import boto3

# Setup required variables
base_url = "https://ca-api.mimecast.com"
uri = "/api/domain/create-domain"
url = base_url + uri
access_key = "mYtOL3XZCOwG96BOiFTZRkcqQZHs5_IMSaR692elbg_muuPavni5YlsY_hzKZ8IRUvM44vE25s_ZHHPzRSjfr0IUtpioUaP6EQAkOkGV27Tila0C9glC4HvsSiJLBlKqrB1q67kltB-YcIRxYoHYqg"
secret_key = "+2//B9dUvSXffZPo169LeT05M9qOBZY+DhD2tpzClWBgk5IJW80mOxdG9fF4qvGj3ao4aet3SjRmSTyKff0Ygw=="
app_id = "4f383146-811d-4f7a-b84b-3063203e8d66"
app_key = "406b30e5-35dc-4d53-9a8e-35cbae763e1e"
## commenting 

domain_name = input("What is domain name?")
Caller_reference = domain_name + "0001"
# Generate request header values
request_id = str(uuid.uuid4())
hdr_date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " UTC"
 
 
# DataToSign is used in hmac_sha1
dataToSign = ':'.join([hdr_date, request_id, uri, app_key])
 
# Create the HMAC SHA1 of the Base64 decoded secret key for the Authorization header
hmac_sha1 = hmac.new(base64.b64decode(secret_key), dataToSign.encode(), digestmod=hashlib.sha1).digest()
 
# Use the HMAC SHA1 value to sign the hdrDate + ":" requestId + ":" + URI + ":" + appkey
sig = base64.b64encode(hmac_sha1).rstrip()
 
# Create request headers
headers = {
    'Authorization': 'MC ' + access_key + ':' + sig.decode(),
    'x-mc-app-id': app_id,
    'x-mc-date': hdr_date,
    'x-mc-req-id': request_id,
    'Content-Type': 'application/json'
}
 
payload = {
 "data": [
     {
         "domain": domain_name,
         "inboundType": "known"
     }
 ]
}
 
r = requests.post(url=url, headers=headers, data=str(payload))

count = 0
token =""
start = False
for item in r.text:
    if item == ":":
        count += 1
        continue
    if count == 6:
        start = True
    if start:
        if item == ",":
            break
    if start:
        token = token + item
token = token[1:len(token) - 1]

client = boto3.client('route53')

response = client.create_hosted_zone(
    Name=domain_name,
    CallerReference= Caller_reference,
    HostedZoneConfig={
        'Comment': 'none',
        'PrivateZone': False
    }
)
hostedzone_id = response["HostedZone"]["Id"]

hostedzone_id = hostedzone_id[12:]

client = boto3.client('route53')
response = client.change_resource_record_sets(
    ChangeBatch={
        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': domain_name,
                    'ResourceRecords': [
                        {
                            'Value': "\"" + token + "\"",
                        },
                    ],
                    'TTL': 600,
                    'Type': 'TXT',
                },
            },
        ],
        'Comment': 'Web Server',
    },
    HostedZoneId=hostedzone_id,
)