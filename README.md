# Running locally:

## Get service account creds:
Download from GCP service account section (in API & Creds, create credentials or download an existing one)
## Getting email token:
1. Remove the entry function header and the decorator above it, all code should run with running main.py, also 
2. pip install poetry
3. poetry shell
4. poetry install
5. python3 main.py
6. Browser will open, then you need to login to the email you want to send the notifications with
7. The token is the token.pickle file generated