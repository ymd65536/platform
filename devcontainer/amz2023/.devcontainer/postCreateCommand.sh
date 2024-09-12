export STAGE=dev
pip config set install.user 'false'
python -m pip install --index-url https://pypi.org/simple --user build twine setuptools==70.3.0
pip config set global.index-url https://pypi.org/simple
python -m build
ls -l dist
export AWS_DOMAIN="$STAGE-ca" && echo $AWS_DOMAIN
export REPOSITORY_NAME="$STAGE-sample-lib"
export AWS_ACCOUNT_ID=`aws sts get-caller-identity --query 'Account' --output text` && echo $AWS_ACCOUNT_ID
export AWS_DEFAULT_REGION="ap-northeast-1" && echo $AWS_DEFAULT_REGION
python --version
python -m build --version
twine --version
pip --version
