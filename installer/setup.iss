[Setup]
AppName=Save The World Claimer
AppVersion=1.15.0
AppPublisher=PRO100KatYT
AppPublisherURL=https://github.com/PRO100KatYT/SaveTheWorldClaimer
AppSupportURL=https://github.com/PRO100KatYT/SaveTheWorldClaimer/issues
AppUpdatesURL=https://github.com/PRO100KatYT/SaveTheWorldClaimer/releases
DefaultDirName={autopf}\SaveTheWorldClaimer
DefaultGroupName=Save The World Claimer
UninstallDisplayIcon={app}\SaveTheWorldClaimer.exe
SetupIconFile=..\icons\penny.ico
OutputDir=installer_output
OutputBaseFilename=Setup_SaveTheWorldClaimer
Compression=lzma2
SolidCompression=yes
LicenseFile=..\LICENSE
ShowLanguageDialog=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"

[CustomMessages]
english.LaunchProgram=Launch Save The World Claimer
polish.LaunchProgram=Uruchom Save The World Claimer

english.RemoveConfigPrompt=Do you also want to remove your saved accounts (auth.json) and configuration files?
polish.RemoveConfigPrompt=Czy chcesz usunąć również zapisane konta (auth.json) i pliki konfiguracyjne?

[Dirs]
Name: "{app}"; Permissions: users-modify

[Files]
Source: "..\build_nuitka\SaveTheWorldClaimer.dist\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Save The World Claimer"; Filename: "{app}\SaveTheWorldClaimer.exe"
Name: "{autodesktop}\Save The World Claimer"; Filename: "{app}\SaveTheWorldClaimer.exe"

[Run]
Filename: "{app}\SaveTheWorldClaimer.exe"; Description: "{cm:LaunchProgram}"; Flags: postinstall nowait skipifsilent

[Code]
procedure InitializeUninstallProgressForm();
var
  MsgBoxResult: Integer;
begin
  MsgBoxResult := MsgBox(CustomMessage('RemoveConfigPrompt'), mbConfirmation, MB_YESNO);
  
  if MsgBoxResult = idYes then
  begin
    DeleteFile(ExpandConstant('{app}\auth.json'));
    DeleteFile(ExpandConstant('{app}\config.ini'));
    DeleteFile(ExpandConstant('{app}\userConfig.json'));
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    DelTree(ExpandConstant('{app}\*'), True, True, True);
    RemoveDir(ExpandConstant('{app}'));
  end;
end;
