import streamlit as st
import boto3
import json
import re
import os

s3 = boto3.client("s3", region_name="ap-south-1")
lambda_client = boto3.client("lambda", region_name="ap-south-1")

INPUT_BUCKET = "image-resize-input45"


def normalize_filename(filename: str) -> str:
    base = os.path.basename(filename)
    base = re.sub(r"\(\d+\)", "", base)
    return base


st.title("Image Resize & Restore System")

option = st.radio(
    "Select Action",
    ["Resize Image", "Get Original Image Back"]
)

# Show resize options ONLY for resize
if option == "Resize Image":
    st.subheader("Resize Options")

    width = st.number_input(
        "Width (px)",
        min_value=50,
        max_value=2000,
        value=300,
        step=50
    )

    height = st.number_input(
        "Height (px)",
        min_value=50,
        max_value=2000,
        value=300,
        step=50
    )
else:
    width = None
    height = None

uploaded_file = st.file_uploader(
    "Upload image",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file and st.button("Submit"):

    raw_name = uploaded_file.name
    file_name = normalize_filename(raw_name)

    # ------------------ RESIZE FLOW ------------------
    if option == "Resize Image":
        s3.upload_fileobj(
            uploaded_file,
            INPUT_BUCKET,
            file_name,
            ExtraArgs={
                "ContentType": uploaded_file.type,
                "Metadata": {
                    "width": str(width),
                    "height": str(height)
                }
            }
        )

        st.success("Image uploaded successfully.")
        st.info(f"Resizing to {width} x {height}px")

    # ------------------ RESTORE FLOW ------------------
    else:
        response = lambda_client.invoke(
            FunctionName="restore-original-image-lambda",
            InvocationType="RequestResponse",
            Payload=json.dumps({"file_name": file_name})
        )

        result = json.loads(response["Payload"].read())

        if result["statusCode"] == 200:
            image_bytes = result["image_bytes"].encode("latin1")
            st.image(image_bytes, caption="Original Image Restored")
        else:
            st.error(result["message"])
