$computers = Get-ADComputer -Filter * | Select-Object -ExpandProperty DNSHostName

foreach ($computer in $computers) {
    if (Test-NetConnection $computer -Port 2701 -InformationLevel Quiet) {
        "$computer : ConfigMgr Remote Control port OPEN"
    }
}
