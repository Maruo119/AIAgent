@echo off
echo Creating deployment zip...

powershell -Command "& {Get-ChildItem -Path . -Recurse -Exclude @('node_modules', '.git', '__pycache__', '*.log', '.env') | Where-Object { $_.FullName -notlike '*node_modules*' -and $_.FullName -notlike '*.git*' -and $_.FullName -notlike '*__pycache__*' -and $_.FullName -notlike '*.log' -and $_.FullName -notlike '*.env' } | Compress-Archive -DestinationPath app-deploy.zip -Force}"

echo Deployment zip created: app-deploy.zip