# Colour clusters API

Rest API that returns a list of the main colours of an image calculated using clustering. Colours can optionally be stored in a database with a datetime stamp. 

## Development server

```bash
pipenv run uvicorn main:app --reload
```

## Deployment

```bash
AWS_PROFILE=my-profile sls create_domain # Only required once
AWS_PROFILE=my-profile sls deploy
```
