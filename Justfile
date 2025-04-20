set shell := ["powershell.exe", "-NoProfile", "-Command"]
    
generate-models:
    datamodel-codegen --input ./schemas/openapi.yaml --output ./app/models_auto.py --force

# generate-client:
#     openapi-python-client generate --path ./schemas/openapi.yaml --output-path api_client --overwrite
