import boto3
from PIL import Image
from io import BytesIO
import os

s3 = boto3.client("s3")


DEST_BUCKET = "image-resize-result45"


SIZE = (300, 300)  

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

        image_data = response["Body"].read()

        
        img = Image.open(BytesIO(image_data))
        img = img.convert("RGB")
        img.thumbnail(SIZE)

        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)

        
        dest_key = f"resized/{os.path.basename(src_key)}"

        s3.put_object(
            Bucket=DEST_BUCKET,
            Key=dest_key,
            Body=buffer,
            ContentType="image/jpeg"
        )

    return {
        "statusCode": 200,
        "body": "Image resized and stored successfully"
    }
