# AWE32 integration — Build 9 experiment

## Frozen baseline

- Desktop frontend: `manudias70-spec/SOFIA-Pure`
- Experimental branch: `feature/awe32-build9`
- DOSBox Pure core repository used by the Build 9 workflow: `anydream/dosbox-pure`
- Pinned core commit: `9cccfa21cb117edf94fbcd1a26b2dee8b12db598`
- Existing frontend patch: `patches/dosbox-pure-xbrz-options.patch`

Do not move the core pin or replace the Build 9 frontend while implementing AWE32.

## Confirmed core architecture at the pinned commit

- Sound Blaster emulation is in `src/hardware/sblaster.cpp`.
- GUS emulation is in `src/hardware/gus.cpp`.
- Audio mixing is in `src/hardware/mixer.cpp`.
- ISA I/O registration is declared in `include/inout.h`.
- The Visual Studio core project explicitly lists each hardware source file; a new EMU8000 translation unit must be added there as well as to the Makefile/source lists.
- DOSBox Pure's mixer has a fixed six-slot libretro volume mapping in `mixer.cpp`; a separate AWE output channel needs a deliberate mapping or a shared SB volume strategy.
- The core serializes hardware state. EMU8000 state must be reviewed for save-state compatibility before enabling it by default.

## Porting source

DOSBox-X's `emu8k.cpp` / `emu8k.h` implementation identifies its EMU8000 voice, register, DRAM, envelope and interpolation logic as following 86Box's `snd_emu8k.c`. This is a substantial hardware module, not a drop-in feature flag. Porting must preserve the relevant upstream copyright and license notices and account for DOSBox Pure's older APIs.

## Planned implementation order

1. Add EMU8000 core and adapt its I/O and mixer interfaces.
2. Attach EMU8000 to the existing SB16 device as the AWE32 variant, retaining SB16 PCM behavior.
3. Load the user-supplied `awe32.raw` from the configured `system` directory; never commit or package the ROM.
4. Add safe behavior when the ROM is missing or malformed.
5. Add/reset/save-state handling and volume behavior.
6. Build Windows x64 first, then expand to the other existing Build 9 targets.
7. Test DOS AWE utilities and a known AWE32 MIDI/sample workload before merging.


## Verified EMU8000 reference details

The DOSBox-X implementation provides a useful integration reference and explicitly attributes its EMU8000 register/voice/DRAM/envelope/interpolation work to 86Box's `snd_emu8k.c` (Sarah Walker). Preserve those notices and the GPL-2.0 terms when adapting code.

- ROM contract in the reference implementation: exactly 1 MiB (`1,048,576` bytes), loaded as raw data. It recognizes the AWE-DUMP two-byte-offset variant by checking the GM marker and shifting the image back two bytes.
- The reference initializes the EMU8000 at ISA base `0x620`, with register windows at `0x620`, `0xA20`, and `0xE20` (the latter two are base + `0x400` and base + `0x800`), each with four byte/word-spaced ports.
- The existing frontend helper `DBP_FileOpenContentOrSystem()` already opens a named file from the content directory and then the Libretro system directory. This can support the user-managed `awe32.raw` without adding ROM data to the repository.
- The core's six Libretro volume slots do not currently include AWE. Decide explicitly whether AWE shares the SB volume slot or receives a new user-facing control; do not add an unchecked mixer channel name because the current mixer asserts on unknown names.
- Save states are a major integration requirement: the EMU8000 owns dynamically allocated ROM/RAM plus a large mutable state structure containing voice, chorus, reverb, and output buffers. Pointer fields and ROM data must not be serialized as raw addresses. On load, rebuild RAM pointer tables and restore mutable sample RAM and synth state. The memory cost of including sample RAM in save states must be measured.

## Integration shape from DOSBox-X

- Keep the existing SB16 DSP/PCM path active when the selected card type is AWE32.
- Register the three EMU8000 I/O windows separately from the SB16 DSP ports.
- Synchronize the wavetable mixer channel before EMU8000 register reads/writes, so register changes take effect at the correct audio boundary.
- Stop/uninstall the AWE mixer callback before freeing EMU8000 memory during shutdown; otherwise an audio callback could access freed state.
- If the ROM is absent or invalid, log a warning and leave the ordinary SB16 path available rather than failing core initialization.


## Build 9 serialization and mixer findings

- The SB device is a single `SB_INFO sb` instance in this pinned Pure core, not DOSBox-X's multi-card array. Its config parser currently accepts `sb1`, `sb2`, `sbpro1`, `sbpro2`, `sb16`, `gb`, and `none`. AWE32 should be a distinct SB type that retains the SB16 DSP command behavior.
- SB save-state data is handled by `DBPSerialize_SBLASTER()` in `src/hardware/sblaster.cpp`, registered in `src/dbp_serialize.cpp`. This is the natural place to serialize the EMU8000 state alongside the SB device.
- `DBPArchive::SerializeExcept` has overloads for up to three pointer exceptions; the EMU8000 structure has four pointer-bearing fields/groups (`ram`, `rom`, `empty`, and `ram_pointers`). Its serializer should use `DoExceptionList` directly or serialize explicit fields, never dump pointer values.
- The ROM is immutable and can be reloaded from the user's system directory on initialization/load. The writable EMU8000 sample RAM and mutable chip state must be preserved. After load, reconstruct the 256-entry RAM pointer table from the reallocated RAM, ROM, and empty buffers.
- The mixer volume assertion is in `MixerChannel::UpdateVolume()`; the current volume index switch routes known channels into six Libretro volume slots. AWE should share the SB volume slot initially, avoiding a new UI option and avoiding an unrecognized channel name. This is the least invasive Build 9 behavior.
- The Build 9 Windows project has explicit compile entries for hardware source files in `dosbox_pure_libretro.vcxproj` and `.filters`. The workflow itself applies the frontend patch to the pinned core before building, so all core changes must be delivered as a patch file in the frontend repository and applied in each build job.

## Next implementation gate

Before enabling AWE32 in the user-facing config, complete the EMU8000 core adaptation and its explicit serializer, then wire the first-SB-only AWE32 type. Do not add a config option that can select an incomplete device. The first acceptance build remains Windows x64 on the frozen core SHA.


## Current implementation checkpoint (experimental; not yet accepted)

- Added `patches/dosbox-pure-awe32-emu8k-core.patch` to the SOFIA-Pure experimental branch. It introduces the DOSBox-X EMU8000 implementation and header, retaining the upstream GPL/copyright attribution to 86Box/Sarah Walker.
- The new source is added to the pinned core's Visual Studio project; the Makefile already discovers `src/*/*.cpp` automatically.
- The Build 9 workflow now applies this patch after the existing xBRZ patch in all seven build jobs.
- The workflow's patch paths were corrected to `../main/patches/...`: `git -C dosbox-pure` resolves patch paths relative to the core checkout, not the workflow root. Earlier run attempts failed at dependency checkout because the old relative path was invalid.
- A fresh workflow run was queued for commit `30e3fa4cc56fff45ac2eca4b0a4a703c031c8ce2`. Its build jobs are running; no compile result has been confirmed yet.
- This is only the EMU8000 engine source scaffold. It is not yet connected to SB16, not selectable as an AWE32 device, and not yet serialized. Do not describe it as working AWE32 support until those steps and functional tests pass.

## Safety rule

This branch is experimental. Keep the known-good Build 9 branch untouched. Do not merge or publish a release until the Windows build and functional AWE32 tests pass.
