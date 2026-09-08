# World-Office Editor UI — 100% OnlyOffice Feature-Parity Specification

**Status:** Approved for implementation
**Oracle:** OnlyOffice DocumentServer **9.4.0 build 129** (container `nc-ooh-onlyoffice-1`), WOPI host Nextcloud 34.0.3 + richdocuments 11.1, harness in `~/workspace/nextcloud/` (`docker-compose.yml`, `Caddyfile`, `wopi-flow.md`, `compose/*.sh`)
**Produces:** The World-Office editor UI (`server/opencloud-docserver/web/editor.js` + `web/index.html`) reaching functional and visual parity with the OnlyOffice desktop web editors
**Spec style:** EARS (`### Requirement: … SHALL …` + `#### Scenario: WHEN/THEN/AND`), matching `plan/specs/*/spec.md`

---

## 1. Purpose and Source of Truth

### Requirement: UI-PARITY-PURPOSE — the World-Office editor UI SHALL cover the feature surface of the OnlyOffice Document Server 9.4 desktop web editors

The only honest measure of "100% of OnlyOffice's features" is the deployed build itself. OnlyOffice ships one locale file per editor variant whose keys enumerate every label, tooltip, menu item, dialog, and control in the UI — it is the complete, build-exact inventory of the product's feature surface.

#### Scenario: WHEN a reviewer asks what "100% parity" means
- THEN the answer is the locale-inventory of the oracle build, not a marketing-document claim
- AND the inventory is reconstructed from the live oracle by `generate-inventory.py` (not from memory or docs)

### Requirement: UI-PARITY-ORACLE — the parity oracle SHALL be the OnlyOffice 9.4.0 build 129 web-apps locale set

#### Scenario: WHEN the inventory is generated
- THEN `generate-inventory.py` reads `/var/www/onlyoffice/documentserver/web-apps/apps/<app>/<variant>/locale/en.json` from the oracle container `nc-ooh-onlyoffice-1` for every shipped `<app>` × `<variant>`
- AND `<app>` ∈ `documenteditor`, `spreadsheeteditor`, `presentationeditor`, `pdfeditor`, `visioeditor`
- AND `<variant>` ∈ `main` (desktop editor), `mobile`, `embed`, `forms` (only where shipped)
- AND the output covers 20,193 locale keys organized into 909 component groups across 14 app-variant inventory files under `inventory/`
- AND `inventory/_coverage.json` records, per app-variant, the number of keys and the component-class breakdown

### Requirement: UI-PARITY-TRACEABILITY — the spec SHALL be traceable to the exact oracle build

#### Scenario: WHEN the inventory changes (oracle upgraded, keys added)
- THEN regenerate the inventory with `generate-inventory.py` and re-run `check-coverage.py`
- AND every component class appearing in `inventory/_coverage.json` for any app-variant SHALL appear in this spec as a backticked literal `` `Full.Dotted.Name` ``

---

## 2. Coverage Rule and Mechanical Verification

### Requirement: UI-PARITY-COVERAGE — every UI component class in the oracle inventory SHALL be named in this spec

The coverage rule is mechanical and enforced by `check-coverage.py`:

**Rule (normative):** For every key `k` in every app-variant locale file, the *component class* of `k` is abstracted as the first three dot-segments of `k` for flat, dot-namespaced locale files (e.g. `DE.Views.Toolbar`), and as the first **two** dot-segments for nested section-based locale files (e.g. `Common.Collaboration`); keys with fewer segments group under their first segment. Each such component class MUST appear verbatim in `spec.md` inside backticks. Because components repeat across app-variants, naming a component once covers all the apps that emit it.

#### Scenario: WHEN `check-coverage.py` runs
- THEN it loads `inventory/_coverage.json`, extracts every component class for every app-variant (2,126 component instances across 612 unique classes)
- AND for each unique class it verifies the literal `` `Class.Name` `` occurs in `spec.md`
- AND it prints `OK: 100% component coverage in spec.md` and exits 0
- OR it lists every missing class and exits 1

### Requirement: UI-PARITY-REPRODUCIBILITY — inventory generation SHALL be deterministic and rerunnable

#### Scenario: WHEN a maintainer regenerates the inventory
- THEN `generate-inventory.py` reproduces identical 20,193-key / 909-group totals for the pinned oracle container
- AND the generator fails loudly if the oracle container is unreachable
- AND `_coverage.json` records the source container name

---

## 3. Global Conformance and Application Shell (every editor)

These requirements apply to all five editors. Per-editor chrome is specified in §8–§12.

### Requirement: R-GLOB-SHELL — every editor SHALL present the OnlyOffice application shell: header, left menu, status bar, toolbar, viewport

#### Scenario: WHEN an editor boots
- THEN the shell mounts all `Common.Controllers.*` application controllers: `Common.Controllers.ChartTab`, `Common.Controllers.Chat`, `Common.Controllers.Desktop`, `Common.Controllers.ExternalDiagramEditor`, `Common.Controllers.ExternalLinks`, `Common.Controllers.ExternalMergeEditor`, `Common.Controllers.ExternalOleEditor`, `Common.Controllers.History`, `Common.Controllers.PasteOptions`, `Common.Controllers.Plugins`, `Common.Controllers.ReviewChanges`, `Common.Controllers.Shortcuts`
- AND it provides the `Common.Controllers.Desktop` controller that wires the menu bar, toolbar, and keyboard to the visible canvas
- WHEN the user interacts with any widget
- THEN the full `Common.UI` widget set is available: `Common.UI.ButtonColored`, `Common.UI.Calendar`, `Common.UI.ComboBorderSize`, `Common.UI.ComboBorderSizeEditable`, `Common.UI.ComboDataView`, `Common.UI.ExtendedColorDialog`, `Common.UI.HSBColorPicker`, `Common.UI.InputField`, `Common.UI.InputFieldBtnCalendar`, `Common.UI.InputFieldBtnPassword`, `Common.UI.SearchBar`, `Common.UI.SearchDialog`, `Common.UI.SynchronizeTip`, `Common.UI.ThemeColorPalette`, `Common.UI.Themes`, `Common.UI.Window`
- AND the measurement, string, and color helpers behave identically: `Common.Utils.Metric`, `Common.Utils.String`, `Common.Utils.ThemeColor`

### Requirement: R-GLOB-HEADER — the header SHALL reproduce the OnlyOffice header chrome

#### Scenario: WHEN the document is open in any editor
- THEN the header (covered by `Common.Views.Header`) shows the editor tabs, the file title, the saved-state indicator and the collaborative user avatars
- THEN hover and click affordances cover the OnlyOffice tooltips and buttons: `Common.Views.Header` scenarios include rename (`Common.Views.RenameDialog`), recent files (`Common.Views.RecentFiles`), open (`Common.Views.OpenDialog` + `Common.Views.SelectFileDlg`), save-as (`Common.Views.SaveAsDlg`), about (`Common.Views.About`), language (`Common.Views.LanguageDialog`), share/embed (`Common.Views.ShareDialog`, `Common.Views.EmbedDialog`), `Common.Views.UserNameDialog`, and the quick-access toolbar (`Common.Views.CustomizeQuickAccessDialog`)
- AND document metadata is inspectable via `Common.Views.DocumentPropertyDialog`

### Requirement: R-GLOB-LOCKED — opened-but-locked or read-only files SHALL communicate the OnlyOffice lock state

#### Scenario: WHEN a file is locked by another session, or the user has view-only rights
- THEN the UI shows the corresponding `Common.Translation` strings exactly: `Common.Translation.tipFileLocked`, `Common.Translation.warnFileLocked`, `Common.Translation.warnFileLockedBtnEdit`, `Common.Translation.warnFileLockedBtnView`, `Common.Translation.tipFileReadOnly`, `Common.Translation.textMoreButton`
- AND the editor offers to open read-only when the edit lock cannot be acquired
- WHEN there is no pending content
- THEN no lock banner is shown

### Requirement: R-GLOB-SEARCH — search/find SHALL behave like OnlyOffice

#### Scenario: WHEN the user invokes search
- THEN the find bar (`Common.Views.SearchPanel`, `Common.UI.SearchBar`, `Common.UI.SearchDialog`; controller `Common.Controllers.Search` per editor) supports find, replace single / replace-all, case sensitivity, match case, whole word, highlight results, and "no matches" feedback
- AND search results are enumerated by the per-editor `Search` related views

### Requirement: R-GLOB-ERRORS — editor-level errors SHALL be surfaced via the OnlyOffice error catalogue

#### Scenario: WHEN a fatal or non-fatal condition occurs
- THEN the modal/notification text SHALL match the `Error` section of the global `Main` locale: conversion timeouts (`Error.convertationTimeoutText`), access denial (`Error.errorAccessDeny`), copy disabled (`Error.errorCopyDisabled`), inconsistent file extension (`Error.errorInconsistentExt` and the per-format variants `Error.errorInconsistentExtDocx`, `.errorInconsistentExtXlsx`, `.errorInconsistentExtPptx`, `.errorInconsistentExtPdf`), bad image URL (`Error.errorBadImageUrl`), password-protected file (`Error.errorFilePassProtect`), file-size exceeded (`Error.errorFileSizeExceed`), forced view mode (`Error.errorForcedViewMode`), session expiry (`Error.errorSessionAbsolute`, `.errorSessionIdle`, `.errorSessionToken`), token errors (`Error.errorToken`, `.errorTokenExpire`), server-connect/save failure (`Error.errorConnectToServer`, `.errorForceSave`, `.errorEditingDownloadas`, `.errorFileNotAssembled`, `.errorUpdateVersionOnDisconnect`, `.errorUserDrop`, `.errorViewerDisconnect`), database connection (`Error.errorDatabaseConnection`), stock-chart ordering (`Error.errorStockChart`), PDF-forms locked (`Error.errorPDFFormsLocked`), watermark cross-domain (`Error.errorSaveWatermark`), upload validation (`Error.uploadDocExtMessage`, `.uploadDocFileCountMessage`, `.uploadDocSizeMessage`, `.uploadImageExtMessage`, `.uploadImageFileCountMessage`, `.uploadImageSizeMessage`), split/divisor constraints (`Error.splitDividerErrorText`, `.splitMaxColsErrorText`, `.splitMaxRowsErrorText`), slow connection (`Error.scriptLoadError`), open/save generic (`Error.openErrorText`, `.saveErrorText`, `.unknownErrorText`), and the shared `Error.notcriticalErrorTitle`, `Error.criticalErrorTitle`, `Error.textOk`
- AND all `Main.*` application-level dialogs are available: session/version reload prompts (`Main.textServerVersion`, `Main.errorServerVersion`, `Main.textUpdateVersion`, `Main.errorUpdateVersion`, `Main.textDontUpdate`, `Main.textUpdate`), unsaved-changes guard (`Main.leavePageText`), read-only title (`Main.titleReadOnly`), protected-document roles (`Main.textDocumentProtected`, `Main.titleDialogProtectedDocument`, `Main.textDialogProtectedChangesTracked`, `Main.textDialogProtectedEditComments`, `Main.textDialogProtectedFillForms`, `Main.textDialogProtectedOnlyView`), macro prompts (`Main.textHasMacros`, `Main.textRequestMacros`, `Main.textRemember`), convert-to-PDF flow (`Main.textSaveAsPdf`, `Main.textDownloadPdf`, `Main.textConvertForm`, `Main.warnDownloadAsPdf`, `Main.txtSignedForm`), anonymous/guest identity (`Main.textAnonymous`, `Main.textGuest`), license states (`Main.tipLicenseExceeded`, `Main.tipLicenseUsersExceeded`, `Main.warnLicenseExp`, `Main.warnLicenseBefore`, `Main.warnLicenseAnonymous`, `Main.warnLicenseLimitedNoAccess`, `Main.warnLicenseLimitedRenewed`, `Main.warnNoLicenseUsers`, `Main.titleLicenseExp`, `Main.titleLicenseNotActive`, `Main.textNoLicenseTitle`, `Main.textPaidFeature`), resource exhaustion (`Main.warnNoResources`, `Main.textNoResourcesTitle`, `Main.textCustomLoader`, `Main.textBuyNow`, `Main.textContactUs`), and find/replace summaries (`Main.textNoMatches`, `Main.textReplaceSuccess`, `Main.textReplaceSkipped`)
- AND per-editor long-running task progress is shown via `LongActions`: `LongActions.openTextText`/`openTitleText`, `LongActions.loadingDocumentTextText`/`loadingDocumentTitleText`, `LongActions.savePreparingText`/`savePreparingTitle`, `LongActions.saveTextText`/`saveTitleText`, `LongActions.changesSaved`, `LongActions.downloadTextText`/`downloadTitleText`, `LongActions.downloadMergeText`/`downloadMergeTitle`, `LongActions.printTextText`/`printTitleText`, `LongActions.mailMergeLoadFileText`/`mailMergeLoadFileTitle`, `LongActions.sendMergeText`/`sendMergeTitle`, `LongActions.loadImageTextText`/`loadImageTitleText`, `LongActions.loadImagesTextText`/`loadImagesTitleText`, `LongActions.loadFontTextText`/`loadFontTitleText`, `LongActions.loadFontsTextText`/`loadFontsTitleText`, `LongActions.loadThemeTextText`/`loadThemeTitleText`, `LongActions.uploadImageTextText`/`uploadImageTitleText`, `LongActions.applyChangesTextText`/`applyChangesTitleText`, `LongActions.waitText`, `LongActions.textContinue`, `LongActions.textUndo`, `LongActions.textCancel`, `LongActions.textOk`, `LongActions.textNo`, `LongActions.textYes`, `LongActions.txtEditingMode`, `LongActions.confirmMaxChangesSize`, `LongActions.advDRMPassword`
- WHEN the browser is unsupported
- THEN the `unsupportedBrowserErrorText` and related `ApplicationController` strings of the affected editor are shown

