# SOFIA-Pure — Frontend UI Audit

Branch reviewed: feature/sofia-ui-redesign

## What the current application actually is

The current SOFIA-Pure repository is a standalone DOSBox Pure application, not a separate game-library launcher. Its main window is initialized in the ZillaLib application class and the application loads the emulator directly.

The visible application surface currently consists of:
- The emulated game/video surface.
- The DOSBox Pure OSD frame, received as a bitmap and drawn over the game.
- Emulator notifications and transient status text.
- Optional throttle indicators and developer diagnostics.
- A short animated startup logo.

There is no existing left navigation rail, game-library home screen, or separate launcher workspace in this codebase. Those would be a future product layer, not a restyle of an existing screen.

## Relevant implementation map

### Window and startup
- sDOSBoxPure::Load() initializes the resizable display, input, font, settings, and emulator startup.
- Window title is currently DOSBox Pure.
- Initial window size defaults to 1280 × 720 when no valid saved size is present.
- Fullscreen and maximized modes are controlled by existing settings.

### Emulator video
- retro_video_refresh_cb() updates core texture scaling information.
- srfCore stores and displays the emulator video surface.
- OnDraw() draws the game surface using the existing geometry and optional CRT/scaling shader.

### On-screen display (OSD)
- DBPS_SubmitOSDFrame() receives the OSD bitmap from DOSBox Pure and uploads it to srfOSD.
- OnDraw() positions and fades that bitmap over the game surface.
- The actual menu contents and their visual design are produced by the DOSBox Pure OSD drawing module, not by the frontend's OnDraw() routine.

### Notifications and overlays
- RETRO_ENVIRONMENT_SET_MESSAGE_EXT receives status and notification messages.
- OnDraw() draws transient notifications, throttle-state indicators, and optional developer diagnostics.

### Startup logo
- DrawIntro() displays the embedded animated DOSBox Pure logo.
- It is called once from OnDraw() after startup.

## Safe frontend-only opportunities

1. Application identity: review the window title and application-facing branding, while preserving upstream attribution and licensing.
2. Startup presentation: consider a SOFIA-Pure identity treatment that does not delay or interfere with emulator startup.
3. Notification styling: adjust only frontend-drawn notification backgrounds, spacing, and colors while retaining message text, severity, timing, and behavior.
4. Status overlays: refine visual treatment without changing the underlying throttle, pointer-lock, or emulator state logic.
5. Window presentation: review default dimensions and saved window behavior without changing emulator geometry or display semantics.

## Separate OSD workstream

The OSD bitmap is rendered upstream. To redesign its menu panels, buttons, selection states, and typography, the OSD drawing source from the DOSBox Pure Codeberg repository must be available in an editable branch/fork. Do not approximate this by modifying the frontend's OSD texture upload or game-rendering path.

## Recommended order

1. Finish mapping the existing OSD menu screens and their actions.
2. Make a visual-only OSD palette/layout proposal.
3. Apply the OSD redesign in a dedicated engine-UI branch, with no changes to emulation logic.
4. Separately make small frontend identity/notification refinements in SOFIA-Pure.
5. Only after that, decide whether a standalone game-library launcher is a desired new feature.

## Preservation checklist

- No changes to CPU, memory, devices, timing, audio mixing, input mapping, libretro callbacks, game loading, save states, or filesystem behavior.
- Preserve all existing OSD actions and keyboard/controller navigation.
- Keep the game video path and OSD bitmap transfer intact.
- Validate window resize, fullscreen, mouse capture, notifications, and game execution after each UI-only change.
