# cubbyshare

Simple, Platform.sh powered, application to share secrets that can be viewed only once

## Setup

Create Platform.sh project.

Push code.

On master, create variable `env:VAULT_URI` with the URI to the Vault app within the same project (drop the trailing `/`).
