import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-solutions-constructs.aws-events-rule-sqs",
    "version": "1.181.1",
    "description": "CDK Constructs for deploying AWS Events Rule that invokes AWS SQS",
    "license": "Apache-2.0",
    "url": "https://github.com/awslabs/aws-solutions-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awslabs/aws-solutions-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_solutions_constructs.aws_events_rule_sqs",
        "aws_solutions_constructs.aws_events_rule_sqs._jsii"
    ],
    "package_data": {
        "aws_solutions_constructs.aws_events_rule_sqs._jsii": [
            "aws-events-rule-sqs@1.181.1.jsii.tgz"
        ],
        "aws_solutions_constructs.aws_events_rule_sqs": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk.aws-events==1.181.1",
        "aws-cdk.aws-iam==1.181.1",
        "aws-cdk.aws-kms==1.181.1",
        "aws-cdk.aws-sqs==1.181.1",
        "aws-cdk.core==1.181.1",
        "aws-solutions-constructs.aws-eventbridge-sqs==1.181.1",
        "aws-solutions-constructs.core==1.181.1",
        "constructs>=3.2.0, <4.0.0",
        "jsii>=1.71.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)