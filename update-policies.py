import argparse
import os

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
        '  value = "{}"',
        '}}',
        ''
    ])
    outputs = []
    arn2name = dict()

    for policy in policies:
        arn2name[policy['Arn']] = policy['PolicyName']

    for arn in sorted(arn2name.keys()):
        name = arn2name[arn]
        outputs.append(template.format(name, arn))

    return outputs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--profile', default='default', help='AWS named profile.')
    args = parser.parse_args()
    os.environ.setdefault('AWS_PROFILE', args.profile)

    policies = get_managed_policies()
    outputs = format_policies(policies)
    print('\n'.join(outputs))
