# 🖼️ Serverless Image Resizing using AWS Lambda & Pillow

This project demonstrates how to automatically resize images uploaded to Amazon S3 using **AWS Lambda**, **Pillow (PIL)**, and **Lambda Layers**. It is designed to be beginner-friendly while also explaining advanced concepts used in real-world production systems.

---

## 📌 What Problem Does This Solve?

When users upload images (profile photos, product images, documents), we often need:

* Smaller thumbnails
* Standardized dimensions
* Optimized image formats

Doing this manually or on a server is inefficient. This project solves it **automatically and serverlessly**.

---

## 🧠 High-Level Architecture

1. User uploads an image to an S3 bucket
2. S3 triggers a Lambda function
3. Lambda uses Pillow to resize the image
4. Resized image is saved to another S3 bucket

No servers. No manual steps.

---

## 🧰 Tech Stack

* **AWS S3** – Image storage and event trigger
* **AWS Lambda** – Serverless compute
* **Python 3.10 / 3.11** – Runtime
* **Pillow (PIL)** – Image processing
* **Lambda Layer** – Dependency management

---

## 📁 S3 Buckets Used

| Purpose        | Bucket Name             |
| -------------- | ----------------------- |
| Input images   | `image-resize-input45`  |
| Resized images | `image-resize-result45` |

---

## ❓ What is Pillow?

**Pillow** is a Python image-processing library.

It allows you to:

* Open images (JPG, PNG)
* Resize, crop, rotate images
* Convert formats (PNG → JPEG)

AWS Lambda does **not** include Pillow by default, which is why we use a **Lambda Layer**.

---

## ❓ What is a Lambda Layer and Why Do We Need It?

A **Lambda Layer** is a separate package that contains dependencies your Lambda function needs.

Why we use it:

* Pillow has native C extensions
* Lambda does not allow `pip install` at runtime
* Layers keep code clean and reusable

Lambda mounts layers at:

```
/opt/python/
```

This is why `from PIL import Image` works.

---

## 🛠️ Creating the Pillow Layer (CloudShell)

> Important: Pillow must be built on **Amazon Linux** (CloudShell), not Windows.

```bash
mkdir pillow-layer
cd pillow-layer
mkdir python
pip3 install pillow==10.2.0 -t python/
zip -r pillow-layer.zip python
```

Upload `pillow-layer.zip` as a Lambda Layer and match the Python runtime.

---

## 🧪 Lambda Function Code (Fully Explained)

```python
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

        response = s3.get_object(Bucket=src_bucket, Key=src_key)
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
        "body": "Image resized successfully"
    }
```

---

## 🔍 Code Breakdown (Beginner-Friendly)

* `boto3` → Communicates with AWS services
* `BytesIO` → Handles images in memory (no disk)
* `thumbnail()` → Resizes while maintaining aspect ratio
* `os.path.basename()` → Extracts filename safely

---

## ⚙️ Lambda Configuration

Recommended settings:

| Setting | Value              |
| ------- | ------------------ |
| Runtime | Python 3.10 / 3.11 |
| Memory  | 512 MB             |
| Timeout | 15 seconds         |

---

## 🔐 IAM Permissions Required

Lambda execution role must allow:

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": [
    "arn:aws:s3:::image-resize-input45/*",
    "arn:aws:s3:::image-resize-result45/*"
  ]
}
```

---

## 🚨 Common Errors and Fixes

### ❌ `No module named PIL`

➡️ Pillow layer not attached

### ❌ `_imaging` import error

➡️ Pillow built for wrong Python version

### ❌ Nothing happens on upload

➡️ S3 trigger missing or misconfigured

---

## 🧠 Advanced Concepts Used

* Event-driven architecture
* Serverless compute
* Native dependency packaging
* Memory-based file processing
* Cloud-native image pipelines

---

## 🚀 Real-World Use Cases

* Profile photo resizing
* E-commerce product thumbnails
* CMS image optimization
* Media processing pipelines

---

## 📈 Possible Enhancements

* Multiple image sizes
* Preserve original image format
* Watermarking
* EXIF auto-rotation
* CloudFront CDN integration

---

## ✅ Final Summary

This project shows how to build a **production-ready, serverless image processing pipeline** using AWS services.

It covers both **beginner concepts** and **advanced AWS patterns** used in real systems.

---

## 👤 Author

Built as a learning + production-ready project.

If you're new to AWS, this project gives you strong fundamentals.

---

Happy building 🚀
