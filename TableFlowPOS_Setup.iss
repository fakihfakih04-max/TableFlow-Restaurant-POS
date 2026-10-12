#define MyAppName "TableFlow Restaurant POS"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "TableFlow"
#define MyAppExeName "TableFlowPOS.exe"

[Setup]
AppId={{4C2D7D6A-0B44-4DB9-A7E1-88B0D0C51A9B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\TableFlow Restaurant POS
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=TableFlow_Restaurant_POS_Setup
SetupIconFile=TableFlowPOS.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
PrivilegesRequired=admin
WizardStyle=modern
Compression=lzma2
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: checkedonce

[Files]
Source: "dist\TableFlowPOS\TableFlowPOS.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\TableFlowPOS\TableFlowPrintAgent.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "index.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "TableFlowPOS.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\TableFlowPOS.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\TableFlowPOS.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
