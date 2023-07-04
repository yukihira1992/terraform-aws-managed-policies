import argparse
import os
import pickle

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
        fetched_policies = response.get('Policies', [])
        policies.extend([p for p in fetched_policies if p['IsAttachable']])
        is_truncated = response['IsTruncated']
        marker = response.get('Marker', None)
    return policies


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('outfile', help='Output file path.')
    parser.add_argument('-p', '--profile', help='AWS named profile.')
    args = parser.parse_args()
    if args.profile is not None:
        os.environ.setdefault('AWS_PROFILE', args.profile)

    policies = get_managed_policies()
    with open(args.outfile, 'wb') as f:
        pickle.dump(policies, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    main()
