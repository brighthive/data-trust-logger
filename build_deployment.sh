ORGANIZATION=brighthive
IMAGE_NAME=data-trust-logger
VERSION=1.0.1
AWS_ECR_REPO=396527728813.dkr.ecr.us-east-2.amazonaws.com

docker build -t $ORGANIZATION/$IMAGE_NAME:$VERSION -f Dockerfile .

$(aws ecr get-login --no-include-email --region us-east-2)
docker tag $ORGANIZATION/$IMAGE_NAME:$VERSION $AWS_ECR_REPO/$ORGANIZATION/$IMAGE_NAME:$VERSION
docker tag $ORGANIZATION/$IMAGE_NAME:$VERSION $AWS_ECR_REPO/$ORGANIZATION/$IMAGE_NAME:latest
docker push $AWS_ECR_REPO/$ORGANIZATION/$IMAGE_NAME:$VERSION
docker push $AWS_ECR_REPO/$ORGANIZATION/$IMAGE_NAME:latest