### Requirement: R-GLOB-APPCONTROLLER — each editor SHALL reproduce its embed/forms `ApplicationController` and `ApplicationView` strings

The embed and forms variants of OnlyOffice carry a legacy flat dictionary per editor. All of the following per-app class strings MUST be present and correctly bound:

#### Scenario: WHEN the embed or forms variant of an editor is rendered
- THEN every `DE.ApplicationController.*` string is available: `DE.ApplicationController.convertationErrorText`, `DE.ApplicationController.convertationTimeoutText`, `DE.ApplicationController.criticalErrorTitle`, `DE.ApplicationController.downloadErrorText`, `DE.ApplicationController.downloadTextText`, `DE.ApplicationController.errorAccessDeny`, `DE.ApplicationController.errorCopyDisabled`, `DE.ApplicationController.errorDefaultMessage`, `DE.ApplicationController.errorEditingDownloadas`, `DE.ApplicationController.errorFileNotAssembled`, `DE.ApplicationController.errorFilePassProtect`, `DE.ApplicationController.errorFileSizeExceed`, `DE.ApplicationController.errorForceSave`, `DE.ApplicationController.errorForcedViewMode`, `DE.ApplicationController.errorInconsistentExt`, `DE.ApplicationController.errorInconsistentExtDocx`, `DE.ApplicationController.errorInconsistentExtPdf`, `DE.ApplicationController.errorInconsistentExtPptx`, `DE.ApplicationController.errorInconsistentExtXlsx`, `DE.ApplicationController.errorLoadingFont`, `DE.ApplicationController.errorSubmit`, `DE.ApplicationController.errorToken`, `DE.ApplicationController.errorTokenExpire`, `DE.ApplicationController.errorUpdateVersionOnDisconnect`, `DE.ApplicationController.errorUserDrop`, `DE.ApplicationController.notcriticalErrorTitle`, `DE.ApplicationController.openErrorText`, `DE.ApplicationController.scriptLoadError`, `DE.ApplicationController.textAnonymous`, `DE.ApplicationController.textCancel`, `DE.ApplicationController.textClear`, `DE.ApplicationController.textConvertFormDownload`, `DE.ApplicationController.textCtrl`, `DE.ApplicationController.textDownloadPdf`, `DE.ApplicationController.textGotIt`, `DE.ApplicationController.textGuest`, `DE.ApplicationController.textLoadingDocument`, `DE.ApplicationController.textNext`, `DE.ApplicationController.textOf`, `DE.ApplicationController.textOk`, `DE.ApplicationController.textRequired`, `DE.ApplicationController.textSubmit`, `DE.ApplicationController.textSubmited`, `DE.ApplicationController.titleLicenseExp`, `DE.ApplicationController.titleLicenseNotActive`, `DE.ApplicationController.txtClose`, `DE.ApplicationController.txtEmpty`, `DE.ApplicationController.txtNo`, `DE.ApplicationController.txtOpenWarning`, `DE.ApplicationController.txtPressLink`, `DE.ApplicationController.txtSecurityWarningLink`, `DE.ApplicationController.txtSecurityWarningLinkOk`, `DE.ApplicationController.txtSecurityWarningOpenFile`, `DE.ApplicationController.txtYes`, `DE.ApplicationController.unknownErrorText`, `DE.ApplicationController.unsupportedBrowserErrorText`, `DE.ApplicationController.waitText`, `DE.ApplicationController.warnLicenseBefore`, `DE.ApplicationController.warnLicenseExp`
- AND the same string family exists for the spreadsheet editor: `SSE.ApplicationController.convertationErrorText`, `SSE.ApplicationController.convertationTimeoutText`, `SSE.ApplicationController.criticalErrorTitle`, `SSE.ApplicationController.downloadErrorText`, `SSE.ApplicationController.downloadTextText`, `SSE.ApplicationController.errorAccessDeny`, `SSE.ApplicationController.errorCopyDisabled`, `SSE.ApplicationController.errorDefaultMessage`, `SSE.ApplicationController.errorEditingDownloadas`, `SSE.ApplicationController.errorFileNotAssembled`, `SSE.ApplicationController.errorFilePassProtect`, `SSE.ApplicationController.errorFileSizeExceed`, `SSE.ApplicationController.errorForceSave`, `SSE.ApplicationController.errorForcedViewMode`, `SSE.ApplicationController.errorInconsistentExt`, `SSE.ApplicationController.errorInconsistentExtDocx`, `SSE.ApplicationController.errorInconsistentExtPdf`, `SSE.ApplicationController.errorInconsistentExtPptx`, `SSE.ApplicationController.errorInconsistentExtXlsx`, `SSE.ApplicationController.errorLoadingFont`, `SSE.ApplicationController.errorToken`, `SSE.ApplicationController.errorTokenExpire`, `SSE.ApplicationController.errorUpdateVersionOnDisconnect`, `SSE.ApplicationController.errorUserDrop`, `SSE.ApplicationController.notcriticalErrorTitle`, `SSE.ApplicationController.openErrorText`, `SSE.ApplicationController.scriptLoadError`, `SSE.ApplicationController.textAnonymous`, `SSE.ApplicationController.textGuest`, `SSE.ApplicationController.textLoadingDocument`, `SSE.ApplicationController.textOf`, `SSE.ApplicationController.titleLicenseExp`, `SSE.ApplicationController.titleLicenseNotActive`, `SSE.ApplicationController.txtClose`, `SSE.ApplicationController.txtNo`, `SSE.ApplicationController.txtOpenWarning`, `SSE.ApplicationController.txtPressLink`, `SSE.ApplicationController.txtYes`, `SSE.ApplicationController.unknownErrorText`, `SSE.ApplicationController.unsupportedBrowserErrorText`, `SSE.ApplicationController.waitText`, `SSE.ApplicationController.warnLicenseBefore`, `SSE.ApplicationController.warnLicenseExp`
- AND the same string family exists for the presentation editor: `PE.ApplicationController.convertationErrorText`, `PE.ApplicationController.convertationTimeoutText`, `PE.ApplicationController.criticalErrorTitle`, `PE.ApplicationController.downloadErrorText`, `PE.ApplicationController.downloadTextText`, `PE.ApplicationController.errorAccessDeny`, `PE.ApplicationController.errorCopyDisabled`, `PE.ApplicationController.errorDefaultMessage`, `PE.ApplicationController.errorEditingDownloadas`, `PE.ApplicationController.errorFileNotAssembled`, `PE.ApplicationController.errorFilePassProtect`, `PE.ApplicationController.errorFileSizeExceed`, `PE.ApplicationController.errorForceSave`, `PE.ApplicationController.errorForcedViewMode`, `PE.ApplicationController.errorInconsistentExt`, `PE.ApplicationController.errorInconsistentExtDocx`, `PE.ApplicationController.errorInconsistentExtPdf`, `PE.ApplicationController.errorInconsistentExtPptx`, `PE.ApplicationController.errorInconsistentExtXlsx`, `PE.ApplicationController.errorLoadingFont`, `PE.ApplicationController.errorToken`, `PE.ApplicationController.errorTokenExpire`, `PE.ApplicationController.errorUpdateVersionOnDisconnect`, `PE.ApplicationController.errorUserDrop`, `PE.ApplicationController.notcriticalErrorTitle`, `PE.ApplicationController.openErrorText`, `PE.ApplicationController.scriptLoadError`, `PE.ApplicationController.textAnonymous`, `PE.ApplicationController.textGuest`, `PE.ApplicationController.textLoadingDocument`, `PE.ApplicationController.textOf`, `PE.ApplicationController.titleLicenseExp`, `PE.ApplicationController.titleLicenseNotActive`, `PE.ApplicationController.txtClose`, `PE.ApplicationController.txtNo`, `PE.ApplicationController.txtOpenWarning`, `PE.ApplicationController.txtPressLink`, `PE.ApplicationController.txtYes`, `PE.ApplicationController.unknownErrorText`, `PE.ApplicationController.unsupportedBrowserErrorText`, `PE.ApplicationController.waitText`, `PE.ApplicationController.warnLicenseBefore`, `PE.ApplicationController.warnLicenseExp`
- AND the same string family exists for the visio editor: `VE.ApplicationController.convertationErrorText`, `VE.ApplicationController.convertationTimeoutText`, `VE.ApplicationController.criticalErrorTitle`, `VE.ApplicationController.downloadErrorText`, `VE.ApplicationController.downloadTextText`, `VE.ApplicationController.errorAccessDeny`, `VE.ApplicationController.errorCopyDisabled`, `VE.ApplicationController.errorDefaultMessage`, `VE.ApplicationController.errorEditingDownloadas`, `VE.ApplicationController.errorFileNotAssembled`, `VE.ApplicationController.errorFilePassProtect`, `VE.ApplicationController.errorFileSizeExceed`, `VE.ApplicationController.errorForceSave`, `VE.ApplicationController.errorForcedViewMode`, `VE.ApplicationController.errorInconsistentExt`, `VE.ApplicationController.errorInconsistentExtDocx`, `VE.ApplicationController.errorInconsistentExtPdf`, `VE.ApplicationController.errorInconsistentExtPptx`, `VE.ApplicationController.errorInconsistentExtXlsx`, `VE.ApplicationController.errorLoadingFont`, `VE.ApplicationController.errorToken`, `VE.ApplicationController.errorTokenExpire`, `VE.ApplicationController.errorUpdateVersionOnDisconnect`, `VE.ApplicationController.errorUserDrop`, `VE.ApplicationController.notcriticalErrorTitle`, `VE.ApplicationController.openErrorText`, `VE.ApplicationController.scriptLoadError`, `VE.ApplicationController.textAnonymous`, `VE.ApplicationController.textGuest`, `VE.ApplicationController.textLoadingDocument`, `VE.ApplicationController.textOf`, `VE.ApplicationController.titleLicenseExp`, `VE.ApplicationController.titleLicenseNotActive`, `VE.ApplicationController.txtClose`, `VE.ApplicationController.txtNo`, `VE.ApplicationController.txtOpenWarning`, `VE.ApplicationController.txtPage`, `VE.ApplicationController.txtPressLink`, `VE.ApplicationController.txtYes`, `VE.ApplicationController.unknownErrorText`, `VE.ApplicationController.unsupportedBrowserErrorText`, `VE.ApplicationController.waitText`, `VE.ApplicationController.warnLicenseBefore`, `VE.ApplicationController.warnLicenseExp`
- AND every `X.ApplicationView` embed string is available and bound to its command: DE: `DE.ApplicationView.txtDownload`, `DE.ApplicationView.txtDownloadDocx`, `DE.ApplicationView.txtDownloadPdf`, `DE.ApplicationView.txtEmbed`, `DE.ApplicationView.txtFileLocation`, `DE.ApplicationView.txtFullScreen`, `DE.ApplicationView.txtPrint`, `DE.ApplicationView.txtSearch`, `DE.ApplicationView.txtShare`; SSE: `SSE.ApplicationView.txtDownload`, `SSE.ApplicationView.txtEmbed`, `SSE.ApplicationView.txtFileLocation`, `SSE.ApplicationView.txtFullScreen`, `SSE.ApplicationView.txtPrint`, `SSE.ApplicationView.txtSearch`, `SSE.ApplicationView.txtShare`; PE: `PE.ApplicationView.txtDownload`, `PE.ApplicationView.txtEmbed`, `PE.ApplicationView.txtFileLocation`, `PE.ApplicationView.txtFullScreen`, `PE.ApplicationView.txtPrint`, `PE.ApplicationView.txtSearch`, `PE.ApplicationView.txtShare`; VE: `VE.ApplicationView.txtDownload`, `VE.ApplicationView.txtEmbed`, `VE.ApplicationView.txtFileLocation`, `VE.ApplicationView.txtFullScreen`, `VE.ApplicationView.txtPrint`, `VE.ApplicationView.txtSearch`, `VE.ApplicationView.txtShare`

