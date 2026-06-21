$path = "C:\Users\User\.claude\projects\C--Users-User-Desktop-realestate-ai-team-main-realestate-ai-team-main\8fabd079-5023-41f4-a94d-9f060159d7a3\tool-results\mcp-c75dc3cd-3c98-4040-acae-4b282365cb2c-get_thread-1781615588091.txt"
$j = Get-Content -Raw $path | ConvertFrom-Json
$m = $j.messages | Where-Object { $_.id -eq "19ecef40658ac9ff" }
$m.date
$m.sender
$m.subject
$m.body
