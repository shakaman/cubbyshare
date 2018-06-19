# cubbyshare

Simple, Platform.sh powered, application to share secrets that can be viewed only once

## Setup

### Platform.sh

Create Platform.sh project.

Push code.

On master, create variable `env:VAULT_URI` with the URI to the Vault app within the same project (drop the trailing `/`).

### Run locally

```
virtualenv .env
source .env/bin/activate
pip install -r frontend/requirements.txt
FLASK_ENV=development FLASK_APP=frontend/__init__.py flask run --with-threads -h 0.0.0.0 -p 8888
```

You will be able to access the frontend on [localhost:8888](http://localhost:8888/).
