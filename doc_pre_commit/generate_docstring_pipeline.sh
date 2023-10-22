#!/bin/bash

python doc_pre_commit/generate_docstring.py $(git diff --name-only $CI_COMMIT_BEFORE_SHA $CI_COMMIT_SHA);
git add .;
git commit -m "Update Docs by ${CI_RUNNER_ID}";
git push -o ci.skip "https://whatever:${PUSH_TOKEN}@${CI_REPOSITORY_URL#*@}"