## Install packages (general)
```powershell
$VERSION="3.12";
$ENV_NAME="azagents";
$ENV_SURFIX="pip";

$ENV_FULL_NAME = "$ENV_NAME$VERSION$ENV_SURFIX";
# with the closing "\"
$ENV_DIR="$env:USERPROFILE\Documents\VENV\";

# absolute path of requirements.txt to install for the python venv
$PROJ_DIR="$env:USERPROFILE\Documents\VCS\democollections\AI-Agent-Workshop-2025";
# $SubProj="\"
$SubProj=""
$PackageFile="$PROJ_DIR\${SubProj}requirements.txt";

& "$ENV_DIR$ENV_FULL_NAME\Scripts\Activate.ps1";
Invoke-Expression "(Get-Command python).Source";

& "python" -m pip install --upgrade pip;
& "python" -m pip install -r $PackageFile --no-cache-dir;

deactivate
```

## (Optional) remove all the packages
For the venv python
```powershell
# which python powershell equivalent
Invoke-Expression "(Get-Command python).Source";
& "python" -m pip freeze | %{$_.split('==')} | %{python -m pip uninstall -y $_};
& "python" -m pip list;
```