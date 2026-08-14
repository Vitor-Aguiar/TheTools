$Ports = @(80, 443, 8000, 8008, 8080, 8081, 8443, 8888)
$TimeoutMs = 5000

$Computers = Get-ADComputer -Filter 'Enabled -eq $true' -Properties DNSHostName |
    Where-Object { $_.DNSHostName } |
    Select-Object -ExpandProperty DNSHostName

$Results = $Computers | ForEach-Object -Parallel {

    $Computer = $_
    $Ports = $using:Ports
    $TimeoutMs = $using:TimeoutMs

    foreach ($Port in $Ports) {

        $TcpClient = [System.Net.Sockets.TcpClient]::new()

        try {
            $Connection = $TcpClient.BeginConnect(
                $Computer,
                $Port,
                $null,
                $null
            )

            if ($Connection.AsyncWaitHandle.WaitOne($TimeoutMs, $false)) {

                try {
                    $TcpClient.EndConnect($Connection)

                    if ($TcpClient.Connected) {
                        [PSCustomObject]@{
                            Computer = $Computer
                            Port     = $Port
                            Status   = "Open"
                        }
                    }
                }
                catch {}
            }
        }
        catch {}

        finally {
            $TcpClient.Dispose()
        }
    }

} -ThrottleLimit 50

$Results |
    Sort-Object Computer, Port |
    Format-Table -AutoSize

$Results |
    Sort-Object Computer, Port |
    Export-Csv ".\AD-Web-Ports.csv" -NoTypeInformation
