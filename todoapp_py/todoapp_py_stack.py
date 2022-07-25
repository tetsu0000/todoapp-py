from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_lambda,
    aws_lambda_python_alpha,
    aws_logs as logs,
    aws_apigateway as apigateway
)
from constructs import Construct


class TodoappPyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB
        todos_table = dynamodb.Table(
            self,
            'TodosTable',
            table_name='todoapp-py-todos-table',
            partition_key=dynamodb.Attribute(
                name='id',
                type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY)

        # Lambda
        todo_function = aws_lambda_python_alpha.PythonFunction(
            self,
            'TodoFunction',
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            entry='src',
            index='main.py',
            handler='handler',
            function_name='todoapp-py-function',
            environment={
                'TODOS_TABLE_NAME': todos_table.table_name
            },
        )
        # LambdaにDynamoDBのCRUD操作権限を付与
        todo_function.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                'dynamodb:Scan',
                'dynamodb:PutItem',
                'dynamodb:UpdateItem',
                'dynamodb:DeleteItem',
            ],
            resources=[todos_table.table_arn]
        ))

        # LogGroup
        logs.LogGroup(self,
                      'TodoFunctionLogs',
                      log_group_name='/aws/lambda/' + todo_function.function_name,
                      removal_policy=RemovalPolicy.DESTROY)

        # API Gateway
        api = apigateway.RestApi(self,
                                 'TodoAPI',
                                 rest_api_name='todoapp-py-api',
                                 default_cors_preflight_options=apigateway.CorsOptions(
                                     allow_origins=apigateway.Cors.ALL_ORIGINS,
                                     allow_methods=apigateway.Cors.ALL_METHODS,
                                     allow_headers=apigateway.Cors.DEFAULT_HEADERS,
                                     status_code=200
                                 ))
        integration = apigateway.LambdaIntegration(todo_function)

        # /todos
        todos_resource = api.root.add_resource('todos')
        todos_resource.add_method('GET', integration=integration)
        todos_resource.add_method('POST', integration=integration)

        # /todos/{id}
        todo_id_resource = todos_resource.add_resource('{id}')
        todo_id_resource.add_method('PUT', integration=integration)
        todo_id_resource.add_method('DELETE', integration=integration)
