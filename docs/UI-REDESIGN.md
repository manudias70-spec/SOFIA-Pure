# SOFIA-Pure — UI Redesign

## Objective

Modernize the SOFIA-Pure user interface while preserving the DOSBox Pure engine, emulator behavior, existing commands, input handling, and compatibility.

The redesign is presentation-only unless a later change is explicitly reviewed and approved.

## Visual direction

**Modern Retro DOS**: a contemporary desktop interface with the clarity and restraint of Windows 11 / Fluent, grounded in classic DOS and PC aesthetics.

- Dark navy / graphite surfaces.
- Cyan and electric-blue accents used for focus, selection, and active states.
- Subtle borders and restrained translucency; avoid heavy blur and excessive glow.
- Clear typography and generous spacing.
- Responsive, resizable window; fullscreen remains an option, not a requirement.
- Sofi mascot appears as a companion panel, never covering the game, menus, or file content.

## Main application layout

1. **Navigation rail** — Inicio, Biblioteca, Explorador, Favoritos, Configuración.
2. **Main workspace** — contextual content for the selected section.
3. **Sofi panel** — compact assistant/mascot area with contextual hints and status; collapsible when more workspace is needed.
4. **Status bar** — emulator state and relevant mounted-drive / media information, using existing data only.

## Explorer direction (later phase)

A modern Norton Commander-inspired browser:
- Optional dual-pane mode.
- Real directory and drive navigation.
- File operations exposed only where the existing application supports them.
- No mandatory cover-art database or per-game recognition catalogue.
- Keyboard navigation remains first-class.

## Implementation boundaries

### Frontend repository
SOFIA-Pure contains the standalone application and its presentation/integration code. Changes here must be limited to the application UI and presentation layer.

### Emulator OSD
The DOSBox Pure on-screen menu is drawn by the OSD module in the DOSBox Pure source tree. The SOFIA-Pure frontend receives and displays the OSD frame; it does not author the menu contents itself.

Therefore:
- Do not try to redesign the OSD by changing emulator behavior or frame-processing logic in main.cpp.
- Treat the OSD drawing module as a separate UI-only workstream.
- Keep core execution, CPU/device emulation, timing, audio, input semantics, and libretro behavior untouched.

## Phased plan

### Phase 1 — Audit and visual specification
- Map each existing screen, menu, dialog, and action to its current implementation.
- Record existing behavior and keyboard/controller shortcuts before changing presentation.
- Define colors, spacing, typography, focus, hover, disabled, and selected states.

### Phase 2 — Existing menus
- Restyle existing menus and dialogs without removing or renaming functionality.
- Preserve all current actions and navigation paths.
- Compare before/after behavior for each screen.

### Phase 3 — Main desktop shell
- Introduce the navigation rail, workspace, collapsible Sofi panel, and status bar.
- Keep the emulator surface and its lifecycle unchanged.

### Phase 4 — Explorer
- Build the Norton Commander-inspired file/game explorer on top of existing filesystem capabilities.
- Add dual-pane navigation as an optional presentation mode.

### Phase 5 — Validation
- Build and run after each isolated change.
- Check keyboard, mouse, controller, resizing, fullscreen, OSD visibility, audio, and game execution.
- Review the diff to ensure no emulator/core logic was altered.

## Non-negotiable rule

**Change how SOFIA-Pure looks and how its existing UI is arranged; do not change what the emulator does.**

Any change that appears to require engine or behavior modifications must be isolated and discussed before implementation.
