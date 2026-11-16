# SOFIA-Pure — Dear ImGui Integration Spike

Status: architecture investigation only. No application source, build configuration, or emulator code has been changed.

Target branch: `feature/sofia-ui-redesign`

## Decision

Keep ZillaLib as the application/window/rendering host for the first integration experiment. Do not replace it as part of the initial UI redesign.

Evaluate Dear ImGui as an optional presentation layer rendered after the existing game/OSD composition. The integration must be isolated behind a small SOFIA-Pure UI adapter so it can be disabled at build time and removed without affecting the emulator.

## What the current frontend confirms

- The application derives `sDOSBoxPure` from `ZL_Application`.
- Window creation, input initialization, key events, resize notifications, joystick setup, and the application frame lifecycle are managed through ZillaLib.
- The frame callback is `AfterFrame()`, which calls `OnDraw()`.
- `OnDraw()` runs `retro_run()`, resets the GL framebuffer, then draws the game surface, OSD bitmap, notifications, and diagnostics.
- DOSBox Pure supplies the OSD bitmap through `DBPS_SubmitOSDFrame()`; the frontend does not generate the OSD menu contents.
- The project currently has no Dear ImGui sources or build dependency.

## Integration constraints to prove before coding

1. **Graphics context ownership:** identify how ZillaLib creates and retains the SDL window and GL context, and confirm which GL profile is used by each supported build.
2. **Event ownership:** ZillaLib owns the SDL event loop. Do not add a second event-polling loop. Determine whether its SDL events can be forwarded safely to ImGui, or whether a thin platform adapter should feed ImGui from existing ZillaLib input callbacks.
3. **Render-state isolation:** ImGui rendering must preserve/restore the GL state used by ZillaLib. It must not disturb the emulator texture, OSD texture, shaders, viewport, framebuffer, or swap lifecycle.
4. **Input arbitration:** when the new SOFIA-Pure UI is active, keyboard/mouse/gamepad events consumed by UI controls must not leak into the emulated machine. When the UI is hidden, existing input behavior must remain unchanged.
5. **Build isolation:** add ImGui as a separate dependency/target group; do not modify the DOSBox Pure source list or its compile definitions.

## Preferred experiment

Create a minimal, compile-time optional ImGui overlay that only displays a small diagnostic panel. Do not create the desktop shell or game explorer in this spike.

- Initialize and shut down the ImGui context with the application lifecycle.
- Start and render the ImGui frame at a point that is known to have the correct GL context current and after the existing scene composition.
- First test mouse and keyboard capture without forwarding captured events to DOSBox Pure.
- Validate window resize, fullscreen, controller input, mouse capture, OSD visibility, game video, audio, and frame pacing.

## Backend strategy

Do not assume that the stock SDL2 + OpenGL3 backends can be dropped in unchanged. They normally expect access to an SDL_Window, an SDL_GLContext, and the SDL event stream. Those handles and event-pump ownership have not yet been proven available through the current ZillaLib integration.

First inspect ZillaLib's public API and platform implementation. Then choose, in order:

1. Standard Dear ImGui SDL2/OpenGL3 backends if the required window/context/event hooks are safely accessible.
2. A narrow SOFIA-Pure platform adapter using existing ZillaLib input callbacks, paired with a renderer compatible with the actual GL context.
3. A different UI approach only if the first two cannot be integrated without invasive changes.

## Non-negotiable boundaries

- No changes to CPU, memory, devices, timing, audio mixing, libretro callbacks, game loading, save states, or filesystem behavior.
- Do not change `DBPS_SubmitOSDFrame()` or the existing game/OSD rendering path for this experiment.
- No replacement of ZillaLib in the initial spike.
- No changes to the default branch until the experiment is built and validated.

## Next implementation gate

Before adding ImGui source files, document the exact ZillaLib APIs or SDL handles available for:
- current window and GL context;
- event forwarding or input callbacks;
- framebuffer/GL state boundaries;
- frame timing and resize.

Only proceed to the diagnostic overlay once those are verified.


## Source audit: stock Dear ImGui backends

Audited the upstream `backends/imgui_impl_opengl3.cpp` and `backends/imgui_impl_sdl2.cpp` sources on 2026-11-16. This is a source review, not a build or runtime test; the project has not selected or pinned an ImGui revision yet.

### OpenGL renderer findings

