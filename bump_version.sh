#!/bin/sh

# how to bump version. See https://pypi.org/project/bumpversion/
# available options by default are
# named "major", "minor", "patch",
PART="${PART:-patch}"

# fetch new version using bumpversion
echo "Fetching current VERSION data"
CURRENT_VERSION=$(bumpversion --dry-run --allow-dirty --list ${PART} | grep '^current_version' | sed -r s,"^.*=",,)
NEW_VERSION=$(bumpversion --dry-run --allow-dirty --list ${PART} | grep '^new_version' | sed -r s,"^.*=",,)

# overwrites CHANGELOG.md
echo "Generating CHANGELOG.md"
PART=${PART} sh ./bump_changelog.sh > CHANGELOG.md

# generate new revisions
echo "Generating new revision files"
bumpversion --allow-dirty --verbose --no-commit --no-tag "${PART}"

# stage changes
echo "Staging files"
git add CHANGELOG.md VERSION .bumpversion.cfg

# commit message
echo "Committing files"
git commit -m "new: dev: bump version v${CURRENT_VERSION} to v${NEW_VERSION} !minor"

# git tag
echo "Tagging new version"
git tag -a "v${NEW_VERSION}" -m "bump version v${NEW_VERSION} from v${CURRENT_VERSION}"
