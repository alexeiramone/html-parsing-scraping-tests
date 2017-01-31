# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Find these values at https://twilio.com/user/account
account_sid = "ACf588546e31d52ab3856e003f3f384614"
auth_token = "21a306b8c90095a1bbb6fd65a2a5c243"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(to="+5511983227455", from_="+553340420305", body="Bixa")