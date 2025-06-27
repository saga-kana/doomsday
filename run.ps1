param (
	[int]$N = 10
)

for ($i = 1; $i -le $N; $i++) {
	if ($i -ne 1 ) { $formatted = $i.ToString("00") } else { $formatted = 1}
	
	Start-Process -FilePath 'C:\Program Files\Sandboxie-Plus\Start.exe' -ArgumentList "/box:dd$formatted", "C:\Program Files (x86)\Doomsday\Launcher_1.0.30\Launcher.exe"
	Start-Sleep 20
}