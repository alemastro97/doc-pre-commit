# Auto-generate Documentation Pre-commit Hook and GitLab Pipeline

This repository provides a pre-commit hook and GitLab pipeline configuration for auto-generating documentation for your Python project.

## Installation

1. Install the Pre-Commit Package:

   ```bash
   pip install pre-commit
   ```

## Usage as a Pre-commit Hook
Once you've installed the pre-commit hook, it will automatically run before each commit. It will generate documentation based on your project's source code and update it as necessary.

You only need to create a ```.pre-commit-config.yaml``` and paste this code inside:

``` yaml
repos:
-   repo: https://github.com/alemastro97/doc-pre-commit/
    rev: v2.0.0
    hooks:
    -   id: generate-docstring
        args: [--api-key=<api-key>]
```
Remember to replace the \<api-key\> with your Openai Api key.  

## Usage in GitLab Pipeline
In this case you need to setup the GitLab environment in order to have all the necessary information to run the pipeline in the correct way.
Add as Environmental Variable of the CI this two variables:
- PUSH_TOKEN: is an access token generated for the project with **write_repository** privileges and **owner/maintainer** as user type
- OPENAI_API_KEY: your OpenAI Api Key
This is the code to add to your ```.gitlab-ci.yml``` to run the pipeline that generates docs over your updated files
```yaml
stages:
  - Docs


before_script:
  - apt-get update
  - apt-get install -y python3-venv
  - python3 -m venv venv
  - source venv/bin/activate
  - python -m pip install --upgrade pip
  - pip install openai astor

doc_generation:
  stage: Docs
  script:
    - git config --global user.name "GitLab Runner Bot"
    - git config --global user.email "gitlab-runner-bot@example.net"
    - git checkout ${CI_COMMIT_REF_NAME}
    - git clone https://github.com/alemastro97/doc-pre-commit.git pre_commit_docs
    - python pre_commit_docs/doc_pre_commit/generate_docstring.py $(git diff --name-only $CI_COMMIT_BEFORE_SHA $CI_COMMIT_SHA)
    - rm -rf pre_commit_docs
    - git status
    - git add .
    - git commit -m "Update Docs by ${CI_RUNNER_ID}"
    - git push -o ci.skip https://whatever:${PUSH_TOKEN}@${CI_REPOSITORY_URL#*@}


```
