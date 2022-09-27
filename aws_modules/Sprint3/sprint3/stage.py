from aws_cdk import(
    Stage,
)
from aws_cdk import cdk
from constructs import Construct
from sprint3_stack import Sprint3Stack

class UmairStage(Stage):
    def __init__(self, scope: Construct, construct_id:str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # instantiate our app
        self.stage = Sprint3Stack(self, "UmairStageApp")
