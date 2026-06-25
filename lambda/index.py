import json
import base64


def handler(event, context):
    try:
        # Parse the body from the event
        body = event.get("body", "")

        if event.get("isBase64Encoded", False):
            body = base64.b64decode(body).decode("utf-8")

        if isinstance(body, str):
            body = json.loads(body)

        # Extract and validate name
        name = body.get("name", "").strip() if isinstance(body, dict) else ""

        if not name:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "POST,OPTIONS",
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"message": "Name is required and cannot be empty."})
            }

        if len(name) > 256:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "POST,OPTIONS",
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"message": "Name must not exceed 256 characters."})
            }

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"greeting": f"Hello, {name}!"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,OPTIONS",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "An unexpected error occurred."})
        }
