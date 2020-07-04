#!/bin/sh

# only meant to be used if no commits after the bump commit are present
CURRENT_VERSION=$(bumpversion --dry-run --allow-dirty --list "${PART}" | grep '^current_version' | sed -r s,"^.*=",,)

echo "Going back one commit (soft reset)"
# undoes one commit
# don't use hard reset because it will delete non tracked changes
# and you don't want that,
git reset --soft HEAD^1

echo "Undoing changes to specific files"
FILES="VERSION CHANGELOG.md .bumpversion.cfg"
git reset HEAD "${FILES}"
git checkout -- "${FILES}"

echo "Deleting local tag=v{CURRENT_VERSION}.\nMake sure to delete any remote tags manually, if present."
git tag --delete "v${CURRENT_VERSION}"

echo "Done"
