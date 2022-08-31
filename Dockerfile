FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.9  AS pythonpackages
RUN pip install pipenv
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system --deploy --skip-lock


FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.9  AS runtime
COPY --from=pythonpackages /var/lang/lib/python3.9/site-packages/ /var/lang/lib/python3.9/site-packages/
COPY *.py ./
CMD ["main.handler"]