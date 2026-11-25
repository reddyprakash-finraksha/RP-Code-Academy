; Inno Setup 6 script for RP Code Academy.  Build:  iscc packaging\installer.iss
#define AppName "RP Code Academy"
#define AppVersion "1.0.0"
#define AppExe "RPCodeAcademy.exe"

[Setup]
AppId={{8F3C2A41-6B7D-4E19-9C55-2D1A7E0B4F63}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=RP Code Academy
DefaultDirName={autopf}\RPCodeAcademy
DefaultGroupName={#AppName}
OutputDir=..\dist
OutputBaseFilename=RPCodeAcademy-Setup-{#AppVersion}
Compression=lzma2/max
SolidCompression=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#AppExe}
WizardStyle=modern
LicenseFile=..\LICENSE.txt

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: checkedonce

[Files]
Source: "..\dist\RPCodeAcademy\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "..\docs\STUDENT_GUIDE.md"; DestDir: "{app}\docs"; Flags: ignoreversion
Source: "..\docs\TEACHER_GUIDE.md"; DestDir: "{app}\docs"; Flags: ignoreversion

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{group}\Teacher Guide"; Filename: "{app}\docs\TEACHER_GUIDE.md"
Name: "{group}\Student Guide"; Filename: "{app}\docs\STUDENT_GUIDE.md"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Student progress lives in %LOCALAPPDATA%\RPCodeAcademy and is intentionally KEPT on uninstall.
Type: filesandordirs; Name: "{app}"
