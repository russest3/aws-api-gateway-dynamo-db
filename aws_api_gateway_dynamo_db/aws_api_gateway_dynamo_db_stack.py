from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_apigateway as apigw,
    custom_resources as cr,
    aws_logs as logs,
    RemovalPolicy,
    Duration,
)
from constructs import Construct

class AwsApiGatewayDynamoDbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB table
        table = dynamodb.Table(
            self, "ItemsTable",
            partition_key=dynamodb.Attribute(
                name="item_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Common Lambda configuration
        lambda_config = {
            "runtime": lambda_.Runtime.PYTHON_3_12,
            "environment": {
                "TABLE_NAME": table.table_name
            }
        }

        # Create Lambda functions
        get_lambda = lambda_.Function(
            self, "GetHandler",
            code=lambda_.Code.from_asset("lambda"),
            handler="get.handler",
            **lambda_config
        )

        get_lambda.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.NONE,
        )

        post_lambda = lambda_.Function(
            self, "PostHandler",
            code=lambda_.Code.from_asset("lambda"),
            handler="post.handler",
            **lambda_config
        )

        put_lambda = lambda_.Function(
            self, "PutHandler",
            code=lambda_.Code.from_asset("lambda"),
            handler="put.handler",
            **lambda_config
        )

        delete_lambda = lambda_.Function(
            self, "DeleteHandler",
            code=lambda_.Code.from_asset("lambda"),
            handler="delete.handler",
            **lambda_config,
        )

        # Lambda function to populate initial data
        init_data_lambda = lambda_.Function(
            self, "InitDataHandler",
            code=lambda_.Code.from_asset("lambda"),
            handler="init_data.handler",
            timeout=Duration.seconds(30),
            **lambda_config,
        )

        # Grant Lambda permissions to DynamoDB
        table.grant_read_data(get_lambda)
        table.grant_write_data(post_lambda)
        table.grant_write_data(put_lambda)
        table.grant_write_data(delete_lambda)
        table.grant_read_write_data(init_data_lambda)

        # Create API Gateway
        api = apigw.RestApi(
            self, "BooksApi",
            rest_api_name="Books Service",
            description="Handles CRUD operations for books",
            endpoint_types=[apigw.EndpointType.REGIONAL],
            deploy_options=apigw.StageOptions(
                logging_level=apigw.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
                stage_name="dev"
            ),
            cloud_watch_role=True,
            cloud_watch_role_removal_policy=RemovalPolicy.DESTROY,
            default_cors_preflight_options={
                "allow_origins": apigw.Cors.ALL_ORIGINS,
                "allow_methods": apigw.Cors.ALL_METHODS,
            },
            deploy=True,
            retain_deployments=False,
            api_key_source_type=apigw.ApiKeySourceType.HEADER,
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

        api_key = apigw.ApiKey(self, "MyApiKey",
            api_key_name="MyServiceApiKey",
            enabled=True
        )

        usage_plan = api.add_usage_plan("MyUsagePlan",
            name="MyServiceUsagePlan",
            api_stages=[apigw.UsagePlanPerApiStage(
                api=api,
                stage=api.deployment_stage,
            )],
        )

        usage_plan.add_api_key(api_key)

        books = api.root.add_resource("books")
        book = books.add_resource("{book_id}")

        # Connect methods to Lambda functions
        get_method = books.add_method("GET", apigw.LambdaIntegration(get_lambda), api_key_required=True)
        post_method = books.add_method("POST", apigw.LambdaIntegration(post_lambda), api_key_required=True)
        put_method = book.add_method("PUT", apigw.LambdaIntegration(put_lambda), api_key_required=True)
        delete_method = book.add_method("DELETE", apigw.LambdaIntegration(delete_lambda), api_key_required=True)

        # Output API URL
        self.api_url = api.url

# curl -kv http://api_url/
# Should return table