### Requirement: R-GLOB-MOBILE — mobile web variants SHALL reproduce OnlyOffice mobile section strings

OnlyOffice ships a mobile web variant per editor. Its locale is section-nested; the World-Office mobile UI SHALL expose the same sections and strings.

#### Scenario: WHEN any editor renders in mobile web view
- THEN the shared `Main` application section is available: `Main.criticalErrorTitle`, `.errorAccessDeny`, `.errorOpensource`, `.errorServerVersion`, `.errorUpdateVersion`, `.leavePageText`, `.notcriticalErrorTitle`, `.textAnonymous`, `.textBuyNow`, `.textCancel`, `.textClose`, `.textContactUs`, `.textConvertForm`, `.textCustomLoader`, `.textDialogProtectedChangesTracked`, `.textDialogProtectedEditComments`, `.textDialogProtectedFillForms`, `.textDialogProtectedOnlyView`, `.textDocumentProtected`, `.textDownloadPdf`, `.textGuest`, `.textHasMacros`, `.textNo`, `.textNoLicenseTitle`, `.textNoMatches`, `.textNoResourcesTitle`, `.textOk`, `.textPaidFeature`, `.textRemember`, `.textReplaceSkipped`, `.textReplaceSuccess`, `.textRequestMacros`, `.textSaveAsPdf`, `.textYes`, `.tipLicenseExceeded`, `.tipLicenseUsersExceeded`, `.titleDialogProtectedDocument`, `.titleLicenseExp`, `.titleLicenseNotActive`, `.titleReadOnly`, `.titleServerVersion`, `.titleUpdateVersion`, `.txtSignedForm`, `.warnDownloadAsPdf`, `.warnLicenseAnonymous`, `.warnLicenseBefore`, `.warnLicenseExp`, `.warnLicenseLimitedNoAccess`, `.warnLicenseLimitedRenewed`, `.warnNoLicenseUsers`, `.warnNoResources`, `.warnProcessRightsChange`, and the nested SDK dictionary `Main.SDK` (`Main.SDK.Heading 1` … `Main.SDK.footnote reference`)
- AND the `Controller.Main` mobile controller strings are present: `Controller.Main.SDK`, `.advDRMOptions`, `.advDRMPassword`, `.closeButtonText`, `.criticalErrorTitle`, `.errorAccessDeny`, `.errorOpensource`, `.errorServerVersion`, `.errorUpdateVersion`, `.leavePageText`, `.notcriticalErrorTitle`, `.textAnonymous`, `.textBuyNow`, `.textClose`, `.textContactUs`, `.textCustomLoader`, `.textDontUpdate`, `.textGuest`, `.textHasMacros`, `.textNo`, `.textNoChoices`, `.textNoLicenseTitle`, `.textNoMatches`, `.textNoResourcesTitle`, `.textOk`, `.textOpenFile`, `.textPaidFeature`, `.textRemember`, `.textReplaceSkipped`, `.textReplaceSuccess`, `.textRequestMacros`, `.textUpdate`, `.textWarnUpdateExternalData`, `.textYes`, `.tipLicenseExceeded`, `.tipLicenseUsersExceeded`, `.titleLicenseExp`, `.titleLicenseNotActive`, `.titleReadOnly`, `.titleServerVersion`, `.titleUpdateVersion`, `.txtIncorrectPwd`, `.txtProtected`, `.warnLicenseAnonymous`, `.warnLicenseBefore`, `.warnLicenseExp`, `.warnLicenseLimitedNoAccess`, `.warnLicenseLimitedRenewed`, `.warnNoLicenseUsers`, `.warnNoResources`, `.warnProcessRightsChange`
- AND the shared mobile sections `About`, `Add`, `ContextMenu`, `Draw`, `Edit`, `Error`, `LongActions`, `Settings`, `Statusbar`, `Toolbar` are all implemented with OnlyOffice-equivalent entries
- AND the per-app mobile `View` sections render equivalent content: `View.Add`, `View.Edit`, `View.Settings`
- AND mobile theme/collaboration sub-dictionaries match: `Common.Collaboration`, `Common.HighlightColorPalette`, `Common.ThemeColorPalette`, `Common.Themes`, `Common.VersionHistory`
- AND the embed-only string pair `common.view.SearchBar` and `common.view.modals` is implemented in the embed viewer
- AND the legacy flat key `cancelButtonText` resolves correctly in every dialog that carries a cancel button

### Requirement: R-GLOB-LEAVE-GUARD — unsaved changes SHALL be guarded before navigation/close

#### Scenario: WHEN the user attempts to leave, close, or reload with unsaved edits
- THEN the `Toolbar`/`Main` guard prompt is shown with the OnlyOffice wording (`Toolbar.dlgLeaveMsgText`/`dlgLeaveTitleText`, `Toolbar.leaveButtonText`, `Toolbar.stayButtonText`, `Toolbar.textSaveData`, `Toolbar.textUnsavedData`, `Toolbar.textSave`, `Toolbar.textCancel`, `Toolbar.textDontSave`)
- AND the user can stay (wait for autosave), leave (discard), or save

### Requirement: R-GLOB-THEME — theme switching SHALL offer OnlyOffice's theme set

#### Scenario: WHEN the user opens theme settings
- THEN `Common.Themes` offers light, dark, and system/same-as-system
- AND `Common.UI.Themes` and `Common.ThemeColorPalette`/`Common.UI.ThemeColorPalette` render the theme and theme-color palettes identically
- AND `Common.UI.Themes` applies the chosen theme to the whole editor chrome

---

## 4. Common Dialogs and Widgets

### Requirement: R-DLG-GENERAL — general-purpose dialogs SHALL match OnlyOffice behavior

#### Scenario: WHEN the user opens any common dialog
- THEN open/recent/save-as flows use `Common.Views.OpenDialog`, `Common.Views.RecentFiles`, `Common.Views.SaveAsDlg`, `Common.Views.SelectFileDlg`, and `Common.Views.RenameDialog` with OnlyOffice field sets (file name, location, format)
- AND file meta is shown by `Common.Views.DocumentPropertyDialog`
- AND the user-dialog `Common.Views.UserNameDialog` and copy-warning `Common.Views.CopyWarningDialog` behave like OnlyOffice
- AND proofing/typing assist uses `Common.Views.AutoCorrectDialog` with the OnlyOffice auto-correct option set (capitalize first letter, replace-as-you-type, smart quotes, custom replacement entries) in DE, SSE, and PE
- AND link/embed/sharing entry points `Common.Views.EmbedDialog`, `Common.Views.ShareDialog`, `Common.Views.DocumentAccessDialog` follow OnlyOffice (see §6 for collaboration-specific behavior)

### Requirement: R-DLG-SEARCHDIALOG — the search dialog SHALL match OnlyOffice

#### Scenario: WHEN the user performs find/replace
- THEN `Common.UI.SearchDialog` and `Common.UI.SearchBar` provide find-text, replace-text, replace-all, case-sensitive, whole-word-only, and highlight-results controls
- AND `Common.Views.SearchPanel` shows match counts, previous/next navigation and "no matches" state

### Requirement: R-DLG-SYMBOL — the symbol table SHALL match OnlyOffice

#### Scenario: WHEN the user inserts a symbol
- THEN `Common.Views.SymbolTableDialog` presents fonts, subsets, recent symbols and the insertable grid exactly as OnlyOffice does

### Requirement: R-DLG-LANGUAGE — the language dialog SHALL match OnlyOffice

#### Scenario: WHEN the user changes proofing or interface language
- THEN `Common.Views.LanguageDialog` lists the OnlyOffice language set and applies the change persistently

### Requirement: R-DLG-IMAGEFROM — insert-image-from-URL SHALL match OnlyOffice

#### Scenario: WHEN the user pastes an image URL
- THEN `Common.Views.ImageFromUrlDialog` validates the URL, shows the OnlyOffice error text for bad URLs, and inserts the fetched image

### Requirement: R-DLG-ABOUT — the About dialog SHALL match OnlyOffice

#### Scenario: WHEN the user opens About
- THEN `Common.Views.About` shows editor name, version, address, email, telephone and "Powered By" attribution matching the mobile `About` section strings

### Requirement: R-DLG-TABLE-INSERT — the insert-table picker SHALL match OnlyOffice

#### Scenario: WHEN the user inserts a table
- THEN `Common.Views.InsertTableDialog` provides the rows×columns picker and quick presets
- AND `Common.Views.ListSettingsDialog` governs list/bullet settings (see also per-app list settings `DE.Views.ListSettingsDialog`, `DE.Views.ListIndentsDialog`, `DE.Views.ListTypesAdvanced`)

### Requirement: R-DLG-FORMATSETTINGS — the shared format-settings dialog SHALL match OnlyOffice

#### Scenario: WHEN a shared formatting dialog is opened
- THEN `Common.Views.FormatSettingsDialog` and `Common.Views.ShapeShadowDialog` reproduce OnlyOffice's font, paragraph, shape and shadow settings surfaces

