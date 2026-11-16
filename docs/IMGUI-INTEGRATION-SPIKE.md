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
