set shell := ["powershell.exe", "-NoProfile", "-Command"]
    
generate-models:
    datamodel-codegen --input ./schemas/openapi.yaml --output ./app/models/models_auto.py --force

generate-grpc:
    python -m grpc_tools.protoc -Iapp/protos --python_out=app/grpc_package --grpc_python_out=app/grpc_package schemas/med_schedule.proto
