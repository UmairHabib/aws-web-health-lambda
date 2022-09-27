import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint3.sprint3_stack import Sprint3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint3/sprint3_stack.py
def test_count_lambda():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is('AWS::Lambda::Function', 2)

def test_count_tables():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is('AWS::DynamoDB::Table', 1)

def test_count_alarms():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is('AWS::CloudWatch::Alarm', 10)

def test_find_policy():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    return template.find_resources('AWS::IAM::Policy')

def test_has_availability_metric():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties('AWS::CloudWatch::Alarm', {
        "Metrics":[{"Label": "Availability Metric"}]
    })