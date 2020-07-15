import argparse
import os
import re

import boto3


def get_managed_policies():
    client = boto3.client('iam')
    policies = []
    marker = None
    is_truncated = True
    while is_truncated:
        kwargs = dict(
            Scope='AWS',
            MaxItems=1000,
        )
        if marker is not None:
            kwargs.update(Marker=marker)
        response = client.list_policies(**kwargs)
        policies.extend(response.get('Policies', []))
        is_truncated = response['IsTruncated']
        marker = response.get('Marker', None)
    return policies


def format_policies(policies):
    template = '\n'.join([
        'output "{}" {{',
        '  value       = "{}"',
        '  description = "https://console.aws.amazon.com/iam/home?#/policies/{}"',
        '}}',
        ''
    ])
    invalid_chars = re.compile(r'[^0-9A-Za-z_-]')

    return [
        template.format(
            invalid_chars.sub('_', policy['PolicyName']),
            policy['Arn'],
            policy['Arn'],
        )
        for policy in policies
    ]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--profile', help='AWS named profile.')
    args = parser.parse_args()
    if args.profile is not None:
        os.environ.setdefault('AWS_PROFILE', args.profile)

    policies = get_managed_policies()
    outputs = format_policies(policies)
    print('\n'.join(outputs))
