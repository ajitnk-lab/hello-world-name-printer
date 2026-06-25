from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    CfnOutput,
    RemovalPolicy
)
from constructs import Construct


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

        # Create CloudFront distribution with S3 origin using OAC (managed automatically)
        distribution = cloudfront.Distribution(
            self, "Distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(website_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            default_root_object="index.html"
        )

        # Deploy frontend assets to S3
        s3_deployment.BucketDeployment(
            self, "DeployWebsite",
            sources=[s3_deployment.Source.asset("../frontend")],
            destination_bucket=website_bucket,
            distribution=distribution,
            distribution_paths=["/*"]
        )

        # Create Lambda function
        handler = lambda_.Function(
            self, "NameHandler",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset("../lambda")
        )

        # Create API Gateway
        api = apigw.RestApi(
            self, "NameAPI",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=["*"],
                allow_methods=["POST", "OPTIONS"]
            )
        )

        # Add /submit resource with POST method
        submit_resource = api.root.add_resource("submit")
        submit_resource.add_method(
            "POST",
            apigw.LambdaIntegration(handler)
        )

        # Output the CloudFront URL
        CfnOutput(
            self, "WebsiteURL",
            value=f"https://{distribution.domain_name}"
        )

        # Output the API Gateway URL
        CfnOutput(
            self, "ApiURL",
            value=api.url
        )
