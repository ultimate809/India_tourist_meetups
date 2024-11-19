import boto3
import json
from datetime import datetime

s3_client = boto3.client('s3')
bucket_name = "meetupwelcomeemail"

def send_participant_in_email_queue(participant_name,participant_email, selected_meetup):
    # Message structure
    message_body = {
        "name": participant_name,
        "email": participant_email,
        "title": selected_meetup.title,
        "location": selected_meetup.location.name,
        "date": selected_meetup.date.strftime("%d/%m/%Y"),
        "description": selected_meetup.description,
    }
    file_name = f"{participant_name}-{selected_meetup.title}-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    print(message_body)

    # Sending message to SQS
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(message_body),
            ContentType="application/json"
        )
        print(f"Data successfully uploaded to {bucket_name}/{file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")


