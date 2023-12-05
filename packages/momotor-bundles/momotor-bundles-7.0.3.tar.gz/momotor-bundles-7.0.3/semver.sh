#!/bin/sh

# Configure git
git config --global user.name "semantic-release (via GitlabCI)"
git config --global user.email "tue.gitlab@momotor.org"
git checkout "$CI_COMMIT_REF_NAME"
git status

set -eux

# Bump the version
if [ "$CI_COMMIT_REF_PROTECTED" = "true" ]; then
  semantic-release -v --strict version
  semantic-release -v publish
elif [ "$CI_COMMIT_REF_NAME" = "development" ]; then
  semantic-release -v --strict version --no-changelog --no-commit --build-metadata "dev$(date -d @$(git log -1 --format=%ct) -u +%Y%m%d%H%M%S).$CI_COMMIT_SHORT_SHA"
else
  semantic-release -v --strict version --no-changelog
fi