### Requirement: R-DLG-EDITNAME — the edit-name dialog SHALL validate like OnlyOffice

#### Scenario: WHEN the user renames a chart, range, style, or other named object
- THEN `Common.Views.EditNameDialog` applies OnlyOffice name-validation rules and conflict messages (`Main.textInvalidName` / `Edit.textInvalidName`)

### Requirement: R-DLG-PASSWORD — password dialogs SHALL match OnlyOffice

#### Scenario: WHEN a file is password-protected or requires a password to set/change
- THEN `Common.Views.PasswordDialog` covers open-password, set-password, and change-password flows with OnlyOffice strings (`Settings.textOpenFile`, `Settings.textSetPassword`, `Settings.textChangePassword`, `Settings.txtIncorrectPwd`, `Settings.textPasswordNotMatched`, `Settings.textPasswordWarning`, `Settings.txtProtected`, `Error.errorPasswordIsNotCorrect`)

---

## 5. Collaboration, Review, Comments, Chat, History

### Requirement: R-COLLAB-COMMENTS — comments SHALL match OnlyOffice

#### Scenario: WHEN any editor is used collaboratively
- THEN the comments panel (`Common.Views.Comments`, controller `Common.Controllers.Chat`) supports add/edit/delete/reply/resolve/reopen with OnlyOffice strings (`Common.Collaboration.textAddComment`, `.textAddReply`, `.textEditComment`, `.textEditReply`, `.textDeleteComment`, `.textDeleteReply`, `.textResolve`, `.textReopen`, `.textMessageDeleteComment`, `.textMessageDeleteReply`, `.textNoComments`)
- AND `Common.Views.ReviewPopover` marks the in-canvas comment popover
- AND display settings honor resolved-comments visibility (`Settings.textResolvedComments`, `Settings.textCommentsDisplay`)

### Requirement: R-COLLAB-REVIEW — change tracking and review SHALL match OnlyOffice

#### Scenario: WHEN a document has tracked changes
- THEN the review surface (`Common.Views.ReviewChanges`, `Common.Views.ReviewChangesDialog`, controller `Common.Controllers.ReviewChanges`) exposes accept/reject per-change and accept/reject-all (`Common.Collaboration.textAccept`, `.textReject`, `.textAcceptAllChanges`, `.textRejectAllChanges`, `.textReviewChange`, `.textReview`, `.textNoChanges`, `.textChanged`-class labels)
- AND the review display modes match (`Common.Collaboration.textMarkup`, `.textFinal`, `.textOriginal`, `.textAllChangesEditing`, `.textAllChangesAcceptedPreview`, `.textAllChangesRejectedPreview`, `.textDisplayMode`)
- AND revision detail labels match (`Common.Collaboration.textInserted`, `.textDeleted`, `.textParaInserted`, `.textParaDeleted`, `.textParaFormatted`, `.textParaMoveFromUp`, `.textParaMoveFromDown`, `.textParaMoveTo`, `.textTableChanged`, `.textTableRowsAdd`, `.textTableRowsDel`, `.textNum`, `.textTabs`)
- AND the fast-mode undo/redo notice matches (`Common.Collaboration.textTryUndoRedo`)

### Requirement: R-COLLAB-CHAT — chat SHALL be available where OnlyOffice offers it

#### Scenario: WHEN the host enables chat for a co-editing session
- THEN `Common.Controllers.Chat`/`Common.Views.Chat` open a chat panel wired to the collaboration channel

### Requirement: R-COLLAB-HISTORY — version history SHALL match OnlyOffice

#### Scenario: WHEN the user opens version history
- THEN `Common.Controllers.History`/`Common.Views.History` show versions with author, timestamp, current-version marker, restore, and the restore warning (`Common.VersionHistory.textVersionHistory`, `.textVersion`, `.textAnonymous`, `.textCurrent`, `.textRestore`, `.textWarningRestoreVersion`, `.titleWarningRestoreVersion`, `.txtErrorLoadHistory`, `.textBack`), matching `Settings.textVersionHistory`

### Requirement: R-COLLAB-USERS — the users/rights surface SHALL match OnlyOffice

#### Scenario: WHEN the user opens sharing/document access
- THEN `Common.Views.DocumentAccessDialog` offers the OnlyOffice sharing settings surface (`Common.Collaboration.textSharingSettings`, `.textEditUser`, `.textUsers`, `.textAnonymous`, `.textGuest`)
- AND `Common.Views.PasteOptions`/`Common.Controllers.PasteOptions` govern collaborative paste behavior with `ContextMenu.errorCopyCutPaste` note text

### Requirement: R-COLLAB-PROTECTION-OVERRIDE — protected documents SHALL disable editing with explanation

#### Scenario: WHEN a document protection or access rule denies editing
- THEN `Common.Views.Protection` shows the OnlyOffice explanation (`Main.textDocumentProtected`, `Main.titleDialogProtectedDocument`) and offers only the permitted actions (view/comment/fill-forms) with matching strings

### Requirement: R-COLLAB-DEFINE — the shared enumerated definitions SHALL be complete

#### Scenario: WHEN the UI renders chart, conditional-format, animation, gridline, or smart-art pickers
- THEN the underlying enumerations are exact: `Common.define.chartData` (≈42 chart types incl. 3-D, combo, radar, scatter, stock, surface, doughnut), `Common.define.conditionalData` (conditional-format rules), `Common.define.effectData` (199 animation effect families), `Common.define.gridlineData` (gridline styles), `Common.define.smartArt` (SmartArt layouts)

---

## 6. Protection, Signing, and Form Roles

### Requirement: R-PROTECT-DE — document protection SHALL match OnlyOffice

#### Scenario: WHEN the author protects a document
- THEN the DE protection flow (`DE.Views.DocProtection`, `DE.Controllers.DocProtection`, `DE.Views.ProtectDialog`) offers the OnlyOffice protection types (no changes, comments only, fill-in forms, tracked changes) with `Settings.textTypeEditing`, `Settings.textTypeEditingWarning`, `Settings.textProtectDocument`, `Settings.textProtectTurnOff`, `Settings.textDialogUnprotect`, `Settings.titleDialogUnprotect`, `Settings.textUnprotect`, `Settings.textRequirePassword`
- WHEN the user opens a protected file
- THEN the read-only/edit-comments/fill-forms sentence is shown (`Settings.textFillingForms`, `Settings.textTrackedChanges`)

### Requirement: R-PROTECT-SSE — spreadsheet protection and protected ranges SHALL match OnlyOffice

#### Scenario: WHEN a workbook/sheet is protected
- THEN the SSE protection surface (`SSE.Views.WBProtection`, `SSE.Views.ProtectDialog`, `SSE.Views.ProtectRangesDlg`, `SSE.Views.ProtectedRangesEditDlg`, `SSE.Views.ProtectedRangesManagerDlg`) protects sheets and named cell ranges, allows/denies specific users, and locks/unlocks range editing with OnlyOffice strings (`LongActions.textUnlockRange`, `LongActions.textUnlockRangeWarning`, `Error.errorEditProtectedRange`, `Error.errorCannotUseCommandProtectedSheet`, `Error.errorChangeOnProtectedSheet`, `Error.errorLockedCellPivot`, `Error.errorLockedWorksheetRename`, `Error.errorLockedAll`)
- AND unexpected protected-range multi-select errors match `Error.errorPasteMultiSelect`

### Requirement: R-PROTECT-SIGN — e-signature SHALL match OnlyOffice

#### Scenario: WHEN the user signs, views a signature, or configures signature settings
- THEN the signing UI (`Common.Views.PdfSignDialog`, `Common.Views.SignDialog`, `Common.Views.SignSettingsDialog`, `DE.Views.SignatureSettings`, `SSE.Views.SignatureSettings`, `PE.Views.SignatureSettings`) supports the OnlyOffice sign-in/sign-out, certificate, and signature image flows
- AND `DE.Views.SendForSigningSettings`/`DE.Views.RolesManagerDlg`/`DE.Views.RoleEditDlg`/`DE.Views.RoleDeleteDlg` manage send-for-signing recipients and roles with the `DE.Views.Role*` strings ("Example: Applicant, Client, Sales Rep", recipient add/delete/edit, order of signing)

### Requirement: R-PROTECT-FORMS — fillable-form submission status SHALL match OnlyOffice

#### Scenario: WHEN a form document records submission
- THEN `DE.Views.SaveFormDlg` and `DE.Views.FillingStatusSettings` track which recipients have filled/signed the form, with per-role status shown in the Forms tab

### Requirement: R-PROTECT-WATERMARK — watermarks SHALL match OnlyOffice

#### Scenario: WHEN the user manages a watermark
- THEN `DE.Views.WatermarkSettingsDialog` provides text watermark (text, font, size, color, transparency, rotation, layout) with OnlyOffice behavior, and cross-domain watermark errors follow `Error.errorSaveWatermark`

---

## 7. External Editors, Links, Plugins, Macros, Shortcuts

### Requirement: R-EXT-EDITORS — external object editors SHALL match OnlyOffice

#### Scenario: WHEN the user edits an embedded diagram (SmartArt/Visio-like), OLE object, or merged range
- THEN the external-editor channels exist: `Common.Controllers.ExternalDiagramEditor` with `Common.Views.ExternalDiagramEditor`, `Common.Controllers.ExternalOleEditor` with `Common.Views.ExternalOleEditor`, `Common.Controllers.ExternalMergeEditor` with `Common.Views.ExternalMergeEditor`, and the generic `Common.Views.ExternalEditor`
- AND `Common.Views.ExternalLinksDlg`/`Common.Controllers.ExternalLinks` manage external links with the OnlyOffice link-refresh behavior (`Edit.textRefreshEntireTable`, `Edit.textRefreshPageNumbersOnly`, `SSE.Views.ExternalLinksDlg` for the spreadsheet variant)

### Requirement: R-EXT-LINK-INSERT — link insertion/editing SHALL match OnlyOffice

#### Scenario: WHEN the user inserts or edits a hyperlink
- THEN the relevant per-app settings dialog opens (`DE.Views.HyperlinkSettingsDialog`, `SSE.Views.HyperlinkSettingsDialog`, `PE.Views.HyperlinkSettingsDialog`, `PDFE.Views.HyperlinkSettingsDialog`) with display text, address, tooltip, and `ContextMenu` open/edit/remove-link entries (`ContextMenu.menuAddLink`, `.menuEditLink`, `.menuOpenLink`, `.menuCancel`, `.textOk`, `.txtWarnUrl`, `Edit.textEditLink`, `Edit.textDeleteLink`, `Edit.textScreenTip`, `Edit.textOpenLocation`)
- AND unsafe-link warnings match `ContextMenu.txtWarnUrl` / `DE.ApplicationController.txtSecurityWarningLink`

### Requirement: R-EXT-PLUGINS — the plugin system SHALL match OnlyOffice

#### Scenario: WHEN plugins are enabled
- THEN `Common.Controllers.Plugins`/`Common.Views.Plugins` host the plugin manager, `Common.Views.PluginPanel` the in-editor plugin panel, and `Common.Views.PluginDlg` the plugin configuration dialog, using the OnlyOffice plugin lifecycle (install, update, enable/disable, per-document scope)

### Requirement: R-EXT-MACROS — macros SHALL match OnlyOffice

