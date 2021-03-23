set -euxo pipefail

# Test
pytest  --exitfirst --verbose --failed-first

# Lint
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# mypy
# mypy opennem

poetry version ${1-prerelease}

VERSION=$(poetry version | sed 's/opennem\ //g')

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
