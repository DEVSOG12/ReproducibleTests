'''
# aws-events-rule-sqs module

<!--BEGIN STABILITY BANNER-->---


![Stability: Deprecated](https://img.shields.io/badge/STABILITY-DEPRECATED-red?style=for-the-badge)

> Some of our early constructs don’t meet the naming standards that evolved for the library. We are releasing completely feature compatible versions with corrected names. The underlying implementation code is the same regardless of whether you deploy the construct using the old or new name. We will support both names for all 1.x releases, but in 2.x we will only publish the correctly named constructs. This construct is being replaced by the functionally identical aws-eventbridge-sqs.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_events_rule_sqs`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-events-rule-sqs`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.eventsrulesqs`|

## Overview

This AWS Solutions Construct implements an AWS Events rule and an AWS SQS Queue.

Here is a minimal deployable pattern definition:

Typescript

```python
// aws-events-rule-sqs has been deprecated for CDK V2 in favor of aws-eventbridge-sqs.
// This sample uses the CDK V1 syntax
import * as cdk from '@aws-cdk/core';
import * as events from '@aws-cdk/aws-events';
import * as iam from '@aws-cdk/aws-iam';
import { EventsRuleToSqsProps, EventsRuleToSqs } from "@aws-solutions-constructs/aws-events-rule-sqs";

const constructProps: EventsRuleToSqsProps = {
  eventRuleProps: {
    schedule: events.Schedule.rate(cdk.Duration.minutes(5))
  }
};

const constructStack = new EventsRuleToSqs(this, 'test', constructProps);

// Grant yourself permissions to use the Customer Managed KMS Key
const policyStatement = new iam.PolicyStatement({
  actions: ["kms:Encrypt", "kms:Decrypt"],
  effect: iam.Effect.ALLOW,
  principals: [new iam.AccountRootPrincipal()],
  resources: ["*"]
});

constructStack.encryptionKey?.addToResourcePolicy(policyStatement);
```

Python

```python
# aws-events-rule-sqs has been deprecated for CDK V2 in favor of aws-eventbridge-sqs.
# This sample uses the CDK V1 syntax
from aws_solutions_constructs.aws_events_rule_sqs import EventsRuleToSqs
from aws_cdk import (
    aws_events as events,
    aws_iam as iam,
    core
)

construct_stack = EventsRuleToSqs(self, 'test',
                            event_rule_props=events.RuleProps(
                                schedule=events.Schedule.rate(
                                    core.Duration.minutes(5))
                            ))

# Grant yourself permissions to use the Customer Managed KMS Key
policy_statement = iam.PolicyStatement(
    actions=["kms:Encrypt", "kms:Decrypt"],
    effect=iam.Effect.ALLOW,
    principals=[iam.AccountRootPrincipal()],
    resources=["*"]
)

construct_stack.encryption_key.add_to_resource_policy(policy_statement)
```

Java

```java
// aws-events-rule-sqs has been deprecated for CDK V2 in favor of aws-eventbridge-sqs.
// This sample uses the CDK V1 syntax
import software.constructs.Construct;
import java.util.List;

import software.amazon.awscdk.core.*;
import software.amazon.awscdk.services.events.*;
import software.amazon.awscdk.services.iam.*;
import software.amazon.awsconstructs.services.eventsrulesqs.*;

final EventsRuleToSqs constructStack = new EventsRuleToSqs(this, "test-construct",
        new EventsRuleToSqsProps.Builder()
                .eventRuleProps(new RuleProps.Builder()
                        .schedule(Schedule.rate(Duration.minutes(5)))
                        .build())
                .build());

// Grant yourself permissions to use the Customer Managed KMS Key
final PolicyStatement policyStatement = PolicyStatement.Builder.create()
        .actions(List.of("kms:Encrypt", "kms:Decrypt"))
        .effect(Effect.ALLOW)
        .principals(List.of(new AccountRootPrincipal()))
        .resources(List.of("*"))
        .build();

constructStack.getEncryptionKey().addToResourcePolicy(policyStatement);
```

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|existingEventBusInterface?|[`events.IEventBus`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.IEventBus.html)| Optional user-provided custom EventBus for construct to use. Providing both this and `eventBusProps` results an error.|
|eventBusProps?|[`events.EventBusProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.EventBusProps.html)|Optional user-provided properties to override the default properties when creating a custom EventBus. Setting this value to `{}` will create a custom EventBus using all default properties. If neither this nor `existingEventBusInterface` is provided the construct will use the `default` EventBus. Providing both this and `existingEventBusInterface` results an error.|
|eventRuleProps|[`events.RuleProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.RuleProps.html)|User provided eventRuleProps to override the defaults. |
|existingQueueObj?|[`sqs.Queue`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.Queue.html)|An optional, existing SQS queue to be used instead of the default queue. Providing both this and `queueProps` will cause an error.|
|queueProps?|[`sqs.QueueProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.QueueProps.html)|User provided props to override the default props for the SQS Queue. |
|enableQueuePurging?|`boolean`|Whether to grant additional permissions to the Lambda function enabling it to purge the SQS queue. Defaults to `false`.|
|deployDeadLetterQueue?|`boolean`|Whether to create a secondary queue to be used as a dead letter queue. Defaults to `true`.|
|deadLetterQueueProps?|[`sqs.QueueProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.QueueProps.html)|Optional user-provided props to override the default props for the dead letter queue. Only used if the `deployDeadLetterQueue` property is set to true.|
|maxReceiveCount?|`number`|The number of times a message can be unsuccessfully dequeued before being moved to the dead letter queue. Defaults to `15`.|
|enableEncryptionWithCustomerManagedKey?|`boolean`|Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct.|
|encryptionKey?|[`kms.Key`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kms.Key.html)|An optional, imported encryption key to encrypt the SQS queue.|
|encryptionKeyProps?|[`kms.KeyProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kms.KeyProps.html)|An optional, user provided properties to override the default properties for the KMS encryption key.|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|eventBus?|[`events.IEventBus`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.IEventBus.html)|Returns the instance of events.IEventBus used by the construct|
|eventsRule|[`events.Rule`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.Rule.html)|Returns an instance of events.Rule created by the construct|
|sqsQueue|[`sqs.Queue`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.Queue.html)|Returns an instance of sqs.Queue created by the construct|
|encryptionKey?|[`kms.Key`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kms.Key.html)|Returns an instance of kms Key used for the SQS queue.|
|deadLetterQueue?|[`sqs.Queue`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.Queue.html)|Returns an instance of the dead-letter SQS queue created by the pattern.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon CloudWatch Events Rule

* Grant least privilege permissions to CloudWatch Events to publish to the SQS Queue.

### Amazon SQS Queue

* Deploy SQS dead-letter queue for the source SQS Queue.
* Enable server-side encryption for source SQS Queue using Customer managed KMS Key.
* Enforce encryption of data in transit.

## Architecture

![Architecture Diagram](architecture.png)

---


© Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_events
import aws_cdk.aws_kms
import aws_cdk.aws_sqs
import aws_cdk.core


class EventsRuleToSqs(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-solutions-constructs/aws-events-rule-sqs.EventsRuleToSqs",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        event_rule_props: typing.Union[aws_cdk.aws_events.RuleProps, typing.Dict[str, typing.Any]],
        dead_letter_queue_props: typing.Optional[typing.Union[aws_cdk.aws_sqs.QueueProps, typing.Dict[str, typing.Any]]] = None,
        deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
        enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
        enable_queue_purging: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
        encryption_key_props: typing.Optional[typing.Union[aws_cdk.aws_kms.KeyProps, typing.Dict[str, typing.Any]]] = None,
        event_bus_props: typing.Optional[typing.Union[aws_cdk.aws_events.EventBusProps, typing.Dict[str, typing.Any]]] = None,
        existing_event_bus_interface: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        existing_queue_obj: typing.Optional[aws_cdk.aws_sqs.Queue] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        queue_props: typing.Optional[typing.Union[aws_cdk.aws_sqs.QueueProps, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param dead_letter_queue_props: Optional user provided properties for the dead letter queue. Default: - Default props are used
        :param deploy_dead_letter_queue: Whether to deploy a secondary queue to be used as a dead letter queue. Default: - true.
        :param enable_encryption_with_customer_managed_key: Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct. Default: - true (encryption enabled, managed by this CDK app).
        :param enable_queue_purging: Whether to grant additional permissions to the Lambda function enabling it to purge the SQS queue. Default: - "false", disabled by default.
        :param encryption_key: An optional, imported encryption key to encrypt the SQS queue, and SNS Topic. Default: - not specified.
        :param encryption_key_props: Optional user-provided props to override the default props for the encryption key. Default: - Default props are used.
        :param event_bus_props: A new custom EventBus is created with provided props. Default: - None
        :param existing_event_bus_interface: Existing instance of a custom EventBus. Default: - None
        :param existing_queue_obj: Existing instance of SQS queue object, providing both this and queueProps will cause an error. Default: - None
        :param max_receive_count: The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue. Default: - required field if deployDeadLetterQueue=true.
        :param queue_props: User provided props to override the default props for the SQS queue. Default: - Default props are used

        :access: public
        :since: 1.62.0
        :summary: Constructs a new instance of the EventsRuleToSqs class.
        '''
        if __debug__:
            def stub(
                scope: aws_cdk.core.Construct,
                id: builtins.str,
                *,
                event_rule_props: typing.Union[aws_cdk.aws_events.RuleProps, typing.Dict[str, typing.Any]],
                dead_letter_queue_props: typing.Optional[typing.Union[aws_cdk.aws_sqs.QueueProps, typing.Dict[str, typing.Any]]] = None,
                deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
                enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
                enable_queue_purging: typing.Optional[builtins.bool] = None,
                encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
                encryption_key_props: typing.Optional[typing.Union[aws_cdk.aws_kms.KeyProps, typing.Dict[str, typing.Any]]] = None,
                event_bus_props: typing.Optional[typing.Union[aws_cdk.aws_events.EventBusProps, typing.Dict[str, typing.Any]]] = None,
                existing_event_bus_interface: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
                existing_queue_obj: typing.Optional[aws_cdk.aws_sqs.Queue] = None,
                max_receive_count: typing.Optional[jsii.Number] = None,
                queue_props: typing.Optional[typing.Union[aws_cdk.aws_sqs.QueueProps, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EventsRuleToSqsProps(
            event_rule_props=event_rule_props,
            dead_letter_queue_props=dead_letter_queue_props,
            deploy_dead_letter_queue=deploy_dead_letter_queue,
            enable_encryption_with_customer_managed_key=enable_encryption_with_customer_managed_key,
            enable_queue_purging=enable_queue_purging,
            encryption_key=encryption_key,
            encryption_key_props=encryption_key_props,
            event_bus_props=event_bus_props,
            existing_event_bus_interface=existing_event_bus_interface,
            existing_queue_obj=existing_queue_obj,
            max_receive_count=max_receive_count,
            queue_props=queue_props,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="eventsRule")
    def events_rule(self) -> aws_cdk.aws_events.Rule:
        return typing.cast(aws_cdk.aws_events.Rule, jsii.get(self, "eventsRule"))

    @builtins.property
    @jsii.member(jsii_name="sqsQueue")
    def sqs_queue(self) -> aws_cdk.aws_sqs.Queue:
        return typing.cast(aws_cdk.aws_sqs.Queue, jsii.get(self, "sqsQueue"))

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(self) -> typing.Optional[aws_cdk.aws_sqs.DeadLetterQueue]:
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.DeadLetterQueue], jsii.get(self, "deadLetterQueue"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="eventBus")
    def event_bus(self) -> typing.Optional[aws_cdk.aws_events.IEventBus]:
        return typing.cast(typing.Optional[aws_cdk.aws_events.IEventBus], jsii.get(self, "eventBus"))


@jsii.data_type(
    jsii_type="@aws-solutions-constructs/aws-events-rule-sqs.EventsRuleToSqsProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_rule_props": "eventRuleProps",
        "dead_letter_queue_props": "deadLetterQueueProps",
        "deploy_dead_letter_queue": "deployDeadLetterQueue",
        "enable_encryption_with_customer_managed_key": "enableEncryptionWithCustomerManagedKey",
        "enable_queue_purging": "enableQueuePurging",
        "encryption_key": "encryptionKey",
        "encryption_key_props": "encryptionKeyProps",
        "event_bus_props": "eventBusProps",
        "existing_event_bus_interface": "existingEventBusInterface",
        "existing_queue_obj": "existingQueueObj",
        "max_receive_count": "maxReceiveCount",
        "queue_props": "queueProps",
    },
)
class EventsRuleToSqsProps:
    def __init__(
        self,
        *,
        event_rule_props: typing.Union[aws_cdk.aws_events.RuleProps, typing.Dict[str, typing.Any]],
        dead_letter_queue_props: typing.Optional[typing.Union[aws_cdk.aws_sqs.QueueProps, typing.Dict[str, typing.Any]]] = None,
        deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
        enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
        enable_queue_purging: typing.Optional[builtins.bool] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
        encryption_key_props: typing.Optional[typing.Union[aws_cdk.aws_kms.KeyProps, typing.Dict[str, typing.Any]]] = None,
        event_bus_props: typing.Optional[typing.Union[aws_cdk.aws_events.EventBusProps, typing.Dict[str, typing.Any]]] = None,
        existing_event_bus_interface: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
        existing_queue_obj: typing.Optional[aws_cdk.aws_sqs.Queue] = None,
        max_receive_count: typing.Optional[jsii.Number] = None,
        queue_props: typing.Optional[typing.Union[aws_cdk.aws_sqs.QueueProps, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param dead_letter_queue_props: Optional user provided properties for the dead letter queue. Default: - Default props are used
        :param deploy_dead_letter_queue: Whether to deploy a secondary queue to be used as a dead letter queue. Default: - true.
        :param enable_encryption_with_customer_managed_key: Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct. Default: - true (encryption enabled, managed by this CDK app).
        :param enable_queue_purging: Whether to grant additional permissions to the Lambda function enabling it to purge the SQS queue. Default: - "false", disabled by default.
        :param encryption_key: An optional, imported encryption key to encrypt the SQS queue, and SNS Topic. Default: - not specified.
        :param encryption_key_props: Optional user-provided props to override the default props for the encryption key. Default: - Default props are used.
        :param event_bus_props: A new custom EventBus is created with provided props. Default: - None
        :param existing_event_bus_interface: Existing instance of a custom EventBus. Default: - None
        :param existing_queue_obj: Existing instance of SQS queue object, providing both this and queueProps will cause an error. Default: - None
        :param max_receive_count: The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue. Default: - required field if deployDeadLetterQueue=true.
        :param queue_props: User provided props to override the default props for the SQS queue. Default: - Default props are used

        :summary: The properties for the EventsRuleToSqs Construct
        '''
        if isinstance(event_rule_props, dict):
            event_rule_props = aws_cdk.aws_events.RuleProps(**event_rule_props)
        if isinstance(dead_letter_queue_props, dict):
            dead_letter_queue_props = aws_cdk.aws_sqs.QueueProps(**dead_letter_queue_props)
        if isinstance(encryption_key_props, dict):
            encryption_key_props = aws_cdk.aws_kms.KeyProps(**encryption_key_props)
        if isinstance(event_bus_props, dict):
            event_bus_props = aws_cdk.aws_events.EventBusProps(**event_bus_props)
        if isinstance(queue_props, dict):
            queue_props = aws_cdk.aws_sqs.QueueProps(**queue_props)
        if __debug__:
            def stub(
                *,
                event_rule_props: typing.Union[aws_cdk.aws_events.RuleProps, typing.Dict[str, typing.Any]],
                dead_letter_queue_props: typing.Optional[typing.Union[aws_cdk.aws_sqs.QueueProps, typing.Dict[str, typing.Any]]] = None,
                deploy_dead_letter_queue: typing.Optional[builtins.bool] = None,
                enable_encryption_with_customer_managed_key: typing.Optional[builtins.bool] = None,
                enable_queue_purging: typing.Optional[builtins.bool] = None,
                encryption_key: typing.Optional[aws_cdk.aws_kms.Key] = None,
                encryption_key_props: typing.Optional[typing.Union[aws_cdk.aws_kms.KeyProps, typing.Dict[str, typing.Any]]] = None,
                event_bus_props: typing.Optional[typing.Union[aws_cdk.aws_events.EventBusProps, typing.Dict[str, typing.Any]]] = None,
                existing_event_bus_interface: typing.Optional[aws_cdk.aws_events.IEventBus] = None,
                existing_queue_obj: typing.Optional[aws_cdk.aws_sqs.Queue] = None,
                max_receive_count: typing.Optional[jsii.Number] = None,
                queue_props: typing.Optional[typing.Union[aws_cdk.aws_sqs.QueueProps, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument event_rule_props", value=event_rule_props, expected_type=type_hints["event_rule_props"])
            check_type(argname="argument dead_letter_queue_props", value=dead_letter_queue_props, expected_type=type_hints["dead_letter_queue_props"])
            check_type(argname="argument deploy_dead_letter_queue", value=deploy_dead_letter_queue, expected_type=type_hints["deploy_dead_letter_queue"])
            check_type(argname="argument enable_encryption_with_customer_managed_key", value=enable_encryption_with_customer_managed_key, expected_type=type_hints["enable_encryption_with_customer_managed_key"])
            check_type(argname="argument enable_queue_purging", value=enable_queue_purging, expected_type=type_hints["enable_queue_purging"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument encryption_key_props", value=encryption_key_props, expected_type=type_hints["encryption_key_props"])
            check_type(argname="argument event_bus_props", value=event_bus_props, expected_type=type_hints["event_bus_props"])
            check_type(argname="argument existing_event_bus_interface", value=existing_event_bus_interface, expected_type=type_hints["existing_event_bus_interface"])
            check_type(argname="argument existing_queue_obj", value=existing_queue_obj, expected_type=type_hints["existing_queue_obj"])
            check_type(argname="argument max_receive_count", value=max_receive_count, expected_type=type_hints["max_receive_count"])
            check_type(argname="argument queue_props", value=queue_props, expected_type=type_hints["queue_props"])
        self._values: typing.Dict[str, typing.Any] = {
            "event_rule_props": event_rule_props,
        }
        if dead_letter_queue_props is not None:
            self._values["dead_letter_queue_props"] = dead_letter_queue_props
        if deploy_dead_letter_queue is not None:
            self._values["deploy_dead_letter_queue"] = deploy_dead_letter_queue
        if enable_encryption_with_customer_managed_key is not None:
            self._values["enable_encryption_with_customer_managed_key"] = enable_encryption_with_customer_managed_key
        if enable_queue_purging is not None:
            self._values["enable_queue_purging"] = enable_queue_purging
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if encryption_key_props is not None:
            self._values["encryption_key_props"] = encryption_key_props
        if event_bus_props is not None:
            self._values["event_bus_props"] = event_bus_props
        if existing_event_bus_interface is not None:
            self._values["existing_event_bus_interface"] = existing_event_bus_interface
        if existing_queue_obj is not None:
            self._values["existing_queue_obj"] = existing_queue_obj
        if max_receive_count is not None:
            self._values["max_receive_count"] = max_receive_count
        if queue_props is not None:
            self._values["queue_props"] = queue_props

    @builtins.property
    def event_rule_props(self) -> aws_cdk.aws_events.RuleProps:
        '''User provided eventRuleProps to override the defaults.

        :default: - None
        '''
        result = self._values.get("event_rule_props")
        assert result is not None, "Required property 'event_rule_props' is missing"
        return typing.cast(aws_cdk.aws_events.RuleProps, result)

    @builtins.property
    def dead_letter_queue_props(self) -> typing.Optional[aws_cdk.aws_sqs.QueueProps]:
        '''Optional user provided properties for the dead letter queue.

        :default: - Default props are used
        '''
        result = self._values.get("dead_letter_queue_props")
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.QueueProps], result)

    @builtins.property
    def deploy_dead_letter_queue(self) -> typing.Optional[builtins.bool]:
        '''Whether to deploy a secondary queue to be used as a dead letter queue.

        :default: - true.
        '''
        result = self._values.get("deploy_dead_letter_queue")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_encryption_with_customer_managed_key(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''Use a KMS Key, either managed by this CDK app, or imported.

        If importing an encryption key, it must be specified in
        the encryptionKey property for this construct.

        :default: - true (encryption enabled, managed by this CDK app).
        '''
        result = self._values.get("enable_encryption_with_customer_managed_key")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_queue_purging(self) -> typing.Optional[builtins.bool]:
        '''Whether to grant additional permissions to the Lambda function enabling it to purge the SQS queue.

        :default: - "false", disabled by default.
        '''
        result = self._values.get("enable_queue_purging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.Key]:
        '''An optional, imported encryption key to encrypt the SQS queue, and SNS Topic.

        :default: - not specified.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.Key], result)

    @builtins.property
    def encryption_key_props(self) -> typing.Optional[aws_cdk.aws_kms.KeyProps]:
        '''Optional user-provided props to override the default props for the encryption key.

        :default: - Default props are used.
        '''
        result = self._values.get("encryption_key_props")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.KeyProps], result)

    @builtins.property
    def event_bus_props(self) -> typing.Optional[aws_cdk.aws_events.EventBusProps]:
        '''A new custom EventBus is created with provided props.

        :default: - None
        '''
        result = self._values.get("event_bus_props")
        return typing.cast(typing.Optional[aws_cdk.aws_events.EventBusProps], result)

    @builtins.property
    def existing_event_bus_interface(
        self,
    ) -> typing.Optional[aws_cdk.aws_events.IEventBus]:
        '''Existing instance of a custom EventBus.

        :default: - None
        '''
        result = self._values.get("existing_event_bus_interface")
        return typing.cast(typing.Optional[aws_cdk.aws_events.IEventBus], result)

    @builtins.property
    def existing_queue_obj(self) -> typing.Optional[aws_cdk.aws_sqs.Queue]:
        '''Existing instance of SQS queue object, providing both this and queueProps will cause an error.

        :default: - None
        '''
        result = self._values.get("existing_queue_obj")
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.Queue], result)

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        '''The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue.

        :default: - required field if deployDeadLetterQueue=true.
        '''
        result = self._values.get("max_receive_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue_props(self) -> typing.Optional[aws_cdk.aws_sqs.QueueProps]:
        '''User provided props to override the default props for the SQS queue.

        :default: - Default props are used
        '''
        result = self._values.get("queue_props")
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.QueueProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventsRuleToSqsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EventsRuleToSqs",
    "EventsRuleToSqsProps",
]

publication.publish()