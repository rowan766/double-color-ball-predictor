param(
  [string]$ApiBaseUrl = "http://localhost:8000/api/v1",
  [int]$Days = 365
)

$ErrorActionPreference = "Stop"

$dayEnd = Get-Date -Format "yyyy-MM-dd"
$dayStart = (Get-Date).AddDays(-$Days).ToString("yyyy-MM-dd")
$officialUrl = "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=&issueStart=&issueEnd=&dayStart=$dayStart&dayEnd=$dayEnd&pageNo=1&pageSize=500&week=&systemType=PC"

$headers = @{
  "User-Agent" = "Mozilla/5.0"
  "Referer" = "https://www.cwl.gov.cn/"
}

Write-Host "Fetching SSQ draws from $dayStart to $dayEnd ..."
$response = Invoke-RestMethod -Uri $officialUrl -Method Get -Headers $headers

if (-not $response.result) {
  throw "No draw data returned from official API."
}

$draws = @()
foreach ($row in $response.result) {
  $redNumbers = @()
  foreach ($number in ($row.red -split ",")) {
    $redNumbers += [int]$number
  }
  $drawDate = ([string]$row.date).Substring(0, 10)

  $draws += @{
    issue_no = [string]$row.code
    draw_date = $drawDate
    red_numbers = $redNumbers
    blue_number = [int]$row.blue
    source = "cwl.gov.cn"
  }
}

$draws = $draws | Sort-Object issue_no
$payload = @{
  draws = $draws
  overwrite = $true
} | ConvertTo-Json -Depth 8

Write-Host "Importing $($draws.Count) draws into local backend ..."
$result = Invoke-RestMethod `
  -Uri "$ApiBaseUrl/draws/import" `
  -Method Post `
  -ContentType "application/json" `
  -Body $payload

$result | ConvertTo-Json -Depth 8
