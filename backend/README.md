# cic-infocommons
This repository contains the CIC Django project which includes the following apps:
1. CIC RESTful APIs
2. PI Survey form

Frameworks/Libraries used include:
1. [`{json:api}`](https://jsonapi.org/format/) specification for request and response formats.
2. [OpenAPI Specification (OAS)](https://github.com/OAI/OpenAPI-Specification/blob/main/README.md) for modeling and documenting the REST APIs.
3. [Django REST framework](https://www.django-rest-framework.org/) as the web framework.
4. [Django REST frameworkJSON:API](https://django-rest-framework-json-api.readthedocs.io/en/stable/index.html) for formatting request and response using json:api specification. 

## CIC RESTful APIs
### Local (dev) Setup
Clone the repository:
```sh
$ git clone https://github.com/columbia-it/covid-infocommons.git
$ cd covid-infocommons
```
Create a virtual environment to install dependencies in and activate it:
```sh
$ python3 -m venv venv
$ source venv/bin/activate
```
Then install the dependencies:
```sh
(venv)$ pip install -r requirements.txt
```
Once the dependencies are successfully installed, update the database connection information (leave it as it is for default sqllite3 DB) by editing **DATABASES** section in `cic->settings.py`.
To create or update your local/dev DB schema, run the (Django) makemigrations and migrate command: 
```sh
(venv)$ python manage.py makemigrations
(venv)$ python manage.py migrate
```
* *makemigrations* creats new migrations based on the changes you have made to your models.
* *migrate* is for applying and unapplying migrations.

### Generating a static schema document
To generate a YAML schema document:
```sh
(venv)$ python manage.py generateschema --generator_class apis.schemas.SchemaGenerator --file docs/schemas/openapi.yaml
```
If you want a JSON schema document:
```sh
(venv)$ python manage.py generateschema --generator_class apis.schemas.SchemaGenerator --format openapi-json --file docs/schemas/openapi.json
```
Use the schema with swagger-ui

You can try out your static schema document with swagger-ui-watcher: Install it with pip install swagger-ui-watcher -g and then use swagger-ui-watcher -p 8080 docs/schemas/openapi.yaml to open the schema document in your browser.

Run the server:
```sh
(venv)$ python manage.py runserver
```

REST APIs URL: `http://127.0.0.1:8000/v1`

Swagger UI for REST API URL: `http://127.0.0.1:8000/v1/swagger-ui`


### Deploy this application to AWS
This Django application is also configured to run in Lambda on AWS. 
[Zappa](https://github.com/zappa/Zappa) is used to build and deploy serverless on AWS Lambda + API Gateway.

To build and deploy to AWS from your workstation, first install zappa:
```sh
(venv)$ pip install zappa
```

Before deploying to Lambda, you have to assume the AWS IAM role (created by DevOps) using your UNI. This can be done by running `saml.py` which has some pre-requirements.

- Download the appropriate chromedriver executable for your operating system from https://chromedriver.chromium.org/downloads
- Put the executable in PATH and set AWS_PROFILE envrionment variable
```sh
export PATH=$PATH:<path to chromedriver>
export AWS_PROFILE=<aws profile name>
(venv)$ pip install selenium boto3
```
- Tell Django to look for static files in location specified in STATIC_ROOT settings.
```sh
 (venv)$ python manage.py collectstatic 
```
- Run `saml.py` to assume role. Running this command will launch Chrome and prompts CAS login
```sh
 (venv)$ python saml.py <role name> <aws account number> 
```
- Once the role has been assumed, verify that you are using the correct AWS account:
```sh
$ aws sts get-caller-identity
```
Finally, deploy to Lambda:
```sh
(venv)$ zappa update dev
```
If you need to update DB schema prior to deploying, it can be done via zappa:
```sh
(venv)$ $ zappa manage <stage> migrate
(venv)$ zappa manage <stage> migrate
```
