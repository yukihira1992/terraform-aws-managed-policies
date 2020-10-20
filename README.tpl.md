# terraform-aws-managed-policies

## Usage

```hcl-terraform
module "managed-policies" {
  source = "yukihira1992/managed-policies/aws"
}

data "aws_iam_policy" "ec2_full_access" {
  arn = module.managed-policies.AmazonEC2FullAccess
}
```

## Outputs

