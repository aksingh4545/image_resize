import boto3
from PIL import Image
from io import BytesIO
import os

s3 = boto3.client("s3")
sns = boto3.client("sns")

SNS_TOPIC_ARN = " "

RESULT_BUCKET = "image-resize-result45"
BACKUP_BUCKET = "image-resize-backup45"

DEFAULT_WIDTH = 300
DEFAULT_HEIGHT = 300


def lambda_handler(event, context):

    for record in event["Records"]:
        src_bucket = record["s3"]["bucket"]["name"]
        src_key = record["s3"]["object"]["key"]

        if src_key.endswith("/") or not src_key.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        response = s3.get_object(
            Bucket=src_bucket,
            Key=src_key
        )

        image_bytes = response["Body"].read()
        content_type = response.get("ContentType", "image/jpeg")

        # 1️⃣ Backup original image
        s3.put_object(
            Bucket=BACKUP_BUCKET,
            Key=os.path.basename(src_key),
            Body=image_bytes,
            ContentType=content_type
        )

        # 2️⃣ Read resize dimensions
        metadata = response.get("Metadata", {})
        width = int(metadata.get("width", DEFAULT_WIDTH))
        height = int(metadata.get("height", DEFAULT_HEIGHT))

        # 3️⃣ Resize image
        image = Image.open(BytesIO(image_bytes))
        image = image.convert("RGB")
        image = image.resize((width, height))

        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)

        # 4️⃣ Save resized image
        dest_key = f"resized/{os.path.basename(src_key)}"

        s3.put_object(
            Bucket=RESULT_BUCKET,
            Key=dest_key,
            Body=buffer,
            ContentType="image/jpeg"
        )

        # 5️⃣ Send SNS notification
        message = (
            "Image resize completed successfully.\n\n"
            f"Original file: {src_key}\n"
            f"Resized file: {dest_key}\n"
            f"Size: {width} x {height}"
        )

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Image Resize Completed",
            Message=message
        )

    return {
        "statusCode": 200,
        "body": "Image backed up, resized, and notification sent"
    }