The current OpenGL3 renderer explicitly backs up and restores the state it changes, including:
- active texture unit, program, texture binding on texture unit 0, and sampler binding where supported;
- array/element buffer and VAO state (or the relevant vertex attribute state on paths without VAOs);
- viewport and scissor rectangle;
- blend factors/equations and enable flags for blend, cull, depth, stencil, and scissor;
- polygon mode and primitive-restart enable state where supported.

It configures blend, cull, depth, stencil, scissor, viewport, shader, buffers/vertex attributes and texture bindings for its draw. It does not bind a different framebuffer, and the inspected render path does not modify depth function or depth write mask. Those facts are important because `ZL_GL_ResetFrameBuffer()` sets the framebuffer, viewport, blend, depth/cull baseline, and depth mask before the app draws its frame.

This makes the upstream OpenGL3 renderer a promising candidate: it has a deliberate state backup/restore path rather than relying on `ZL_GL_ResetFrameBuffer()` afterward. However, the state contract must be rechecked against the exact pinned ImGui revision and the exact ZillaLib GL profile. Do not assume it preserves arbitrary GL state it does not modify.

### SDL platform backend findings

`ImGui_ImplSDL2_ProcessEvent()` consumes an SDL event supplied by the caller; the backend does not require a second SDL event-polling loop. Its OpenGL initialization still requires an `SDL_Window*` and `SDL_GLContext`. ZillaLib's inspected public API does not expose those handles, and ZillaLib owns SDL event dispatch.

Therefore the preferred first experiment is:
- use the Dear ImGui OpenGL renderer backend only, if its GL requirements match the actual context;
- implement a narrow SOFIA-Pure platform/input adapter fed by ZillaLib's public keyboard, text, mouse, wheel, focus, resize and timing signals;
- do not access SDL internals, create another event loop, or modify ZillaLib merely to obtain SDL handles.

### Remaining compatibility checks

1. Verify the exact desktop GL version/profile and available entry points for the user's actual Visual Studio configuration. The `ZL_VIDEO_OPENGL2` and `ZL_VIDEO_OPENGL_CORE` build paths must not be conflated.
2. Pin a specific Dear ImGui revision and inspect its OpenGL renderer code at that revision.
3. Verify how ZillaLib reports mouse coordinates, logical/display dimensions, focus and text input so the adapter can supply correct ImGui IO values.
4. Verify event ordering and capture arbitration so UI-consumed keyboard/mouse input does not reach the emulated machine.
5. Only then add a compile-time optional diagnostic panel and build it on the user's target configuration.

No application, build, ZillaLib, or emulation-core code has been modified. This update is documentation only.


## Windows Visual Studio configuration and input API audit

Inspected the actual `DOSBoxPure-vs.vcxproj`, its imported `ZillaApp-vs.props`, and ZillaLib public headers.

### GL profile selection

- The SOFIA-Pure Visual Studio project imports `$(ZillaLibDir)/ZillaApp-vs.props`.
- The standard Visual Studio `Debug` and `Release` configurations do not add `ZL_VIDEO_OPENGL_CORE`; on desktop they therefore use ZillaLib's default `ZL_VIDEO_OPENGL2` path.
- The optional `DebugGLCORE` / `ReleaseGLCORE` configurations add `ZL_VIDEO_OPENGL_CORE`.
- The imported props file has a case variation in the spelling of the Debug GLCORE condition (`DebugGLCORE` vs `DebugGLCore`); MSBuild condition string comparisons are case-insensitive, but this should be cleaned up only if a future build-system change is actually needed. No change is proposed now.

The repository alone cannot tell us which configuration the user currently builds or runs. The first prototype must target the actual selected configuration, not assume the Core profile. For the lowest-risk first pass, use the existing standard Windows Debug configuration unless the user's normal workflow is known to use another one.

### Public input and display interface

ZillaLib publicly exposes:
- `ZL_Display::sigKeyDown` / `sigKeyUp`;
- `sigTextInput`;
- `sigPointerMove`, `sigPointerDown`, `sigPointerUp`;
- `sigMouseWheel`;
- `sigActivated` and `sigResized`;
- current pointer coordinates, key/button state, display width/height and focus queries.

This is sufficient in principle to build a platform adapter without polling SDL independently. Exact event field semantics, coordinate scaling, key mapping and input-capture ordering still need inspection before implementation.

### Render placement and input routing constraints

The existing `OnDraw()` calls `retro_run()`, applies save/load and geometry/interface changes, calls `ZL_GL_ResetFrameBuffer()`, then composes the game image and OSD. The ImGui draw call should be evaluated after all existing game/OSD/notification/diagnostic drawing and before the frame returns to ZillaLib for presentation.

