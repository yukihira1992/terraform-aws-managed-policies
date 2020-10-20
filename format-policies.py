import argparse
import pickle
import re

invalid_chars = re.compile(r'[^0-9A-Za-z_-]')


def format_output_name(policy_name):
    return invalid_chars.sub('_', policy_name)


def arn2url(arn):
    return 'https://console.aws.amazon.com/iam/home?#/policies/{}'.format(arn)


def policies2outputs(policies):
    template = '\n'.join([
        'output "{}" {{',
        '  value       = "{}"',
        '  description = "{}"',
        '}}',
        ''
    ])

    return '\n'.join([
        template.format(
            format_output_name(policy['PolicyName']),
            policy['Arn'],
            arn2url(policy['Arn']),
        )
        for policy in policies
    ])


def policies2readme(policies):
    table = [
        '| Name | Description |',
        '|------|-------------|',
    ]

    table.extend([
        '| {} | {} |'.format(
            format_output_name(policy['PolicyName']),
            arn2url(policy['Arn']),
        )
        for policy in policies
    ])

    return '\n'.join(table)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('policies', help='Pickle dump of policies.')
    parser.add_argument('-t', '--type', dest='type', choices=['outputs.tf', 'README.md'], help='Format type.')
    args = parser.parse_args()

    with open(args.policies, 'rb') as f:
        policies = pickle.load(f)

    if args.type == 'outputs.tf':
        print(policies2outputs(policies))
    elif args.type == 'README.md':
        print(policies2readme(policies))


if __name__ == '__main__':
    main()
