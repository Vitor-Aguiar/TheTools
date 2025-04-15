# Define input and output files
$ComputerList = Get-Content "computers.txt"
$OutputFile = "output-shares.txt"

# Clear the output file if it exists
if (Test-Path $OutputFile) { Remove-Item $OutputFile }

# Loop through each computer
foreach ($Computer in $ComputerList) {
    Write-Host "Scanning $Computer..."
    Add-Content -Path $OutputFile -Value "Checking shares on $Computer:"

    # Get the shared folders
    $Shares = net view \\$Computer 2>&1 | Select-String "Disk" | ForEach-Object { ($_ -split '\s{2,}')[0] }

    # If shares are found, try to get directory listing
    if ($Shares) {
        foreach ($Share in $Shares) {
            $Path = "\\$Computer\$Share"
            Add-Content -Path $OutputFile -Value "`nListing contents of $Path:"

            try {
                $cmdOutput = cmd /c "dir /a `"$Path`"" 2>&1
                Add-Content -Path $OutputFile -Value $cmdOutput
            } catch {
                Add-Content -Path $OutputFile -Value "❌ Failed to list contents of $Path: $_"
            }
        }
    } else {
        Add-Content -Path $OutputFile -Value "⚠️ No shares found or access denied."
    }

    Add-Content -Path $OutputFile -Value "" # Add a blank line for readability
}