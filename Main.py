import Playsound_Play
import Google_StT_Streaming
import Google_TtS
import RaSmails

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = \
    "/Users/anirudh/Documents/GitHub/Python-Exercises/googleSpeechToText/GMAIL_gTtS_gStT_ServiceAccountKey.json"


gmail_service_instance = RaSmails.get_gmail_service_instance()

# read email
print('Reading EMail')
mails_df =  RaSmails.read_main_info(gmail_service_instance)
print('Snippet: ', mails_df.loc[0,'Snippet'])
# convert text to speech
file = Google_TtS.google_TtS(mails_df.loc[0,'Snippet'])

print('Playing EMail')
# play the email
Playsound_Play.play(file)

# record the response
print('Recording Response EMail')
response_transcript = Google_StT_Streaming.main()
response_transcript = response_transcript.replace('exit','.')
print('response_transcript: ', response_transcript)

# # send the response
send_to = mails_df.loc[0,'Sender']
threadId = mails_df.loc[0,'threadId']
subject =  mails_df.loc[0,'Subject']
reply_body = response_transcript
#
print('Sending EMail')
emsg = RaSmails.CreateMessage('Me',send_to, subject, threadId, reply_body)

if threadId is None:
    print(RaSmails.SendMessage(gmail_service_instance,'Me',emsg))
else:
    draft = gmail_service_instance.users().drafts().create(userId="me", body=emsg).execute()
    print('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))
    message = gmail_service_instance.users().drafts().send(userId='me', body={'id': draft['id']}).execute()
    print(message)