#### Scenario: WHEN macros are used
- THEN `Common.Views.MacrosDialog` and `Common.Views.MacrosAiDialog` provide the macro editor and the OnlyOffice AI-macro assistant dialog
- AND `SSE.Views.MacroDialog` provides the spreadsheet macro dialog
- AND macro security settings are honored: `Settings.textDisableAll`, `Settings.textDisableAllMacrosWithNotification`, `Settings.textDisableAllMacrosWithoutNotification`, `Settings.textEnableAll`, `Settings.textEnableAllMacrosWithoutNotification`, `Settings.textMacrosSettings`, `Settings.textShowNotification`, plus macro-run prompts (`Main.textHasMacros`, `Main.textRequestMacros`, `Main.textRemember`)

### Requirement: R-EXT-SHORTCUTS — keyboard shortcuts SHALL match OnlyOffice

#### Scenario: WHEN the user presses a shortcut
- THEN `Common.Controllers.Shortcuts`, `Common.Views.ShortcutsDialog`, and `Common.Views.ShortcutsEditDialog` provide OnlyOffice's default keymap and the ability to view/reassign shortcuts per category

---

## 8. Document Editor (DE)

### Requirement: R-DE-CONTROLLERS — the DE controller layer SHALL match OnlyOffice

#### Scenario: WHEN the document editor runs
- THEN these controllers are mounted: `DE.Controllers.ApplicationController`, `DE.Controllers.DocProtection`, `DE.Controllers.HeaderFooterTab`, `DE.Controllers.LeftMenu`, `DE.Controllers.Main`, `DE.Controllers.Navigation`, `DE.Controllers.Print`, `DE.Controllers.Search`, `DE.Controllers.Statusbar`, `DE.Controllers.Toolbar`, `DE.Controllers.Viewport`, `DE.Views.ApplicationView`

### Requirement: R-DE-TOOLBAR — the DE toolbar tabs SHALL match OnlyOffice exactly

#### Scenario: WHEN the user views the DE ribbon
- THEN `DE.Views.Toolbar` shows exactly the OnlyOffice tab set: **File, Home, Insert, Layout, References, Review, Collaboration, View** plus the contextual tabs **Draw, Chart design, Header & Footer, Protection** when their object type is active
- AND each tab exposes the OnlyOffice command groups (clipboard, fonts, paragraph, styles, editing; insert page/table/image/shape/chart/header-footer/textbox/smartart; page setup, section breaks, columns, hyphenation; table of contents, footnotes, citations; proofing, language, track changes, comments, compare; zoom, rulers, navigation; macros; protect; email merge under File)
- AND DE `FileMenuPanels`Slide settings, and the Slide Master, Protection, and Collaboration contextual tabs are shown when appropriate

### Requirement: R-DE-FILEMENU — the DE File menu SHALL match OnlyOffice

#### Scenario: WHEN the user opens File
- THEN `DE.Views.FileMenu` and `DE.Views.FileMenuPanels` offer New, Open (recent/from device), Save, Save As (docx/odt/txt/rtf/pdf/download-as), Print, Protect, Info (with `Settings.textDocumentInfo`, `Settings.textDocumentTitle`, `Settings.textAuthor`, `Settings.textCreated`, `Settings.textModified`-class fields), Feedback, Go back (`Settings.textDownload`, `Settings.textDownloadAs`, `Settings.textExport`, `Settings.textExportAs`, `Settings.textPrint`, `Settings.textHelp`, `Settings.textFeedback`, `Settings.textAbout`, `Settings.textDocumentSettings`, `Settings.textAddToFavorites`, `Settings.textRemoveFromFavorites`, `Settings.textOpenLocation`, `Settings.textStatistic`, `Settings.textWords`, `Settings.textPages`, `Settings.textParagraphs`, `Settings.textCharacters`-class statistics)
- AND download-format warnings match (`Settings.textDownloadTxt`, `Settings.textDownloadRtf`, `Settings.txtDownloadTxt`)

### Requirement: R-DE-VIEWTAB — DE view options and navigation SHALL match OnlyOffice

#### Scenario: WHEN the user uses View
- THEN `DE.Views.ViewTab` offers zoom (fit-to-page, fit-to-width, custom), page navigation (`DE.Views.Navigation`, `DE.Controllers.Navigation`), thumbnails (`DE.Views.PageThumbnails`), rulers, track-changes display, field shading, nonprinting characters, dark document, interface theme, and macros recording (record/pause/resume/stop)
- AND `View.Settings`/`Settings.textNavigation` navigation-panel toggles apply (`Settings.textEmptyScreen`-class empty-headings hint)
- WHEN the user searches within the document
- THEN `DE.Controllers.Search` drives find/replace with `DE.Views.ApplicationView` echo

### Requirement: R-DE-HOMEFORMATTING — home formatting dialogs SHALL match OnlyOffice

#### Scenario: WHEN the user formats text, paragraphs, or lists
- THEN `DE.Views.ParagraphSettings` and `DE.Views.ParagraphSettingsAdvanced` (indents, spacing, pagination, tabs, borders, bullets), `DE.Views.ListSettingsDialog`, `DE.Views.ListIndentsDialog`, `DE.Views.ListTypesAdvanced`, `DE.Views.StyleTitleDialog` (rename/update-to-match style), and `DE.Views.DropcapSettingsAdvanced` reproduce OnlyOffice controls
- AND list item text/number edits open `DE.Views.EditListItemDialog` with OnlyOffice list-level and value controls
- AND line numbers (`DE.Views.LineNumbersDialog`) and hyphenation (`DE.Views.HyphenationDialog`) match OnlyOffice

### Requirement: R-DE-INSERT — insert/rereference objects SHALL match OnlyOffice

#### Scenario: WHEN the user inserts document objects
- THEN bookmarks (`DE.Views.BookmarksDialog`), captions (`DE.Views.CaptionDialog`), cross-references (`DE.Views.CrossReferenceDialog`), custom columns (`DE.Views.CustomColumnsDialog` for columns in tables), date-time (`DE.Views.DateTimeDialog`), and notes (`DE.Views.NoteSettingsDialog`, `DE.Views.NotesRemoveDialog`) reproduce OnlyOffice
- AND Links (`DE.Views.Links`) manages hyperlinks/bookmark links in the References flow

### Requirement: R-DE-CAPTION — multi-level captions SHALL match OnlyOffice

#### Scenario: WHEN the user numbers chapters/captions
- THEN `DE.Views.CaptionDialog` and `DE.Views.TableFormulaDialog`/`DE.Views.CellsAddDialog`/`DE.Views.CellsRemoveDialog` (formulas and row/column cells in tables) behave like OnlyOffice

### Requirement: R-DE-TABLES — table tools SHALL match OnlyOffice

#### Scenario: WHEN the user works with tables
- THEN `DE.Views.TableSettings` and `DE.Views.TableSettingsAdvanced` (rows/columns, cell margins, borders, repeat header, banded rows/columns, position), `DE.Views.TableToTextDialog`, and `DE.Views.TextToTableDialog` reproduce OnlyOffice
- AND the row/column add/remove confirmations match `DE.Views.CellsAddDialog`/`DE.Views.CellsRemoveDialog`

### Requirement: R-DE-HEADERFOOTER — headers/footers and page setup SHALL match OnlyOffice

#### Scenario: WHEN the user edits headers/footers or page setup
- THEN `DE.Controllers.HeaderFooterTab`/`DE.Views.HeaderFooterTab` and `DE.Views.HeaderFooterSettings` provide Header/Footer tabs and Settings with Justify/Align function for header text
- AND page setup reproduces OnlyOffice: `DE.Views.PageSizeDialog`, `DE.Views.PageMarginsDialog`, `DE.Views.PageNumberingDlg` (page-number field insertion at current/any position), `DE.Views.CustomColumnsDialog` for custom column layouts, and `DE.Views.PoPosition` correct
- AND section behavior matches `Edit.textDifferentFirstPage`, `.textDifferentOddAndEvenPages`, `.textLinkToPrevious`, `.textContinueFromPreviousSection`

### Requirement: R-DE-IMAGESHAPE — image and shape settings SHALL match OnlyOffice

#### Scenario: WHEN the user formats an image, shape, or text art
- THEN `DE.Views.ImageSettings`/`DE.Views.ImageSettingsAdvanced` (size, rotation, wrapping, position, picture border/shadow), `DE.Views.ShapeSettings` (fill, line, shadow, autoshape), and `DE.Views.TextArtSettings` reproduce OnlyOffice (`Edit.textWrappingStyle`, `.textBehind`, `.textInFront`, `.textTight`, `.textThrough`, `.textInLine`, `.textMoveWithText`, `.textAllowOverlap`, `.textChangeShape`, `.textResetBackground`)
- AND chart objects open OnlyOffice chart settings: `DE.Views.ChartSettings` and `DE.Views.ChartSettingsDlg` expose the chart type/design/format surfaces (per `R-DE-IMAGESHAPE` scope: fill, border, layout, title/legend/axis options)
- AND the shared `Common.Views.ShapeShadowDialog`/`Common.Views.Draw` affordances apply

### Requirement: R-DE-REFS — table of contents and compare SHALL match OnlyOffice

#### Scenario: WHEN the user builds a TOC or compares documents
- THEN `DE.Views.TableOfContentsSettings` offers the OnlyOffice TOC options (levels, styles, page numbers, hyperlinks, update), with empty-TOC guidance (`Error.errorEmptyTOC`, `Error.errorNoTOC`)
- AND `DE.Views.CompareSettingsDialog` compares against an uploaded document with changes shown in the review surface (compare is disabled in co-editing: `Error.errorCompare`)

### Requirement: R-DE-MAILMERGE — mail merge SHALL match OnlyOffice

#### Scenario: WHEN the user runs mail merge (File → Mail Merge)
- THEN `DE.Views.MailMergeSettings` (data source, recipient list, merge fields, preview) and `DE.Views.MailMergeEmailDlg` (send emails to recipients with subject/body) reproduce OnlyOffice, with load/save/merge status via `LongActions.mailMergeLoadFile*`, `.sendMerge*`, `Error.errorMailMergeLoadFile`, `Error.errorMailMergeSaveFile`

### Requirement: R-DE-CONTROLS — form controls in DE SHALL match OnlyOffice

#### Scenario: WHEN the user inserts form controls in a fillable form
- THEN `DE.Views.ControlSettingsDialog` (text/checkbox/dropdown field properties), `DE.Views.FormSettings`, and `DE.Views.FormsTab` reproduce OnlyOffice (`Edit.textRequired`, `Error.errorTextFormWrongFormat`, `Error.errorSubmit`, `DE.ApplicationController.textSubmit`, `Toolbar.warnEmptyRequiredField`)

### Requirement: R-DE-LEFTRIGHT-PANELS — DE side panels SHALL match OnlyOffice

#### Scenario: WHEN the user opens a side panel
- THEN `DE.Views.LeftMenu`/`DE.Controllers.LeftMenu` provide the OnlyOffice left-menu icons (Navigation, Comments, Users, Search, Plugins, Accessibility) and `DE.Views.RightMenu` shows contextual panels (preview, review, comments, chart, shape, image, table, paragraph, textart, watermark, settings) exactly as OnlyOffice toggles them
- AND `DE.Views.DocumentHolder`/`DE.Controllers.Viewport` mount the collaborative surface with selection, cursors and co-author colors

### Requirement: R-DE-PRINT-STATUS — DE print preview and status bar SHALL match OnlyOffice

#### Scenario: WHEN the user prints or inspects status
- THEN `DE.Controllers.Print`/`DE.Views.PrintWithPreview` reproduces the print dialog (printer, copies, layout, pages, orientation, margins, scale) 
- AND `DE.Views.Statusbar`/`DE.Controllers.Statusbar` shows page count, zoom, language, word count, and review/user toggles as in OnlyOffice

