# Third-party notices

This file records known upstream components and attribution information for SOFIA-Pure. It is a project-level guide, not a substitute for the copyright and license notices in individual source files. Preserve those original notices.

## DOSBox Pure / DOSBox Pure Unleashed

- Upstream projects: [DOSBox Pure](https://codeberg.org/schelling/dosbox-pure) and [DOSBox Pure Unleashed](https://github.com/schellingb/dosbox-pure-unleashed).
- The original DOSBox Pure project credits **Bernhard Schelling** and its contributors.
- SOFIA-Pure is an independent derivative based on the DOSBox Pure Unleashed desktop project.
- The repository's `LICENSE` file is retained from the upstream base. Consult that file and the relevant source-file headers for the applicable license terms.

## xBR / xBRZ shader

- File: `xbrz_shader.h`.
- **Hyllian**: xBR vertex code and texel mapping; the MIT-related notice is retained in the source file.
- **Zenju**: xBRZ-derived code and concepts; the source notice identifies GNU GPL-3.0.
- Keep both upstream notices intact.
- References: [Hyllian](https://github.com/Hyllian), [xBRZ project](https://sourceforge.net/projects/xbrz/).

## Sound Blaster AWE32 / EMU8000

- Integration patch: `patches/dosbox-pure-awe32-emu8k-core.patch`.
- The EMU8000 core adapted in SOFIA-Pure is based on DOSBox-X `src/hardware/emu8k.cpp`.
- That source header states that register I/O, 32 voices, DRAM, envelopes and cubic interpolation follow 86Box `snd_emu8k.c`, crediting **Sarah Walker**.
- DOSBox-X's AWE32 support history credits **cyberfox1** for adding AWE32 support and subsequent improvements to the 86Box-derived EMU8K implementation.
- References:
  - [DOSBox-X EMU8K source](https://github.com/joncampbell123/dosbox-x/blob/master/src/hardware/emu8k.cpp)
  - [DOSBox-X AWE32 support commit](https://github.com/joncampbell123/dosbox-x/commit/ac3f80e14c616f35b12a534793ad1224bffd5350)
  - [cyberfox1](https://github.com/cyberfox1)
  - [86Box EMU8000 source](https://github.com/86Box/86Box/blob/master/src/sound/snd_emu8k.c)
  - [86Box project](https://github.com/86Box/86Box)

## Project independence and distribution

SOFIA-Pure is an independent, AI-assisted project. No upstream project or contributor is represented as endorsing, maintaining or supporting it.

The repository's `LICENSE` file and the notices in individual source files must be read together. Some incorporated components carry their own license notices. This document records known provenance; it does not make a blanket legal determination that every component can be redistributed under one license. Before distributing source or binaries, verify compatibility and comply with the applicable license conditions, including preservation of notices and provision of corresponding source where required.
