# Design

## Architecture Overview
The application follows a simple serverless architecture using AWS services to host a static frontend that communicates with a REST API backend.

## AWS Services Used
- Amazon S3: Hosts static web content (HTML, CSS, JavaScript)
- Amazon CloudFront: Content delivery network for S3 content
- AWS Lambda: Handles form submission requests
- Amazon API Gateway: Creates REST API endpoint and manages Lambda integration

## Data Flow
1. User accesses website via CloudFront distribution
2. CloudFront serves static content from S3
3. User submits name via form
4. Form submission sends POST request to API Gateway
5. API Gateway invokes Lambda function
6. Lambda processes name and returns personalized message
7. Frontend displays the returned message

## Security
- CloudFront uses HTTPS for all traffic
- S3 bucket blocks direct public access
- API Gateway has basic request throttling enabled
- CORS policies configured on API Gateway
- No sensitive data handling required