Input must be arbitrated before it reaches existing DOSBox hotkey and emulated-input handlers: when the SOFIA UI owns keyboard or pointer interaction, consumed events must not leak into the emulated machine. The current code also uses pointer lock and direct SDL cursor calls in the host, so overlay mode must deliberately suspend or coordinate pointer lock rather than fighting it.

No source, project, build, or engine code was changed. This remains a documentation-only audit. No compilation or runtime test has been performed.


## Follow-up audit: actual context and input boundaries

Inspected the current ZillaLib SDL implementation, public event structures, and the SOFIA-Pure frontend callbacks.

### Actual GL context request

- With `ZL_VIDEO_OPENGL_CORE`, ZillaLib requests an OpenGL **3.1 Core** context through SDL.
- With the desktop `ZL_VIDEO_OPENGL2` path, ZillaLib does **not** set an explicit GL version or profile in the inspected SDL creation path. The resulting compatibility context is therefore platform/driver dependent and must be queried at runtime; it is not safe to assume a specific GLSL version from the macro name alone.
- ZillaLib creates the SDL GL context internally, but the inspected implementation does not retain the return value from `SDL_GL_CreateContext()` in a public handle. The SDL window pointer is also private to the platform source.
- Consequently, the standard ImGui SDL2 platform backend cannot be initialized from SOFIA-Pure without reaching into ZillaLib internals. That remains outside the preferred integration boundary.

### Public event data and the real input path

ZillaLib's public event structures provide the fields needed for a small adapter:
- keyboard: `is_down`, `is_repeat`, key and modifier mask;
- pointer motion: absolute and relative coordinates plus button-state bits;
- pointer button: button, down/up state and coordinates;
- wheel: horizontal and vertical deltas;
- window resize: previous dimensions plus fullscreen/maximized flags;
- activation: keyboard focus, mouse focus and minimized/maximized state.

Important limitation: these signals do not expose a general-purpose “consumed” return value. In SOFIA-Pure, `OnKeyDown()` and `OnKeyUp()` currently pass keyboard events into the libretro keyboard callback after hotkey handling. Therefore UI capture must be implemented explicitly in the SOFIA-Pure frontend callbacks; merely subscribing another listener to the same ZillaLib signal will not prevent the event reaching DOSBox.

Mouse input has a separate, critical path: `retro_input_state_cb()` polls `ZL_Input::MouseDelta()`, `Held()`, `MouseWheel()`, and pointer position directly. UI capture must gate those libretro mouse/pointer reads while the UI owns the pointer. Otherwise clicks and movement can leak into the emulated game even if pointer events were also delivered to ImGui.

### Pointer-lock coordination

The existing frontend applies pointer lock and cursor visibility from `OnDraw()`, based on the DOSBox OSD state, pause state and its pointer-lock option. The SOFIA-Pure UI needs an explicit ownership state:
- when the UI is interactive, release the game's pointer lock and expose the cursor;
- while the UI is closed, preserve the existing pointer-lock and cursor behavior;
- do not change the core's OSD behavior or mouse emulation policy outside this frontend arbitration.

### Updated implementation gate

The next safe implementation is still a compile-time optional frontend-only adapter and diagnostic panel. Before source changes, the build target must be identified: Windows Visual Studio standard configurations request the GL2 path, Windows GLCORE configurations request 3.1 Core, and the Makefile can select a different default according to target platform. The actual Git-based build job/configuration has not yet been identified.

No application source, build configuration, ZillaLib source, or DOSBox Pure core code has been modified. This remains a source audit only; no build or runtime test has been performed.


## GitHub Actions build target verified

The repository workflow `.github/workflows/build.yml` was inspected on both `main` and `feature/sofia-ui-redesign`; the file is identical (blob `fa561c53b21201adbdf453df93f08462f598b068`).

### Triggers and source checkout

- Automatic runs occur on pushes to `main` and pull requests targeting `main`.
- The workflow also declares `workflow_dispatch` with an optional version string.
- The checked-out SOFIA-Pure source is placed in the runner's `main/` directory. Thus a PR build checks out the PR source, not an unrelated local Visual Studio configuration.
- A push directly to `feature/sofia-ui-redesign` does not match the automatic push trigger. To build this branch, it needs a PR targeting `main` or a manually dispatched run selecting the branch.

### Windows build profile — decisive result

