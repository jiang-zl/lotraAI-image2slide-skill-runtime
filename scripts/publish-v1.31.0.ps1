$ErrorActionPreference = 'Stop'
$entry = Join-Path (Split-Path $PSScriptRoot -Parent) 'tools\publish_release.py'
& py -3 $entry @args
exit $LASTEXITCODE
