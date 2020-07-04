#!/bin/sh

# fetch new version
NEW_VERSION=$(bumpversion --dry-run --allow-dirty --list "${PART}" | grep '^new_version' | sed -r s,"^.*=",,)

# creates an unreleased version header
# see <https://github.com/vaab/gitchangelog/issues/94>
UNRELEASED_VERSION_HEADER="v${NEW_VERSION} ($(date +%Y-%m-%d))"
gitchangelog | sed -r "s/%%unreleased_version%%/${UNRELEASED_VERSION_HEADER}/g"
