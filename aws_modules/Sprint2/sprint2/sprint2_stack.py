from aws_cdk import (
    # Duration,
    RemovalPolicy,
    aws_lambda as lambda_,
    Stack,
    aws_events as events_,
    Duration,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as cw_actions,
    aws_dynamodb as db
    # aws_sqs as sqs,
)
import os
from constructs import Construct
from resources import constants
class Sprint2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        lambda_role = self.create_lambda_cloudwatch_role()  # giving lambda permission to use cloudwatch
        web_health_lambda = self.create_lambda('web_health_app', './resources', 'web_health_app.lambda_handler', lambda_role)
        web_health_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # DBlambda for writing cloudwatch alarm action details to db table
        db_lambda = self.create_lambda('db_lambda', './resources', 'db_app.lambda_handler', lambda_role)
        db_lambda.apply_removal_policy(RemovalPolicy.DESTROY)


        # creating DB table
        table = db.Table(self, "AlarmTable",
        partition_key=db.Attribute(name="id", type=db.AttributeType.STRING),
        removal_policy=RemovalPolicy.DESTROY)
        table.grant_full_access(db_lambda)
        table_name = table.table_name
        db_lambda.add_environment("table_name", table_name)

        # triggering lambda as cron job
        # event generation
        events_lambda = events_.Schedule.rate(Duration.minutes(1))
        # defining target
        event_target = targets_.LambdaFunction(web_health_lambda)

        # binding rule with event and target
        event_rule = events_.Rule(self, "LambdaInvocationRule", 
        description="Periodic lambda function",
        schedule=events_lambda,
        targets=[event_target]
        )

        # SNS Topic for publishing alarm details to email
        topic = sns_.Topic(self, 'WebHealthNotifications')
        topic.apply_removal_policy(RemovalPolicy.DESTROY)
        topic.add_subscription(subscriptions_.EmailSubscription("umair.habib.skipq@gmail.com"))
        topic.add_subscription(subscriptions_.LambdaSubscription(db_lambda))
        # refering lambda matrics to cloudwatch for generating alarms
        # using same namespace and matric name for refering metric
        for value in constants.URLS_TO_MONITOR:
            cloudwatch_dimensions = {"url": value}
            availability_metric = cloudwatch_.Metric(
                metric_name=constants.URL_MONITOR_METRIC_NAME_AVAILABILITY,
                namespace=constants.URL_MONItOR_NAMESPACE,
                dimensions_map=cloudwatch_dimensions,
                label=value + " Availability Metric",
                period=Duration.minutes(1)
            )

            latency_metric = cloudwatch_.Metric(
                metric_name=constants.URL_MONITOR_METRIC_NAME_LATENCY,
                namespace=constants.URL_MONItOR_NAMESPACE,
                dimensions_map=cloudwatch_dimensions,
                label=value + " Latency Metric",
                period=Duration.minutes(1)
            )


            # creating alarm
            availability_alarm = cloudwatch_.Alarm(
                self,
                value + " availability_Alarm",
                metric=availability_metric,
                evaluation_periods=1,
                comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                threshold=1,
                datapoints_to_alarm=1
            )


            latency_alarm = cloudwatch_.Alarm(
                self,
                value + " latency_Alarm",
                metric=latency_metric,
                evaluation_periods=1,
                comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
                threshold=.22,
                datapoints_to_alarm=1
            )

            availability_alarm.add_alarm_action(cw_actions.SnsAction(topic))
            latency_alarm.add_alarm_action(cw_actions.SnsAction(topic))
            

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Sprint2Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )

    def create_lambda(self, id, asset, handler, temp_role):
        return lambda_.Function(
            self,
            id = id,
            handler = handler,
            code = lambda_.Code.from_asset(asset),
            runtime = lambda_.Runtime.PYTHON_3_8,
            role=temp_role
        )
    
    def create_lambda_cloudwatch_role(self):
        lambda_role = aws_iam.Role(self,
        'lambda-role', 
        assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies=[
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess')
        ])
        return lambda_role

