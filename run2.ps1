param (
	[Parameter(ValueFromRemainingArguments=$true)]
	[int[]]$Numbers
)

# for ($i = 0; $i -lt $Numbers.Count; $i++) {
# 	# if ($i -ne 1 ) { $formatted = $i.ToString("00") } else { $formatted = 1}
# 	# Start-Process -FilePath 'C:\Program Files\Sandboxie-Plus\Start.exe' -ArgumentList "/box:dd$formatted", "C:\Program Files (x86)\Doomsday\Launcher_1.0.30\Launcher.exe"


# 	# Start-Sleep 60
# }

foreach ($number in $Numbers) {
	Write-Host "Boot dd$number"
	Start-Process -FilePath 'C:\Program Files\Sandboxie-Plus\Start.exe' -ArgumentList "/box:dd$number", "C:\Program Files (x86)\Doomsday\Launcher_1.0.30\Launcher.exe"
	Start-Sleep 60
}