#define MyAppName "vocal"
#define MyAppVersion "1.5.2"
#define MyAppPublisher "NASA DEVELOP"
#define MyAppURL "http://www.example.com/"
#define MyAppExeName "Calipso.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{454CC175-D5EC-41C8-9E3F-580334AFB49F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DisableProgramGroupPage=yes
; NOTE: CHANGE PATHS TO OUTPUT LOCATION OF YOUR CHOICE
OutputDir=C:\Users\Grant\Documents\Inno Setup Examples Output
OutputBaseFilename=vocal_setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

; NOTE: CHANGE PATHS TO YOUR LOCATION OF VOCAL BUILD
[Files]
Source: "C:\Users\Grant\Documents\vocal\core\Calipso.exe"; DestDir: "{app}\core"; Flags: ignoreversion
Source: "C:\Users\Grant\Documents\vocal\dat\*"; DestDir: "{localappdata}\vocal\dat"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Grant\Documents\vocal\db\*"; DestDir: "{localappdata}\vocal\db"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Grant\Documents\vocal\log\*"; DestDir: "{localappdata}\vocal\fakedir\log"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Grant\Documents\vocal\ico\*"; DestDir: "{localappdata}\vocal\fakedir\ico"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Grant\Documents\vocal\dat_\*"; DestDir: "{localappdata}\vocal\fakedir\dat"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Grant\Documents\vocal\core\*"; DestDir: "{app}\core"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\core\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\core\{#MyAppExeName}"; Tasks: desktopicon
