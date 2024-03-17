FROM public.ecr.aws/lambda/python:3.9

RUN yum upgrade -y

RUN yum update -y

RUN yum clean all

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.
COPY . ${LAMBDA_TASK_ROOT}

COPY requirements.txt  .

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]

# docker build -t scindo_service .
# docker run -d --rm --name scindo_serv -p 9001:8080 scindo_service
# aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 069829654358.dkr.ecr.eu-central-1.amazonaws.com
# aws ecr create-repository --repository-name scindo_service --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
# docker tag  scindo_service 069829654358.dkr.ecr.eu-central-1.amazonaws.com/scindo_service:v1
# docker push 069829654358.dkr.ecr.eu-central-1.amazonaws.com/scindo_service:v1