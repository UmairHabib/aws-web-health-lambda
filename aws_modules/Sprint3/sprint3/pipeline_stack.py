from aws_cdk import (
    # Duration,
    SecretValue,
    Stack,
    pipelines,
    aws_codepipeline_actions as actions
    # aws_sqs as sqs,
)
from constructs import Construct
from stage import UmairStage

class MyPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # define source
        source = pipelines.CodePipelineSource.git_hub("umair-habib2022skipq/SculptorRepo_Python", branch="main",
        authentication=SecretValue.secrets_manager('gitSecret2'), trigger=actions.GitHubTrigger(value='POLL'))

        # build code with shellstep
        synth = pipelines.ShellStep("umairSynth",
        input=source,
        commands=["cd UmairHabib/Sprint3/", "npm install -g aws-cdk", "pip install -r requirements.txt", "cdk synth"],
        primary_output_directory="UmairHabib/Sprint3/cdk.out")
        
        
        # creating our pipeline
        my_pipeline = pipelines.CodePipeline(self, 
        "umairSynth", synth=synth,
        )

        # beta stage
        beta_stage = UmairStage(self, "betaUmairStage")
        # gamma stage
        gamma_stage = UmairStage(self, "gammaUmairStage")
        # prod stage
        prof_stage = UmairStage(self, "prodUmairStage")

        my_pipeline.add_stage(beta_stage, pre=[synth])
        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Sprint3Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )
