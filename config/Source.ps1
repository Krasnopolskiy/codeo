$content = Get-Content .\config\.env;
foreach ($line in $content) {
    if ($line.StartsWith("#")) {continue};
    if ($line.Trim()) {
        $line = $line.Replace("`"","")
        $kvp = $line -split "=", 2
        [Environment]::SetEnvironmentVariable($kvp[0].Trim(), $kvp[1].Trim(), "Process")
    }
}