---

## 9. Spreadsheet Editor (SSE)

### Requirement: R-SSE-CONTROLLERS — the SSE controller layer SHALL match OnlyOffice

#### Scenario: WHEN the spreadsheet editor runs
- THEN these controllers are mounted: `SSE.Controllers.ChartTab`, `SSE.Controllers.DataTab`, `SSE.Controllers.DocumentHolder`, `SSE.Controllers.FormulaDialog`, `SSE.Controllers.LeftMenu`, `SSE.Controllers.Main`, `SSE.Controllers.PivotTable`, `SSE.Controllers.Print`, `SSE.Controllers.Search`, `SSE.Controllers.SparklineTab`, `SSE.Controllers.Statusbar`, `SSE.Controllers.TableDesignTab`, `SSE.Controllers.Toolbar`, `SSE.Controllers.Viewport`
- AND `SSE.Views.LeftMenu`/`SSE.Views.RightMenu` provide the OnlyOffice side panels (navigation, comments, users, search, accessibility; and contextual format/insert panels for cells, images, shapes, charts, tables, pivots, sparklines)

### Requirement: R-SSE-TOOLBAR — the SSE toolbar tabs SHALL match OnlyOffice exactly

#### Scenario: WHEN the user views the SSE ribbon
- THEN `SSE.Views.Toolbar` shows exactly the OnlyOffice tab set: **File, Home, Insert, Layout, Formulas, Data, Review, View, Collaboration**, plus the contextual **Draw, Chart design, Formula, Table Design, Sparkline, Pivot Table, Protection** tabs when their object type is active, and the sheet **Tab color** affordance
- AND each tab exposes the OnlyOffice command groups (clipboard, font, alignment, number, formats, merge, conditional formatting, tables; insert cell/row/column/sheet/pivot/chart/image/shape/link/comment/header-footer/symbol; page setup, print areas, gridlines; function library incl. financial/logical/text/date&time/lookup&reference/math&trig/statistical/engineering/information/web, defined names, formula auditing, calculation; data tools incl. sort/filter/remove-duplicates/validate/consolidate/group/outline/get-external-data; spellcheck, protect, proofing; view incl. freeze panes/hide/show/zoom; macros under View)

### Requirement: R-SSE-FILEMENU — the SSE File menu SHALL match OnlyOffice

#### Scenario: WHEN the user opens File
- THEN `SSE.Views.FileMenu`/`SSE.Views.FileMenuPanels` offer New, Open, Save, Save As (xlsx/csv/ods/pdf/download-as), Print, Protect workbook/sheet, Info (`Settings.textSpreadsheetInfo`, `Settings.textSpreadsheetTitle`, `Settings.textAuthor`, `Settings.textCreated`, `Settings.textModifiedBy`-class fields, `Settings.textApplication`, `Settings.textCompany`-class fields), Feedback, and Back
- AND CSV export options follow OnlyOffice (`View.Settings.advCSVOptions`, `.textChooseCsvOptions`, `.textChooseDelimeter`, `.textDelimeter`, `.textEncoding`, `.txtComma`, `.txtSemicolon`, `.txtTab`, `.txtSpace`, `.txtColon`, `View.Settings.warnDownloadCsv`, `.warnDownloadAs`, `.warnDownloadOds`, `.txtDownloadCsv`)

### Requirement: R-SSE-VIEWTAB — SSE view/settings SHALL match OnlyOffice

#### Scenario: WHEN the user uses View or Settings
- THEN `SSE.Views.ViewTab` offers zoom, freeze panes, gridlines/headings toggles (`View.Settings.textHideGridlines`, `.textHideHeadings`), formula bar, R1C1 style (`View.Settings.textR1C1Style`), and interface theme
- AND `SSE.Views.MainSettingsPrint`/`SSE.Views.PrintWithPreview`/`SSE.Views.PrintSettings`/`SSE.Views.PrintTitlesDialog`/`SSE.Views.PageMarginsDialog`/`SSE.Views.ScaleDialog` reproduce OnlyOffice print/paging (print area, titles repeat rows/columns, fit-to-page, center on page)

### Requirement: R-SSE-HOME — SSE home-formatting dialogs SHALL match OnlyOffice

#### Scenario: WHEN the user formats cells or applies conditional rules
- THEN `SSE.Views.CellSettings` (number format, alignment, font, borders, fill, protection preset), `SSE.Views.CellRangeDialog`, `SSE.Views.SetValueDialog`, `SSE.Views.ParagraphSettings`/`SSE.Views.ParagraphSettingsAdvanced` (in-cell formatting), `SSE.Views.AdvancedSeparatorDialog` (thousands/decimal separators), `SSE.Views.SpecialPasteDialog` (paste values/formats/transpose/skip blanks), and `SSE.Views.FillSeriesDialog` (linear/growth/date series) reproduce OnlyOffice
- AND conditional formatting (`SSE.Views.FormatRulesManagerDlg`, `SSE.Views.FormatRulesEditDlg`), top/bottom rules (`SSE.Views.Top10FilterDialog`), data validation (`SSE.Views.DataValidationDialog`), spellcheck (`SSE.Views.Spellcheck`), and remove-duplicates (`SSE.Views.RemoveDuplicatesDialog`) match OnlyOffice, with errors `Error.errorDataValidate`, `Error.errorRemoveDuplicates`-class behavior

### Requirement: R-SSE-INSERT — SSE insert SHALL match OnlyOffice

#### Scenario: WHEN the user inserts objects
- THEN `SSE.Views.ImageSettings`/`SSE.Views.ImageSettingsAdvanced`, `SSE.Views.ShapeSettings`/`SSE.Views.ShapeSettingsAdvanced`, `SSE.Views.TextArtSettings`, `SSE.Views.HyperlinkSettingsDialog`, `SSE.Views.HeaderFooterDialog`, and `SSE.Views.FieldSettingsDialog` (function/field insertion) reproduce OnlyOffice
- AND external data import follows OnlyOffice: `SSE.Views.ImportFromXmlDialog` (XML map import) and `SSE.Views.ExternalLinksDlg` (link refresh/break)

### Requirement: R-SSE-NUMBERS — SSE data-type formatting SHALL match OnlyOffice

#### Scenario: WHEN the user formats numbers/currency/date
- THEN number format creation follows `View.Edit.textCreateCustomFormat`, `.textCustomFormat`, `.textEnterFormat`, `.textCreateFormat`, `.textCurrency`, `.textAccounting`, `.textDate`, `.textTime`, `.textScientific`, `.textFraction`, `.textTextFormat`, `.textNumber`, `.textGeneral`, `.textValue`, `.textCustomFormatWarning`, and `.textErrorMsg`/`.textErrorTitle`/`.textEmptyItem`

### Requirement: R-SSE-CHARTS — SSE chart creation/editing SHALL match OnlyOffice

#### Scenario: WHEN the user creates or edits a chart
- THEN the SSE chart surface (`SSE.Controllers.ChartTab`, `SSE.Views.ChartTab`, `SSE.Views.ChartSettings`, `SSE.Views.ChartSettingsDlg`, `SSE.Views.ChartTypeDialog`, `SSE.Views.ChartDataDialog`, `SSE.Views.ChartDataRangeDialog`, `SSE.Views.ChartWizardDialog`, `SSE.Views.ChartSettings`-class) supports all `Common.define.chartData` types and the full Chart design tab (change chart type, edit data range, switch row/column, quick layout, colors, styles), with combo-chart constraints (`Error.errorComboSeries`) and stock-order validation (`Error.errorStockChart`)
- AND the shared `Common.Controllers.ChartTab`/`Common.Views.ChartTab`/`Common.Views.Charts3DDlg` providers back SSE, DE, and PE

### Requirement: R-SSE-FORMULAS — formula tools SHALL match OnlyOffice

#### Scenario: WHEN the user works with formulas
- THEN `SSE.Controllers.FormulaDialog`/`SSE.Views.FormulaDialog`, `SSE.Views.FormulaTab`, `SSE.Views.FormulaWizard`, `SSE.Views.NameManagerDlg`, `SSE.Views.NamedRangeEditDlg`, `SSE.Views.NamedRangePasteDlg`, and the cell formula bar (`SSE.Views.CellEditor`) reproduce OnlyOffice (function categories per `View.Add.sCat*`, defined names, formula auditing, error classes `View.Add.errorMaxRows`, `Error.errorFrmlMaxLength`, `.errorFrmlMaxTextLength`, `.errorFrmlMaxReference`, `.errorFrmlWrongReferences`, `.errorCircularReference`, `.errorFormulaParsing`, `.errorOperandExpected`, `.errorWrongBracketsCount`, `.errorWrongOperator`, `.errorFormulaName`, `.errorInvalidRef`, `.errorArgsRange`, `.errorMultiCellFormula`, `.errorCountArg`, `.errorCountArgExceed`)

### Requirement: R-SSE-DATA — data tools SHALL match OnlyOffice

#### Scenario: WHEN the user sorts/filters/validates data
- THEN `SSE.Views.DataTab` provides the OnlyOffice Data-tab command surface (sort, filter, remove duplicates, validation, consolidate, group/outline, get external data) wired to the Data-tab controller
- AND `SSE.Views.SortDialog`, `SSE.Views.SortFilterDialog`, `SSE.Views.SortOptionsDialog`, `SSE.Views.AutoFilterDialog`, `SSE.Views.DigitalFilterDialog`, and the filter/sort context entries (`ContextMenu.menuSortLow2High`-class per `View.Edit.txtSortHigh2Low`, `.txtSortLow2High`) reproduce OnlyOffice
- AND filter-error classes match `View.Add.txtLockSort`, `.txtSortSelected`, `.txtExpandSort`, `.txtExpand`, `Error.errorAutoFilterChange`, `.errorAutoFilterChangeFormatTable`, `.errorAutoFilterDataRange`, `.errorAutoFilterHiddenRange`, `.errorFTChangeTableRangeError`, `.errorFTRangeIncludedOtherTables`, `.errorChangeFilteredRange`, `.errorChangeArray`, `.errorFillRange`, `.errorMoveRange`, `.errorPasteMaxRange`, `.errorPasteInPivot`, `.errorPasteSlicerError`, `Error.pastInMergeAreaError`, `.errorSingleColumnOrRowError`, `.errorNoDataToParse`, `.errorFillOtherRows`-class fill hints and `Error.textFormulaFilled*` notices

### Requirement: R-SSE-TABLES — SSE table tools SHALL match OnlyOffice

#### Scenario: WHEN the user styles a data range as a table
- THEN `SSE.Controllers.TableDesignTab`/`SSE.Views.TableDesignTab` and `SSE.Views.TableOptionsDialog` (name, banded rows/columns, header/total row, filter button) reproduce OnlyOffice
- AND `SSE.Views.TableSettingsAdvanced` covers further table properties

### Requirement: R-SSE-PIVOT — pivot tables SHALL match OnlyOffice

#### Scenario: WHEN the user builds a pivot table
- THEN `SSE.Controllers.PivotTable`/`SSE.Views.PivotTable`, `SSE.Views.CreatePivotDialog`, `SSE.Views.PivotSettings`/`SSE.Views.PivotSettingsAdvanced`, `SSE.Views.PivotGroupDialog`, `SSE.Views.PivotCalculatedItemsDialog`, `SSE.Views.PivotInsertCalculatedItemDialog`, `SSE.Views.PivotDigitalFilterDialog`, `SSE.Views.PivotShowDetailDialog`, and `SSE.Views.ValueFieldSettingsDialog` reproduce OnlyOffice (filters, rows/columns/values, calculated fields/items, group by date, show detail), with pivot errors (`Error.errorPivotOverlap`, `.errorPivotGroup`, `.errorPivotFieldNameExists`, `.errorFormulaInPivotFieldName`, `.errorLockedCellPivot`, `.errorPivotWithoutUnderlying`, `.errorLabledColumnsPivot`, `.errorChangeArray`)

