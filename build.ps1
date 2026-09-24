$startTime = Get-Date

python -m venv venv
.\venv\Scripts\Activate.ps1
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pip install nuitka==4.2.1

Set-Content -Path ".\buildtime.py" -Value "buildTime = '$(Get-Date -Format 'yyyyMMdd_HHmmss')'" -Encoding UTF8

nuitka --standalone --remove-output --windows-console-mode=disable `
--windows-icon-from-ico=.\icon.ico --include-data-file=.\icon.ico=.\ `
--output-dir=dist --output-filename=tray-force-show_win_amd64 `
.\tray-force-show.py

$endTime = Get-Date
$elapsedTime = New-TimeSpan -Start $startTime -End $endTime
Write-Output "程序构建用时：$($elapsedTime.TotalSeconds) 秒"