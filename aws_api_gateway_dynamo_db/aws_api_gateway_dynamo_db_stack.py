# This works but needs every method updated

from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_apigateway as apigw,
    aws_logs as logs,
    RemovalPolicy,
)
from constructs import Construct

class AwsApiGatewayDynamoDbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_policy_document = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=[
        				"dynamodb:DeleteItem",
        				"dynamodb:GetItem",
        				"dynamodb:PutItem",
        				"dynamodb:Query",
        				"dynamodb:Scan",
        				"dynamodb:UpdateItem",
                        "dynamodb:ConditionCheckItem",
        				"logs:CreateLogGroup",
        				"logs:CreateLogStream",
        				"logs:PutLogEvents",
                        "logs:DescribeLogStreams",
        			],
                    resources=["*"],
                    effect=iam.Effect.ALLOW
                ),
            ]
        )

        custom_policy = iam.Policy(
            self, "lambda-apigateway-policy",
            policy_name="lambda-apigateway-policy",
            document=my_policy_document
        )

        custom_role = iam.Role(
            self, "lambda-apigateway-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            role_name="lambda-apigateway-role",
            description="Custom IAM role for Lambda function",
        )

        custom_policy.attach_to_role(custom_role)

        lambda_functions = lambda_.Function(
            self, "LambdaFunctions",
            function_name="LambdaFunctions",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="functions.functions_handler",
            code=lambda_.Code.from_asset("lambda"),
            role=custom_role,
            environment={
                "TABLE_NAME": "lambda-apigateway-table"
            }
        )

        api = apigw.RestApi(
            self, "DynamoDBOperations",
            rest_api_name="DynamoDBOperations",
            endpoint_types=[apigw.EndpointType.REGIONAL],
            deploy_options=apigw.StageOptions(
                logging_level=apigw.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                stage_name="test"
            ),
            cloud_watch_role=True,
            cloud_watch_role_removal_policy=RemovalPolicy.DESTROY,
            default_cors_preflight_options={
                "allow_origins": apigw.Cors.ALL_ORIGINS,
                "allow_methods": apigw.Cors.ALL_METHODS,
            },
            deploy=True,
            retain_deployments=False,
            # api_key_source_type=apigw.ApiKeySourceType.HEADER,
            policy=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        actions=["execute-api:Invoke"],
                        principals=[iam.AnyPrincipal()],
                        resources=["execute-api:/*"]
                    )
                ]
            )
        )

        endpoint = api.root.add_resource("dynamodb-operations")
        endpoint.add_method("ANY", apigw.LambdaIntegration(lambda_functions, proxy=False))


        lambda_functions.add_permission(
            "lambda-apigateway-permission",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_arn=api.arn_for_execute_api()
        )

        table = dynamodb.Table(
            self, "lambda-apigateway-table",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            table_name="lambda-apigateway-table",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        table.grant_read_write_data(lambda_functions)

        # Output API URL
        self.api_url = api.url
