from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as lambda_,
    # aws_sqs as sqs,
)
from constructs import Construct

class Sprint1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        hwLambda = self.create_lambda('hwLambda', './resources', 'hwLambda.lambda_handler')
        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Sprint1Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )

    def create_lambda(self, id, asset, handler):
        return lambda_.Function(
            self,
            id = id,
            handler = handler,
            code = lambda_.Code.from_asset(asset),
            runtime = lambda_.Runtime.PYTHON_3_8
        )