Both Windows jobs use MSBuild with `/p:Configuration=ReleaseGLCORE`:
- Win64: `/p:Platform=x64`
- Win32: `/p:Platform=Win32`
- Windows ARM64: `/p:Platform=ARM64`, also applying ARM64 project substitutions.

Therefore the principal Windows CI target is **ReleaseGLCORE**, not standard Release/GL2. This resolves the earlier uncertainty for the Windows artifacts produced by this workflow.

### Other CI targets

- Linux x64: `make linux-release -j4 ZL_VIDEO_OPENGL_CORE=1` (GL Core).
- Linux ARM64: regular CI build uses `ZL_VIDEO_OPENGL_ES2=1`; release/versioned build additionally produces GL Core and GLES2 artifacts.
- macOS x64 and ARM64: `make macos-release` without an explicit GL override in the workflow.

### Dependency reproducibility note

Each job clones `dosbox-pure` and `ZillaLib` from the owner's `main` branch at run time with `--depth 1`. Those dependency revisions are not pinned to immutable SHAs by this workflow. The workflow references the public `dosbox-pure` repository; the separately available private `dosbox-unleashed` repository is not named in these clone commands. This distinction should be preserved until the intended source relationship is verified.

### What this changes for the UI spike

Use **Windows x64 ReleaseGLCORE** as the first CI compatibility target for the ImGui renderer adapter, then validate Win32 and ARM64. Linux x64 GL Core is a useful second target. Keep the adapter frontend-only and optional; do not change the DOSBox core or dependency checkout policy as part of the first UI prototype.

No workflow or application code was changed. This was a read-only audit; no workflow run was started and no build has been executed by this audit.


## Pinned renderer candidate: Dear ImGui v1.91.9b

Inspected the exact upstream tag `v1.91.9b` rather than relying on the moving default branch.

