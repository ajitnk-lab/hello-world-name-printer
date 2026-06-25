from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    CfnOutput,
    RemovalPolicy
)
from constructs import Construct
import os

class HelloWorldNamePrinterStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket for website hosting
        website_bucket = s3.Bucket(
            self, "WebsiteBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Upload index.html to S3
        s3_deployment = s3.Bucket.add_object_from_asset(
            website_bucket,
            "index.html",
            path="index.html",
            content_type="text/html",
            content="<html><body><h1>Hello World Name Printer</h1><form id='nameForm'><input type='text' id='name' placeholder='Enter your name'><button type='submit'>Submit</button></form><div id='result'></div></body></html>"
        )

        # Create CloudFront OAC
        oac = cloudfront.OriginAccessControl(
            self, "OAC",
            origin_access_control_origin_type=cloudfront.OriginAccessControlOriginTypes.S3,
            signing_behavior=cloudfront.OriginAccessControlSigningBehavior.ALWAYS,
            signing_protocol=cloudfront.OriginAccessControlSigningProtocol.SIGV4
        )

        # Create CloudFront distribution
        distribution = cloudfront.Distribution(
            self, "Distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(
                    bucket=website_bucket,
                    origin_access_control=oac
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            default_root_object="index.html"
        )

        # Create Lambda function
        handler = lambda_.Function(
            self, "NameHandler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.Code.from_inline(
                "def handler(event, context):\n    name = event['body']\n    return {'statusCode': 200, 'body': f'Hello, {name}!'}"
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create API Gateway
        api = apigw.RestApi(
            self, "NameAPI",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=["*"],
                allow_methods=["POST"]
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        api.root.add_method(
            "POST",
            apigw.LambdaIntegration(handler)
        )

        # Output the CloudFront URL
        CfnOutput(
            self, "WebsiteURL",
            value=f"https://{distribution.domain_name}"
        )
