<h1>🖼️ Serverless Image Resizing with AWS Lambda, Pillow, and SNS</h1>

<p>
This project implements an event-driven, serverless image processing pipeline on AWS.
Images uploaded to Amazon S3 are automatically resized using AWS Lambda and Pillow,
stored in a destination bucket, and followed by an email notification using Amazon SNS.
</p>

<hr />

<h2>📌 Problem Statement</h2>
<p>
Applications that accept user-uploaded images often need standardized image sizes
for thumbnails, profile photos, or product listings.
Handling this on traditional servers increases operational overhead and cost.
</p>

<p>
This project solves the problem using a fully serverless approach:
</p>

<ul>
  <li>Automatic image resizing on upload</li>
  <li>No servers or background workers to manage</li>
  <li>Instant notification once processing is complete</li>
</ul>

<hr />

<h2>🧠 High-Level Architecture</h2>
<ol>
  <li>User uploads an image to an S3 bucket</li>
  <li>S3 triggers an AWS Lambda function</li>
  <li>Lambda resizes the image using Pillow (via a Lambda Layer)</li>
  <li>Resized image is saved to a destination S3 bucket</li>
  <li>Lambda publishes a notification to an SNS topic</li>
</ol>

<p>
This design follows an event-driven, cloud-native architecture.
</p>

<hr />

<h2>🧰 Tech Stack</h2>
<ul>
  <li><strong>AWS S3</strong> – Image storage and event source</li>
  <li><strong>AWS Lambda</strong> – Serverless compute</li>
  <li><strong>Python 3.10 / 3.11</strong> – Runtime</li>
  <li><strong>Pillow (PIL)</strong> – Image processing</li>
  <li><strong>Lambda Layer</strong> – Dependency packaging</li>
  <li><strong>AWS SNS</strong> – Email notifications</li>
</ul>

<hr />

<h2>📁 S3 Buckets</h2>
<table>
  <tr>
    <th>Purpose</th>
    <th>Bucket Name</th>
  </tr>
  <tr>
    <td>Input images</td>
    <td><code>image-resize-input45</code></td>
  </tr>
  <tr>
    <td>Resized images</td>
    <td><code>image-resize-result45</code></td>
  </tr>
  <tr>
    <td>Backup originals</td>
    <td><code>image-resize-backup45</code></td>
  </tr>
</table>

<hr />

<h2>❓ Why Pillow and Lambda Layers</h2>
<p>
AWS Lambda does not include Pillow by default.
Since Pillow depends on native system libraries, it must be packaged separately.
</p>

<p>
A Lambda Layer is used to:
</p>
<ul>
  <li>Package Pillow correctly for Amazon Linux</li>
  <li>Keep Lambda function code clean</li>
  <li>Reuse the dependency across functions</li>
</ul>

<p>
Lambda automatically mounts layers at:
</p>
<pre><code>/opt/python/</code></pre>

<hr />

<h2>🛠️ Creating the Pillow Layer (AWS CloudShell)</h2>
<p>
Pillow must be built on Amazon Linux. Use AWS CloudShell:
</p>

<pre><code>
mkdir pillow-layer
cd pillow-layer
mkdir python
pip3 install pillow==10.2.0 -t python/
zip -r pillow-layer.zip python
</code></pre>

<p>
Upload <code>pillow-layer.zip</code> as a Lambda Layer and attach it to your function.
</p>

<hr />

<h2>🧪 Lambda Function Overview</h2>
<p>
The Lambda function performs the following steps:
</p>

<ul>
  <li>Reads the uploaded image from S3</li>
  <li>Backs up the original image</li>
  <li>Resizes the image using Pillow</li>
  <li>Saves the resized image to a destination bucket</li>
  <li>Sends a notification using SNS</li>
</ul>

<hr />

<h2>🔍 Key Concepts Used</h2>
<ul>
  <li>Event-driven architecture</li>
  <li>Serverless compute</li>
  <li>In-memory file processing</li>
  <li>Native dependency packaging</li>
  <li>Asynchronous notifications with SNS</li>
</ul>

<hr />

<h2>⚙️ Lambda Configuration</h2>
<table>
  <tr>
    <th>Setting</th>
    <th>Recommended Value</th>
  </tr>
  <tr>
    <td>Runtime</td>
    <td>Python 3.10 / 3.11</td>
  </tr>
  <tr>
    <td>Memory</td>
    <td>512 MB</td>
  </tr>
  <tr>
    <td>Timeout</td>
    <td>15 seconds</td>
  </tr>
</table>

<hr />

<h2>🔐 IAM Permissions</h2>
<p>
The Lambda execution role requires the following permissions:
</p>

<pre><code>
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject",
    "sns:Publish"
  ],
  "Resource": [
    "arn:aws:s3:::image-resize-input45/*",
    "arn:aws:s3:::image-resize-result45/*",
    "arn:aws:s3:::image-resize-backup45/*",
    "arn:aws:sns:ap-south-1:ACCOUNT_ID:image-resize-notification"
  ]
}
</code></pre>

<hr />

<h2>🚨 Common Issues</h2>
<ul>
  <li><strong>No module named PIL</strong> – Pillow layer not attached</li>
  <li><strong>_imaging import error</strong> – Layer built for wrong Python version</li>
  <li><strong>Lambda not triggered</strong> – S3 event notification missing</li>
  <li><strong>SNS publish denied</strong> – Missing <code>sns:Publish</code> permission</li>
</ul>

<hr />

<h2>🚀 Real-World Use Cases</h2>
<ul>
  <li>User profile photo processing</li>
  <li>E-commerce product image resizing</li>
  <li>CMS image optimization pipelines</li>
  <li>Media processing workflows with alerts</li>
</ul>

<hr />

<h2>📈 Possible Enhancements</h2>
<ul>
  <li>Multiple output sizes</li>
  <li>Preserve original image format</li>
  <li>Watermarking</li>
  <li>EXIF auto-rotation</li>
  <li>CloudFront CDN integration</li>
</ul>

<hr />

<h2>✅ Summary</h2>
<p>
This project demonstrates a clean, production-ready approach to serverless image processing on AWS.
It combines S3, Lambda, Pillow, and SNS into a scalable, low-maintenance pipeline suitable for real systems.
</p>

<p>
Built as a learning-focused yet production-aligned implementation.
</p>
