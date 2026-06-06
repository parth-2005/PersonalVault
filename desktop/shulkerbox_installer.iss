#define AppName "ShulkerBox"
#define AppVersion "0.1.0"

[Setup]
AppId={{9E7A7E2A-4C1D-4F28-A0D5-5E3B8A2E3B6A}}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
DefaultDirName={autopf}\ShulkerBox
DefaultGroupName=ShulkerBox
OutputBaseFilename=ShulkerBox-Installer
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=no

[Files]
Source: "dist\ShulkerBox.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\ShulkerBox"; Filename: "{app}\ShulkerBox.exe"
Name: "{autodesktop}\ShulkerBox"; Filename: "{app}\ShulkerBox.exe"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "ShulkerBox"; ValueData: """{app}\ShulkerBox.exe"""; Flags: uninsdeletevalue