### Requirement: R-SSE-SLICERS — slicers SHALL match OnlyOffice

#### Scenario: WHEN the user adds or formats a slicer
- THEN `SSE.Views.SlicerAddDialog`, `SSE.Views.SlicerSettings`, and `SSE.Views.SlicerSettingsAdvanced` reproduce OnlyOffice (columns, height, style, caption), with errors `Error.errorMoveSlicerError`, `.errorPasteSlicerError`

### Requirement: R-SSE-SPARKLINES — sparklines SHALL match OnlyOffice

#### Scenario: WHEN the user inserts a sparkline
- THEN `SSE.Controllers.SparklineTab`/`SSE.Views.SparklineTab` and `SSE.Views.CreateSparklineDialog` reproduce OnlyOffice (line/column/win-loss types, data range, location, style, axis, markers)

### Requirement: R-SSE-ANALYSIS — goal seek, solver, watch SHALL match OnlyOffice

#### Scenario: WHEN the user runs what-if analysis
- THEN `SSE.Views.GoalSeekDlg`/`SSE.Views.GoalSeekStatusDlg`, `SSE.Views.SolverDlg`/`SSE.Views.SolverMethodDialog`/`SSE.Views.SolverResultsDlg`, and `SSE.Views.WatchDialog` reproduce OnlyOffice (target cell/value, adjustable cells, constraints per `SSE.Views.ConstraintDialog`, solution report)
- AND constraints editing matches `SSE.Views.ConstraintDialog`

### Requirement: R-SSE-HOME-STATUS — SSE status bar and sheet tabs SHALL match OnlyOffice

#### Scenario: WHEN the user inspects the sheet
- THEN `SSE.Views.Statusbar`/`SSE.Controllers.Statusbar` shows cells, selection stats (sum/avg/min/max/count), zoom, and the sheet-tab management menu (`Statusbar.textRenameSheet`, `.textRename`, `.textSheet`, `.textSheetName`, `.textTabColor`, `.textHidden`, `.textHide`, `.textUnhide`, `.textUnhideSheets`, `.textMove`, `.textMoveBefore`, `.textMoveToEnd`, `.textDuplicate`, `.textDelete`, `.textMore`, `.textErrorLastSheet`, `.textErrorRemoveSheet`, `.textWarnDeleteSheet`, `.textErrNameExists`, `.textErrNameWrongChar`, `.textErrNotEmpty`, `.warnAddSheetCsv`, `.textContinue`, `.textCancel`, `.textOk`, `Statusbar.notcriticalErrorTitle`) matching OnlyOffice
- AND `SSE.Views.DocumentHolder`/`SSE.Controllers.DocumentHolder` mount the grid, freeze panes, and collaborative cursors
- AND workbook views (`SSE.Views.ViewManagerDlg`) manage named custom views

---

## 10. Presentation Editor (PE)

### Requirement: R-PE-CONTROLLERS — the PE controller layer SHALL match OnlyOffice

#### Scenario: WHEN the presentation editor runs
- THEN these controllers are mounted: `PE.Controllers.DocumentHolder`, `PE.Controllers.LeftMenu`, `PE.Controllers.Main`, `PE.Controllers.Print`, `PE.Controllers.Search`, `PE.Controllers.Statusbar`, `PE.Controllers.Toolbar`, `PE.Controllers.Viewport`, and `PE.Views.DocumentHolder`/`PE.Views.DocumentPreview`

### Requirement: R-PE-TOOLBAR — the PE toolbar tabs SHALL match OnlyOffice exactly

#### Scenario: WHEN the user views the PE ribbon
- THEN `PE.Views.Toolbar` shows exactly the OnlyOffice tab set: **File, Home, Insert, Draw, Transitions, Animation, Design, Slide Master, View, Collaboration**, plus the contextual **Chart design, Protection** tabs when their object type is active, and the slide **Tab color** is configurable
- AND `PE.Views.ViewTab` offers zoom, notes, gridlines, guides, slide-show-from-current, interface theme, and the OnlyOffice view/settings toggles
- AND each tab exposes the OnlyOffice command groups (clipboard, font, paragraph, arrange, slide; insert table/image/shape/text box/chart/audio/video/link/comment; transitions gallery + transition settings; animation gallery + animation pane; design gallery, slide size, background; master edits; view toggles incl. notes, gridlines, guides, zoom; macros under View)

### Requirement: R-PE-FILEMENU — the PE File menu SHALL match OnlyOffice

#### Scenario: WHEN the user opens File
- THEN `PE.Views.FileMenu`/`PE.Views.FileMenuPanels` offer New, Open, Save, Save As (pptx/odp/pdf/download-as), Print, Protect, Info (`View.Settings.textPresentationInfo`, `.textPresentationTitle`, `Settings.textAuthor`, `.textCreated`, `.textModifiedBy`-class fields), Feedback, and Back, plus slideshow Quick Start

### Requirement: R-PE-SLIDE — slide management SHALL match OnlyOffice

#### Scenario: WHEN the user manages slides
- THEN `PE.Views.LeftMenu`/`PE.Controllers.LeftMenu` (slide thumbnails, add/duplicate/delete slide via `View.Edit.textAddSlide`-class and `View.Edit.textDuplicateSlide`, `.textDeleteSlide`), `PE.Views.SlideSettings`, `PE.Views.SlideSizeSettings` (standard, wide, custom, orientation per `View.Settings.mniSlideStandard`, `.mniSlideWide`, `.mniSlideLandscape`, `.mniSlidePortrait`), and `PE.Views.SlideMasterTab` reproduce OnlyOffice
- AND slide background/design follow `PE.Views.GridSettings` (gridlines/guides) and `PE.Views.SlideSettings`

### Requirement: R-PE-TRANSITIONS — slide transitions SHALL match OnlyOffice

#### Scenario: WHEN the user applies a transition
- THEN `PE.Views.Transitions` offers the full OnlyOffice transition catalogue (None, Blinds, Box, Box Zoom, Checker, Circle, Clock, Clockwise, Comb, Counterclockwise, Cover, Cube, Cut, Diamond, Dissolve, Doors, Fade, Ferris Wheel, Flip, Gallery, Honeycomb, Morph, Orbit, Plus, Push, Random, Random Bars, Ripple, Rotate, Split, Switch, UnCover, Vortex, Wedge, Window, Wipe, Zoom; directional variants per `Edit.textFromLeft`-class; through-black), with duration/delay (`View.Edit.textDuration`, `.textDelay`), sound, apply-to-all, and preview (`View.Edit.textPreview`)
- AND transition effect-direction strings match `View.Edit.textFromBottom`, `.textFromTop`, `.textFromLeft`, `.textFromRight`, `.textFromTopLeft`, `.textFromBottomLeft`, `.textFromTopRight`, `.textFromBottomRight`, `.textFromCenter`, `.textVerticalIn`, `.textVerticalOut`, `.textHorizontalIn`, `.textHorizontalOut`, `.textMorph`, `.textMorphObjects`, `.textMorphWords`, `.textMorphLetters`, `.textSmoothly`, `.textThroughBlack`, `.textDynamicContent`

### Requirement: R-PE-ANIMATION — animations SHALL match OnlyOffice

#### Scenario: WHEN the user animates an object
- THEN `PE.Views.Animation`/`PE.Views.AnimationDialog` reproduce the OnlyOffice animation surface covering all `Common.define.effectData` families (199 effect families: 1/2/3/4-Spoke, 4/5-Point Star, Appear variants, Blinds, Box, Circle, Diamond, Dissolve, Fade, Flash, Fly In, Float, Grow/Shrink, Paths, Random Effects, Spin, Switch, Teeter, Whip, Zoom, …), with start on click/tap/with previous/after previous (`View.Edit.textStartOnClick`, `.textStartOnTap`), duration, delay, and effect options
- AND the animation preview and order list render like OnlyOffice

### Requirement: R-PE-HOMEOBJECTS — PE object formatting SHALL match OnlyOffice

#### Scenario: WHEN the user formats PE objects
- THEN `PE.Views.ParagraphSettings`/`PE.Views.ParagraphSettingsAdvanced`, `PE.Views.ImageSettings`/`PE.Views.ImageSettingsAdvanced`, `PE.Views.ShapeSettings`/`PE.Views.ShapeSettingsAdvanced`, `PE.Views.TextArtSettings`, `PE.Views.ChartSettings`/`PE.Views.ChartSettingsAdvanced`/`PE.Views.ChartSettingsDlg`, `PE.Views.TableSettings`/`PE.Views.TableSettingsAdvanced`, `PE.Views.DateTimeDialog`, and `PE.Views.RightMenu`-hosted contextual format panels reproduce OnlyOffice
- AND header/footer (`PE.Views.HeaderFooterDialog`), hyperlinks (`PE.Views.HyperlinkSettingsDialog`), and notes reproduce OnlyOffice

### Requirement: R-PE-SLIDESHOW — slideshow settings SHALL match OnlyOffice

#### Scenario: WHEN the user configures or runs a slideshow
- THEN `PE.Views.SlideshowSettings` (show type, loop, advance timing, pen color, display presenter view) matches OnlyOffice, incl. `View.Settings.textLoopSlideshow`
- AND `PE.Views.SignatureSettings` covers presentation signing

### Requirement: R-PE-PRINT-STATUS — PE print and status SHALL match OnlyOffice

#### Scenario: WHEN the user prints or inspects state
- THEN `PE.Controllers.Print`/`PE.Views.PrintWithPreview` reproduces the OnlyOffice presentation print flow (slides per page incl. notes/handouts) 
- AND `PE.Views.Statusbar`/`PE.Controllers.Statusbar` shows slide count, zoom, fit-to-slide, and presenter controls

---

## 11. PDF Editor (PDFE)

### Requirement: R-PDF-CONTROLLERS — the PDFE controller layer SHALL match OnlyOffice

#### Scenario: WHEN the PDF editor runs
- THEN these controllers are mounted: `PDFE.Controllers.InsTab`, `PDFE.Controllers.LeftMenu`, `PDFE.Controllers.Main`, `PDFE.Controllers.Navigation`, `PDFE.Controllers.Print`, `PDFE.Controllers.RedactTab`, `PDFE.Controllers.Search`, `PDFE.Controllers.Statusbar`, `PDFE.Controllers.Toolbar`, `PDFE.Controllers.Viewport`

### Requirement: R-PDF-TOOLBAR — the PDFE toolbar tabs SHALL match OnlyOffice exactly

#### Scenario: WHEN the user views the PDFE ribbon
- THEN `PDFE.Views.Toolbar` shows exactly the OnlyOffice tab set: **File, Home, Comment, Insert, Edit, Redact, View**, plus the contextual **Forms, Collaboration** and **Chart design** tabs when appropriate
- AND each tab exposes the OnlyOffice command groups (selection, hand, zoom, page nav, text select; comment add/highlight/sticky note; insert image/shape/text art/table/hyperlink; edit text/images (with OCR toggle); redact text/images/pages; view toggles, dark mode, interface theme)
- AND `PDFE.Controllers.InsTab`/`PDFE.Views.InsTab` back the Insert tab and `PDFE.Controllers.RedactTab`/`PDFE.Views.RedactTab` the Redact tab

