$parent_directory = Split-Path -Path (Get-Location) -Leaf -Resolve
$target_subfolder = Split-Path -Path ".\$parent_directory" -Leaf -Resolve

if ( Test-Path .\$target_subfolder)
{
    Compress-Archive -Force -Path .\$target_subfolder -Destination .\$target_subfolder.zip
} 