$ProfilePath = $PROFILE.CurrentUserAllHosts
$ProfileDir = Split-Path $ProfilePath -Parent

# Create directory if it doesn't exist
if (!(Test-Path $ProfileDir)) {
    New-Item -Path $ProfileDir -ItemType Directory -Force | Out-Null
}

# Create profile if it doesn't exist
if (!(Test-Path $ProfilePath)) {
    New-Item -Path $ProfilePath -ItemType File -Force | Out-Null
}

$AutoActivateBlock = @'

# Auto-activate Python venv
function Invoke-AutoActivate {
    $venvPath = Join-Path (Get-Location) "venv"
    $dotVenvPath = Join-Path (Get-Location) ".venv"
    
    if (Test-Path "$venvPath\Scripts\Activate.ps1") {
        if ($env:VIRTUAL_ENV -ne $venvPath) {
            Write-Host "Auto-activating venv..." -ForegroundColor Green
            & "$venvPath\Scripts\Activate.ps1"
        }
    } elseif (Test-Path "$dotVenvPath\Scripts\Activate.ps1") {
        if ($env:VIRTUAL_ENV -ne $dotVenvPath) {
            Write-Host "Auto-activating .venv..." -ForegroundColor Green
            & "$dotVenvPath\Scripts\Activate.ps1"
        }
    }
}

# Hook into prompt to check on every command/location change
# Note: appending to existing prompt function is minimal for demo
$oldPrompt = Get-Command prompt -ErrorAction SilentlyContinue
if ($oldPrompt) {
    # If prompt exists, we wrap it (simplified approach, usually just redefining is safer for simple profiles)
    # For now, we'll just define a new one that calls the logic
}

function prompt {
    Invoke-AutoActivate
    "PS " + $(Get-Location) + "> "
}
'@

Add-Content -Path $ProfilePath -Value $AutoActivateBlock
Write-Host "PowerShell profile updated at $ProfilePath"