### Requirement: R-PDF-FILEMENU — the PDFE File menu SHALL match OnlyOffice

#### Scenario: WHEN the user opens File
- THEN `PDFE.Views.FileMenu`/`PDFE.Views.FileMenuPanels` offer Open, Save, Save As (pdf/docx/xlsx/pptx/txt/odt…), Print, Download, Info (`Settings.textPdfInfo`-class: `Settings.textPdfVer`, `.textPdfProducer`, `.textPdfTagged`), Feedback, and Back
- AND conversion warnings match `Main.warnDownloadAsPdf`/`Settings.warnDownload*`

### Requirement: R-PDF-FORMS — PDF form filling/creation SHALL match OnlyOffice

#### Scenario: WHEN the user fills or creates a PDF form
- THEN `PDFE.Views.FormsTab` and `PDFE.Views.FormSettings` reproduce the OnlyOffice form-field set: text, checkbox, radio, combo box, list box, date & time, image, and the masked/auto fields (phone number, email address, ZIP code, credit card number), with field validation (`Error.errorTextFormWrongFormat`) and next/previous-field navigation ("Go to the next field"/"Go to the previous field")
- AND form-creation errors match `Error.errorPDFFormsLocked` and `Error.errorSubmit`

### Requirement: R-PDF-REDACT — redaction SHALL match OnlyOffice

#### Scenario: WHEN the user redacts content
- THEN `PDFE.Controllers.RedactTab`/`PDFE.Views.RedactTab` reproduce OnlyOffice (redact text/images/pages, search-redact, mark-up state, apply) with the OnlyOffice redaction confirmation and sanitization warnings
- WHEN pages are reordered/rotated
- THEN `PDFE.Views.PageThumbnails` provides the OnlyOffice thumbnails panel (reorder, rotate, delete, insert)

### Requirement: R-PDF-HOME — PDFE home/insert/edit SHALL match OnlyOffice

#### Scenario: WHEN the user formats objects in a PDF
- THEN `PDFE.Views.ParagraphSettings`/`PDFE.Views.ParagraphSettingsAdvanced`, `PDFE.Views.ImageSettings`/`PDFE.Views.ImageSettingsAdvanced`, `PDFE.Views.ShapeSettings`/`PDFE.Views.ShapeSettingsAdvanced`, `PDFE.Views.TextArtSettings`, `PDFE.Views.TableSettings`/`PDFE.Views.TableSettingsAdvanced`, `PDFE.Views.ChartSettings`/`PDFE.Views.ChartSettingsAdvanced`/`PDFE.Views.ChartSettingsDlg`, `PDFE.Views.FormatSettingsDialog`, and `PDFE.Views.HyperlinkSettingsDialog` reproduce OnlyOffice
- AND `PDFE.Views.DocumentHolder`/`PDFE.Views.LeftMenu`/`PDFE.Views.RightMenu`/`PDFE.Views.Navigation`/`PDFE.Views.ViewTab`/`PDFE.Views.Statusbar`/`PDFE.Views.PrintWithPreview` behave per the PDFE chrome described above

---

## 12. Visio Editor (VE)

### Requirement: R-VE-CONTROLLERS — the VE controller layer SHALL match OnlyOffice

#### Scenario: WHEN the visio editor runs
- THEN these controllers are mounted: `VE.Controllers.LeftMenu`, `VE.Controllers.Main`, `VE.Controllers.Print`, `VE.Controllers.Search`, `VE.Controllers.Statusbar`, `VE.Controllers.Toolbar`

### Requirement: R-VE-TOOLBAR — the VE toolbar SHALL match OnlyOffice exactly

#### Scenario: WHEN the user views the VE chrome
- THEN `VE.Views.Toolbar` shows exactly the OnlyOffice tab set: **File, Home, Insert, Page Layout, Data, Review, View** (per VE locale: File/Home/Insert/Page Layout/Data/Review/View), and `VE.Views.ViewTab` covers zoom and view toggles
- AND `VE.Views.FileMenu`/`VE.Views.FileMenuPanels` offer New/Open/Save/Save As/Print/Info/Feedback
- WHEN the user works on a drawing
- THEN `VE.Views.Statusbar` shows zoom and selection info, `VE.Views.LeftMenu` the stencil/shapes panel, `VE.Views.DocumentHolder` the drawing surface, and `VE.Views.PrintWithPreview` the print flow, matching OnlyOffice

---

## 13. Viewer Mode, Embed, and Mobile Scope

### Requirement: R-VIEWER-MODE — viewer/read-only mode SHALL match OnlyOffice

#### Scenario: WHEN a file opens in view-only mode (no edit rights, or locked)
- THEN every editor renders in the OnlyOffice read-only chrome: editing commands disabled, `Main.titleReadOnly`, `Common.Translation.tipFileReadOnly`, `Common.Translation.tipFileLocked`/`warnFileLocked` when applicable, comment/annotation entry points remain per OnlyOffice (`Main.textDialogProtectedOnlyView`, `Main.textDialogProtectedEditComments`, `Main.textDialogProtectedChangesTracked`, `Main.textDialogProtectedFillForms`)
- AND `Main.warnProcessRightsChange` explains permission changes

### Requirement: R-VIEWER-EMBED — embed/viewer variant SHALL match OnlyOffice

#### Scenario: WHEN the editor is embedded (iframe)
- THEN the embed chrome uses the `embed` locale surfaces: per-app `x.ApplicationView` command strings (download, print, search, share, embed, full screen, file location) and the flat `x.ApplicationController` strings (see R-GLOB-APPCONTROLLER), plus `common.view.SearchBar`/`common.view.modals` for embedded search and modal chrome
- AND `Common.Views.EmbedDialog`/`Common.Views.ShareDialog` provide the OnlyOffice embed-code and share dialogs

### Requirement: R-VIEWER-MOBILE — mobile web SHALL match OnlyOffice scoping

#### Scenario: WHEN the user opens the editor on a mobile viewport
- THEN the mobile variant renders with the mobile section strings (`About`, `Add`, `ContextMenu`, `Draw`, `Edit`, `Error`, `LongActions`, `Main`, `Settings`, `Statusbar`, `Toolbar`, `View.Add`, `View.Edit`, `View.Settings`, `Controller.Main`, `Main.SDK`) and offers the Standard/Mobile view switch (`Toolbar.textSwitchedMobileView`, `.textSwitchedStandardView`, `.textSwitchToDesktop`, `Settings.textMobileView`, `Toolbar.btnRestartNow`)
- AND the legacy `cancelButtonText` key resolves correctly for cancel buttons

---

## 14. Editor Configuration and Host-Integration Surface

### Requirement: R-CFG-API — the host integration surface (WOPI/hosting API) SHALL expose the OnlyOffice editor-configuration knobs

The World-Office docserver's editor host page SHALL accept and honor the same configuration surface that OnlyOffice's `DocumentServer/web-apps/apps/api/documents/api.js` exposes to WOPI hosts (verified: 51 `customization` references in the oracle build).

#### Scenario: WHEN a host opens the editor with a config object
- THEN the config supports: `autosave`, `forcesave`, `spellcheck`, `compactHeader`, `toolbarNoTabs`, `hideRulers`, `hideRightMenu`/`hideLeftMenu`, `uiTheme` (with `Themes` light/dark/system tie-in), `customer` (name/logo) with `loaderLogo`, `goback` (URL + requestClose), `macros`, `mention`, `anonymous`, `feedback` (hide), `integrationMode` (embed vs. editor), and `mention` — exactly the knobs the oracle api.js consumes
- AND the World-Office editor applies each knob with OnlyOffice-equivalent behavior (e.g. `forcesave` triggers a PutFile on beforeunload; `toolbarNoTabs` renders the compact single-row toolbar; `hideRulers` strips rulers from the Layout/View chrome)

### Requirement: R-CFG-COEDIT — co-editing modes SHALL match OnlyOffice

#### Scenario: WHEN the host selects a co-editing mode
- THEN fast mode delivers instant collaborative updates with the OnlyOffice fast-mode semantics (undo/redo disabled: `Common.Collaboration.textTryUndoRedo`), and strict mode serializes changes with per-character/object locks matching OnlyOffice
- AND co-author presence, cursors and selections render with OnlyOffice colors and `Common.Collaboration.textEditUser`/`.textUsers` attribution

---

## 15. Verification and Acceptance

### Requirement: R-VERIFY-MECHANICAL — component coverage SHALL be re-verified on every inventory change

#### Scenario: WHEN the oracle inventory is regenerated or the oracle version changes
- THEN run `/usr/bin/python3 generate-inventory.py` (regenerates `inventory/*.md`, `inventory/_coverage.json`, `inventory/enums.md`) and `/usr/bin/python3 check-coverage.py`
- AND `check-coverage.py` MUST print `OK: 100% component coverage in spec.md` before the spec is considered in force

### Requirement: R-VERIFY-ORACLE-SESSION — spot-check parity against the live oracle

#### Scenario: WHEN a parity claim is disputed
- THEN open the same document side-by-side in the oracle harness (`http://onlyoffice.test:8080` via `~/workspace/nextcloud/`) and in the World-Office editor
- AND compare dialog-by-dialog against `inventory/<app>-<variant>.md` for the disputed feature
- AND any behavioral divergence not captured by the inventory is recorded here as a requirement amendment (spec-driven change), not silently fixed in code

### Requirement: R-VERIFY-AUTOMATION — parity checking SHALL be scriptable

#### Scenario: WHEN automated verification runs
- THEN a checker may diff the rendered DOM/command-ids of the World-Office editor against the OnlyOffice command catalogue implicit in the locale keys (e.g. every `*Btn*`/`capBtn*`/`menu*` key maps to a present control id)
- AND regressions fail loudly with the missing control id and its locale key

---

## Appendix A — Scope Exclusions

The following are NOT part of this parity target (explicitly out of scope; separate specs cover them):

- Document Server server-side administration (converter, metrics, JWT, clustering)
- Desktop application chrome (system menus, native file dialogs, tray) — `Common.Controllers.Desktop` here refers only to the in-browser desktop-view controller
- Print-production / typesetting engines (only the print preview dialogs are in scope)
- Native mobile apps (only the mobile *web* variant surfaces are in scope, §13)
- Backend format fidelity (ODF/ECMA-376 conformance is tracked in `plan/specs/document-server/spec.md` and `server/core/crates/wo-conformance`)
- Host-side file management (files app, sharing, versioning UI of the cloud backend)

## Appendix B — Inventory Totals (oracle build, regenerated 2026-09-07)

| app/variant       | keys | components |
|-------------------|------|-----------|
| documenteditor/main | 4479 | 159 |
| documenteditor/mobile | 821 | 16 |
| documenteditor/embed | 79 | 70 |
| documenteditor/forms | 218 | 16 |
| spreadsheeteditor/main | 5393 | 180 |
| spreadsheeteditor/mobile | 877 | 15 |
| spreadsheeteditor/embed | 59 | 52 |
| presentationeditor/main | 3707 | 124 |
| presentationeditor/mobile | 598 | 15 |
| presentationeditor/embed | 59 | 52 |
| pdfeditor/main | 3167 | 100 |
| visioeditor/main | 482 | 47 |
| visioeditor/mobile | 194 | 10 |
| visioeditor/embed | 60 | 53 |
| **total** | **20193** | **909** |

612 unique component classes — every one named in backticks above; enforced by `check-coverage.py`.
