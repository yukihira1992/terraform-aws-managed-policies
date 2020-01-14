#!/bin/bash

if [[ -n "$(git status --porcelain)" ]]; then
    git remote set-url origin https://yukihira1992:${GITHUB_TOKEN}@github.com/yukihira1992/terraform-aws-managed-policies.git
    git config --local user.name "yukihira1992"
    git config --local user.email "ykhr0130@gmail.com"
    python next_patch.py `cat version.txt` > version.txt
    git add outputs.tf
    git add version.txt
    NEW_VERSION=`cat version.txt`
    git commit -m "Updated policies and bumped version ${NEW_VERSION}."
    git tag v${NEW_VERSION}
    git push origin HEAD --tags
fi
