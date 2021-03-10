set -euxo pipefail

pytest

poetry version ${1-prerelease}

VERSION=$(poetry version | sed 's/opennempy\ //g')

echo "Building version $VERSION"

poetry export --format requirements.txt > requirements.txt
poetry export --format requirements.txt --dev > requirements-dev.txt

git add pyproject.toml requirements.txt

git ci -m "v$VERSION"

git tag v$VERSION
git push -u origin master v$VERSION


poetry build

twine upload --skip-existing dist/*

rm -rf build