- Tag: `v1.91.9b`
- Renderer source blob: `7d0b53621960d4f86f54077f7fdc8dda88bbece7` (the tag's Git commit SHA was not independently resolved in this audit)
- Renderer source: `backends/imgui_impl_opengl3.cpp`
- The backend contains its own small OpenGL loader in `imgui_impl_opengl3_loader.h`; it does not require ZillaLib's private SDL window/context handles and does not require the frontend to expose ZillaLib's function-pointer globals.
- The loader is deliberately isolated to the renderer translation unit. Keep ImGui's renderer backend in its own .cpp compilation unit; do not amalgamate it with ZillaLib GL headers or sources.
- The backend supports desktop OpenGL 3.1. Its own GLSL compatibility table maps GL 3.1 to GLSL 1.40, so initialize it explicitly with `ImGui_ImplOpenGL3_Init("#version 140")` for the ReleaseGLCORE target.
- OpenGL 3.1 support includes the primitive-restart state path. The backend only enables its base-vertex draw path on GL 3.2+, so the 3.1 target does not assume that later core feature.
- Its render path backs up and restores the GL state it changes. This remains preferable to trying to use `ZL_GL_ResetFrameBuffer()` as a restore operation; that ZillaLib function establishes a baseline and does not restore arbitrary prior state.

### Decision for the first CI prototype

Use Dear ImGui v1.91.9b, the OpenGL3 renderer backend only, and GLSL `#version 140` for the first Windows x64 `ReleaseGLCORE` diagnostic-overlay experiment. Feed ImGui through a SOFIA-Pure adapter using ZillaLib's public signals and frame timing. Do not use the stock SDL2 platform backend, do not create another GL context or SDL event loop, and do not modify ZillaLib or the DOSBox Pure core.

This is a source-level compatibility decision only. The tag has not been vendored, linked, compiled, or run in SOFIA-Pure. Input capture, mouse coordinate scaling, frame ordering, and actual CI validation remain open gates.

No application or build source has been modified; this update records the chosen integration candidate and its rationale.


## Follow-up audit: frontend input routing contract

Inspected the current `main.cpp` input callbacks and pointer-lock logic at the branch head.

### Keyboard path

- `OnKeyDown()` currently calls `OnKeyUseHotKey()` before translating and forwarding the key to the libretro keyboard callback.
- `OnKeyUp()` also calls `OnKeyUseHotKey()` first, then clears `RETROKDown[]` and sends the release event.
- Therefore the UI ownership check must sit **before hotkey handling**, not merely before the final libretro callback. Otherwise UI shortcuts can still trigger DOSBox frontend hotkeys.
- Do not implement capture as a naive early return on both key-down and key-up. A key pressed by the emulated machine before the UI opens still needs its release delivered; otherwise the guest can retain a stuck key. The adapter needs per-key routing/ownership bookkeeping and a focus-loss cleanup policy.
- ZillaLib's text-input signal should feed ImGui text input separately from physical key mapping; avoid synthesizing duplicate character input from key-down events.

### Mouse and pointer path

- `retro_input_state_cb()` polls relative mouse motion, buttons and wheel directly from `ZL_Input`.
- The same callback separately maps absolute pointer X/Y into the emulated core rectangle and reports the left button as pointer-pressed.
- When the UI owns the pointer, the frontend must return neutral mouse/pointer state for the corresponding libretro device queries; suppressing only pointer callbacks would not stop the polling path.
- `OnDraw()` also checks the middle mouse button to toggle the DOSBox OSD. That shortcut must be suppressed while the SOFIA UI owns pointer input.
- Existing pointer-lock and cursor-visibility management runs in `OnDraw()`. UI ownership must release pointer lock and keep the cursor visible, then restore the existing policy when the UI closes. Avoid competing cursor changes from two independent owners.

### Isolation rules for the first prototype

1. UI capture affects keyboard and pointer devices only; do not swallow joystick/gamepad input.
2. Preserve correct key-up delivery for keys already held when UI ownership changes.
3. Clear any UI/game routing state on window focus loss and shutdown so no stuck keys/buttons survive.
4. Keep DOSBox OSD and its existing input behavior unchanged when the new UI is inactive.
5. Do not change the core callbacks or DOSBox Pure source; implement arbitration in the SOFIA-Pure host only.

### Still not proven

Exact pointer coordinate units/scaling, text-input event payload details, signal ordering, and the correct focus-loss callback wiring still require a targeted read of the ZillaLib event definitions and dispatch implementation. No implementation should assume these details. No code or build files have been changed, and no build/runtime test has been performed.


## Follow-up audit: ZillaLib event semantics and coordinate conversion

Inspected the public event structures, the SDL-to-ZillaLib translation, and `ZL_Display_Process_Event()` in the current ZillaLib `main` branch.

### Pointer coordinates

- SDL desktop pointer coordinates enter ZillaLib in top-left-origin window coordinates and are DPI-scaled.
- If input scaling is enabled, ZillaLib applies viewport offset and input scaling before publishing pointer events.
- Immediately before public pointer signals, ZillaLib flips Y to a bottom-left origin using `Height - 1 - y`; relative Y is also inverted.
- The public absolute coordinates therefore use ZillaLib's logical display coordinate space, not raw SDL pixels. The adapter must convert to ImGui's top-left-origin coordinates (including the Y inversion) and supply the correct display/framebuffer scale.
- Pointer motion provides both absolute `x/y` and relative `xrel/yrel`; button events provide absolute coordinates and down/up state.
- Mouse-wheel values are multiplied by 120 in the SDL translation. Normalize them to the unit convention expected by ImGui rather than passing the raw ZillaLib values unchanged.

### Keyboard and text input

- ZillaLib exposes key-down/up with scancode-like `ZL_Key`, repeat state, and modifier bits.
- Text input arrives separately as UTF-8 text through `sigTextInput`. The SDL platform layer also synthesizes text events for Tab, Enter, keypad Enter and Backspace; the adapter must account for that behavior and avoid generating duplicate characters from physical key events.
- ZillaLib processes Alt+Enter and Alt+F4 before publishing key-down signals unless the corresponding prevent flags are set. SOFIA-Pure initializes the display with both `ZL_DISPLAY_PREVENTALTENTER` and `ZL_DISPLAY_PREVENTALTF4`, so these two shortcuts are not intercepted ahead of the frontend's event handlers in the current application configuration.

### Focus and resize

- `sigActivated` carries keyboard focus, mouse focus, minimized and maximized flags. Use loss of keyboard focus to release any keys routed to the emulated machine and reset ImGui's transient input state.
- `sigResized` is emitted after ZillaLib updates its display dimensions and GL viewport. The adapter should refresh ImGui display size and framebuffer scale from the post-resize values.
- The signals are dispatched synchronously from ZillaLib's event processing. They are suitable inputs to an adapter, but they do not provide a generic event-consumed return value; frontend-side routing remains necessary.

### Consequence for the adapter

The adapter can use ZillaLib's public signals without SDL handles or a second event loop. It must explicitly handle coordinate-origin conversion, DPI/input scaling, wheel normalization, UTF-8 text, focus loss, and per-key routing. This audit is source-based; no runtime coordinate test has been performed. No application, ZillaLib, or build code has been modified.


## Adapter integration design: minimal diagnostic overlay

This section defines the first implementation boundary. It is a design contract, not an implementation.

### Ownership and module boundary

Add a small frontend-only adapter module (proposed files: `SofiaUI.h/.cpp`) that owns:
- ImGui context lifetime and IO configuration;
- the pinned OpenGL3 renderer backend lifetime;
- translation of ZillaLib public input events into ImGui IO;
- the UI visibility/interaction mode and input-routing bookkeeping;
- one minimal diagnostic window for the first spike.

It must not own or create the SDL window, GL context, event loop, game surface, or DOSBox core. Do not call SDL_PollEvent, SDL_GL_SwapWindow, or ZL_GL_ResetFrameBuffer from the adapter. Keep ImGui's OpenGL3 backend implementation in its own translation unit so its embedded GL loader remains isolated.

### Lifecycle and frame order

1. Initialize the adapter only after `ZL_Display::Init()` has created the GL context and ZillaLib's GL setup is complete. Initialization failure leaves the existing frontend fully usable.
2. Connect the adapter to public ZillaLib signals for key down/up, UTF-8 text, pointer move/down/up, wheel, activation/focus, and resize. Keep the existing frontend callbacks connected; do not rely on signal consumption.
3. Each application frame, feed display size, framebuffer scale and delta time to ImGui, then call the OpenGL3 renderer's NewFrame and `ImGui::NewFrame()`.
4. Preserve the current game/OSD/notification drawing order. Submit ImGui draw data as the final overlay after existing frontend drawing (including the intro/logo overlay), so the diagnostic panel is above the game and existing HUD.
5. Render ImGui before ZillaLib performs its normal frame presentation/swap. Do not introduce another swap or frame loop.
6. Shut down the ImGui renderer and context before the GL context is destroyed. The exact ZillaLib quit/destruction ordering must be verified before implementation; if `OnQuit()` is not guaranteed to run while GL is valid, use a confirmed earlier teardown hook.

### Input routing and capture policy

- Feed every relevant public event to ImGui regardless of whether it is also routed to the emulator. ImGui's `WantCaptureKeyboard` and `WantCaptureMouse` are the policy inputs for routing, not a reason to stop populating IO.
- For the first diagnostic spike, use the last completed ImGui frame's capture flags when dispatching the next batch of ZillaLib events. Document the one-frame capture-state boundary; do not attempt to query a half-built frame.
- Keyboard arbitration belongs at the top of `OnKeyDown()` and `OnKeyUp()`, before `OnKeyUseHotKey()`. Track, per physical ZillaLib key, whether its key-down was delivered to the guest or owned by the UI. On key-up, release only keys previously delivered to the guest; never let a UI-owned key-up trigger a DOSBox hotkey. Preserve guest key-up for keys that were already down when UI capture begins.
- The libretro keyboard polling path must reflect the same routed state. A UI-captured key must not remain visible through `RETRO_DEVICE_KEYBOARD`.
- Pointer arbitration must gate all relevant paths, not just event signals: relative mouse axes, mouse buttons, wheel, absolute pointer axes, pointer-pressed state, and the middle-button OSD shortcut. When UI owns the pointer, return neutral values to the core for these devices.
- Keep joystick/gamepad routing untouched in this spike.
- When UI opens, release pointer lock and show the cursor. When UI closes, restore the pre-UI pointer-lock/cursor policy through one owner-controlled transition, not competing toggles.
- On keyboard-focus loss, synthesize releases for guest-routed keys, clear per-key ownership and mouse-button state, and reset ImGui's transient input state. On shutdown, perform equivalent cleanup.
- Respect existing ZillaLib Alt+Enter/Alt+F4 prevention flags; do not add a second shortcut handler for these keys.

### Minimal first visual test

The first visible build should be deliberately small:
- a toggleable, non-modal diagnostic panel;
- a title and a few read-only values (UI active state, display dimensions, capture flags, frame time);
- no file browser, game library, settings persistence, custom fonts, mascot, animations, or complex styling yet.

The panel is considered successful only if it can be opened/closed repeatedly, mouse/keyboard capture does not leak to DOSBox hotkeys or guest input, joystick input remains unchanged, focus loss does not leave stuck keys/buttons, resizing keeps pointer hit-testing aligned, and disabling the adapter restores the current frontend behavior.

### Remaining implementation gates

Before coding, verify:
- the exact ZillaLib frame/event dispatch order and the timing of `AfterFrame()` relative to `sigKeepAlive` and SDL buffer swap;
- the actual GL context profile/version on the Windows x64 `ReleaseGLCORE` CI path;
- the actual framebuffer scale on high-DPI and input-scaled windows;
- the safe GL-context teardown point;
- the exact Dear ImGui v1.91.9b backend compile definitions and project/Makefile source inclusion strategy.

No implementation, vendoring, project-file, workflow, ZillaLib, or DOSBox core change is included in this design update. No build or runtime test has been performed.


## Lifecycle gate resolved: exact desktop frame ordering

Inspected the current ZillaLib SDL desktop loop and `ZL_Application::Frame()`.

The verified order is:

1. Desktop loop calls `ZL_MainApplication->Frame()`.
2. `Frame()` updates timing, then calls `sigKeepAlive`.
3. ZillaLib's SDL platform connects `ProcessSDLEvents()` to `sigKeepAlive`, so pending SDL events are translated and dispatched before application drawing.
4. `Frame()` calls `BeforeFrame()`, scene calculation/drawing if present, then `AfterFrame()`.
5. SOFIA-Pure overrides `AfterFrame()` and calls `OnDraw()`.
6. `OnDraw()` completes the existing game, OSD, notification, diagnostic and intro drawing.
7. Control returns to the SDL desktop loop, which calls `SDL_GL_SwapWindow()`.

### Consequences

- Public ZillaLib input signals are dispatched before `AfterFrame()`; the adapter can queue translated input during event dispatch, then consume it when starting its ImGui frame from the frontend's drawing path.
- The natural render insertion point is at the very end of SOFIA-Pure's `OnDraw()`, after `DrawIntro()`, immediately before `AfterFrame()` returns. The existing SDL loop then performs the only buffer swap.
- Do not render ImGui from a separate keep-alive callback: that would place it before the frontend's normal drawing and allow the game frame to overwrite it.
- The desktop SDL loop calls `OnQuit()` after leaving the frame/swap loop. The current SOFIA-Pure override performs settings synchronization and `retro_unload_game()`. The inspected loop invokes `OnQuit()` before returning from the platform main function; the exact GL-context destruction/SDL shutdown path still needs confirmation before selecting the final ImGui backend shutdown point.
- `BeforeFrame()` is currently not overridden by SOFIA-Pure. A future implementation could use it to begin the ImGui frame after input dispatch and before `AfterFrame()`, but must verify that the retro core's `retro_run()` and all ZillaLib GL state transitions do not invalidate assumptions made by the renderer backend. The simpler first spike may begin and build the ImGui frame at the tail of `OnDraw()`, then render immediately there; this avoids an unnecessary split frame lifecycle.

This resolves the event-pump/draw/swap ordering from source. It does not prove GL state compatibility or teardown safety at runtime.


## OpenGL 3.1 Core and renderer-backend audit (Dear ImGui v1.91.9b)

The Windows x64 CI target is `ReleaseGLCORE`. Its ZillaLib SDL window setup explicitly requests:
- `SDL_GL_CONTEXT_PROFILE_CORE`
- OpenGL major 3, minor 1
- double buffering

This is a concrete desktop target, not a runtime observation from a built executable. SDL's request is confirmed in source; the actual driver-created context still needs to be logged during the first run.

### Dear ImGui backend compatibility

Inspected the upstream Dear ImGui tag `v1.91.9b`, specifically `backends/imgui_impl_opengl3.cpp` and its bundled `imgui_impl_opengl3_loader.h`.

- The backend includes its own stripped GL3W loader unless `IMGUI_IMPL_OPENGL_LOADER_CUSTOM` is defined. It does not require ZillaLib's private `InitExtensionEntries()` or SDL window/context handles.
- The desktop path uses VAOs and supports desktop GL 3.1. The requested context is therefore within the backend's stated desktop GL 3.x target.
- The backend's default desktop GLSL string is `#version 130`; an explicit `#version 140` is also valid for OpenGL 3.1. For the spike, use explicit `#version 140` to match the previously selected target, then confirm shader compilation on the CI/runtime driver.
- The renderer backend does not bind a framebuffer. It renders into whichever framebuffer is already bound, so it must be called while ZillaLib's intended window framebuffer is active.
- Its render function backs up/restores the state it changes: active texture (and unit-0 texture binding), current program, sampler where supported, array buffer, VAO, blend equations/functions and blend/cull/depth/stencil/scissor enables, primitive restart, polygon mode, viewport and scissor box.
- In the inspected version it does not change framebuffer binding, depth function, or depth write mask. Those states are not part of its backup; the first runtime spike must still verify the real host/core state and draw result.
- This backend is not a universal GL state transaction. Keep the UI render at the end of the existing frame and do not use `ZL_GL_ResetFrameBuffer()` as a substitute for state preservation.

### Teardown point resolved for the current SDL desktop implementation

The inspected SDL desktop loop calls `OnQuit()` after it exits the Frame/swap loop. The loop then returns; this source path contains no explicit `SDL_GL_DeleteContext`, `SDL_DestroyWindow`, `SDL_VideoQuit`, or `SDL_Quit` call. The GL context created by `SDL_GL_CreateContext()` therefore remains available during the application's `OnQuit()` callback in this implementation.

Recommended shutdown ordering for the future adapter:
1. Call `SofiaUI::Shutdown()` at the start of SOFIA-Pure's `OnQuit()`, while the desktop GL context is still alive.
2. Then continue the existing settings synchronization and `retro_unload_game()` path.
3. Keep shutdown idempotent so partial initialization and initialization failure are safe.

This is source-level lifecycle evidence for the current SDL desktop path, not a runtime validation and not a guarantee for other ZillaLib platform backends. If explicit SDL context destruction is added later, the shutdown ordering must be revisited.

### Remaining gates

- Log the actual GL version/profile and renderer string on the first Windows x64 `ReleaseGLCORE` run.
- Confirm the ImGui shader compiles with explicit GLSL `#version 140`.
- Verify framebuffer binding and visible compositing at runtime after the DOSBox core has rendered.
- Verify framebuffer scale and pointer coordinate mapping on high-DPI/scaled windows.
- Confirm input arbitration and focus-loss recovery with the real guest.

No application source, build files, vendored ImGui sources, ZillaLib code, or DOSBox core code has been changed. No build or runtime test has been performed.


## Build-system integration audit: Windows x64 and Linux

Inspected the current SOFIA-Pure Visual Studio project and Makefile, plus ZillaLib's Linux app makefile.

### Confirmed source discovery behavior

- Visual Studio uses explicit `<ClCompile Include=...>` entries. A new `SofiaUI.cpp` and the Dear ImGui translation units will not be picked up automatically.
- The SOFIA-Pure Makefile includes ZillaLib's app Makefile and defines `ZL_ADD_SRC_FILES` for DOSBox Pure sources.
- ZillaLib's Linux app makefile builds root-level `*.cpp` files and then appends files expanded from `ZL_ADD_SRC_FILES`. A root-level `SofiaUI.cpp` would therefore be picked up automatically on Linux; ImGui sources under a third-party subdirectory need explicit entries in `ZL_ADD_SRC_FILES`.
- The Windows project currently sets include paths for DOSBox Pure and its own headers; no ImGui include path or ImGui source entries exist.

### Minimal future source layout

If the first code spike is approved, keep the third-party code isolated:

```
SOFIA-Pure/
  SofiaUI.h
  SofiaUI.cpp
  third_party/
    imgui/                 # pinned Dear ImGui v1.91.9b source
      imgui.cpp
      imgui_draw.cpp
      imgui_tables.cpp
      imgui_widgets.cpp
      imgui.h
      imconfig.h
      imgui_internal.h
      imstb_*.h
      backends/
        imgui_impl_opengl3.cpp
        imgui_impl_opengl3.h
        imgui_impl_opengl3_loader.h
```

Only the four core ImGui translation units and `backends/imgui_impl_opengl3.cpp` are required for this custom ZillaLib platform adapter. Do not compile `imgui_impl_sdl2.cpp` or any other platform backend.

### Required build-file edits when implementation begins

- Visual Studio: add `SofiaUI.cpp`, the four ImGui core `.cpp` files and `imgui_impl_opengl3.cpp` as `ClCompile` items; add `third_party/imgui` and, where needed, `third_party/imgui/backends` to include directories.
- Linux Makefile: add the four ImGui core source paths and OpenGL3 backend source path to `ZL_ADD_SRC_FILES`; add the same include directories to `APPFLAGS`. `SofiaUI.cpp` at repository root is already included by the app source wildcard.
- Keep the ImGui version pinned in-repository so CI does not depend on an unpinned upstream checkout at build time.

The Windows Visual Studio project and Linux source-discovery path are confirmed from source. The macOS-specific makefile path and any platform-specific OpenGL loader/link requirements remain to be checked before claiming cross-platform build coverage.

No build files or source code have been modified in this documentation-only step.
