param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $Args
)

& "$PSScriptRoot\.venv\Scripts\python.exe" "$PSScriptRoot\manage.py" @Args
