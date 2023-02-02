# start by pulling the python image
FROM python:3.11

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# RUN apk --update add --no-cache python3-dev gcc libc-dev libffi-dev g++

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

ENV PYTHONUNBUFFERED 1

# # configure the container to run in an executed manner
# ENTRYPOINT [ "python" ]

# CMD ["view.py" ]