import boto3
import base64
import hashlib
import hmac
import uuid
import datetime
import requests

client = boto3.client('workmail')

response = client.list_users(
    OrganizationId='m-4d1878281b9f4c3794f47393be4bfcf5',
    MaxResults=100
)

users = response['Users']

name = []
email = []
count = 0
for user in users:
    name.append(user['DisplayName'])
    email.append(user['Email'])
    count += 1
print(name)
print(email)

base_url = "https://ca-api.mimecast.com"
uri = "/api/user/create-user"
url = base_url + uri
access_key = "mYtOL3XZCOwG96BOiFTZRmaOeUw51MRzxI4ruf7Of5Ra8lsYf3OLpmotY6DX4i1mgdRngrzQkCxdKsPZGjbNvZMhG4FfXuwRthwqtXyFxcTNO3iNzaI1HqA2COyxaU8BYW8cxZnXEtfPBcvjfCLs6Q"
secret_key = "+VWpAFHyyAWccJHxUloi1baW/QBCFjhq1Czq73iGfpz3NfUFqMau+ZB56eGHCzxNdA7L3WpKLr8Xqi3ybCaLMw=="
app_id = "08877ab2-d68c-4c1b-bc3a-c7dae92f63da"
app_key = "96f2fe4b-23cf-4477-8305-52fde648f041"
 
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

for index in range(0, count):
    payload = {
            'data': [
                {
                    'emailAddress': email[index],
                    'name': name[index]
                }
            ]
        }
    r = requests.post(url=url, headers=headers, data=str(payload))
    print(r.text)
 
