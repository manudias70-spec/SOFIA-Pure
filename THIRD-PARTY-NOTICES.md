# Third-party notices

This file records known upstream components and attribution information for SOFIA-Pure. It is a project-level guide; copyright and license notices in individual source files remain authoritative.

## DOSBox Pure / DOSBox Pure Unleashed

- Upstream projects: [DOSBox Pure](https://codeberg.org/schelling/dosbox-pure) and [DOSBox Pure Unleashed](https://github.com/schellingb/dosbox-pure-unleashed).
- Original author credited by the upstream project: Bernhard Schelling.
- The upstream README states GNU GPL version 2 or any later version.
- A copy of the GPLv2 license text inherited from the upstream repository is preserved at [LICENSES/GPL-2.0.txt](LICENSES/GPL-2.0.txt).

## xBR / xBRZ shader

- File: `xbrz_shader.h`.
- Hyllian: xBR vertex code and texel mapping; the MIT license notice is retained in the file.
- Zenju: xBRZ-derived code/concepts; the source notice identifies GNU GPL-3.0.
- This file contains a GPL-3.0-derived component as well as MIT-licensed xBR material. Do not remove either upstream notice. Its combination with other project components must be assessed before distributing the whole application.
- References: [Hyllian](https://github.com/Hyllian), [xBRZ](https://sourceforge.net/projects/xbrz/).

## Sound Blaster AWE32 / EMU8000

- Integration patch: `patches/dosbox-pure-awe32-emu8k-core.patch`.
- The EMU8000 core adapted in SOFIA-Pure is based on DOSBox-X `src/hardware/emu8k.cpp`. Its source header explicitly states that register I/O, 32 voices, DRAM, envelopes and cubic interpolation follow 86Box `snd_emu8k.c`, crediting Sarah Walker.
- DOSBox-X's AWE32 support commit and release notes credit **cyberfox1** for adding AWE32 support and subsequent improvements to the original 86Box-derived EMU8K implementation.
- The 86Box README declares GNU GPL version 2 or later. The DOSBox-X source file and the SOFIA-Pure integration patch also carry GPL version 2-or-later notices.
- References: [DOSBox-X EMU8K source](https://github.com/joncampbell123/dosbox-x/blob/master/src/hardware/emu8k.cpp), [DOSBox-X AWE32 support commit](https://github.com/joncampbell123/dosbox-x/commit/ac3f80e14c616f35b12a534793ad1224bffd5350), [cyberfox1](https://github.com/cyberfox1), [86Box source](https://github.com/86Box/86Box/blob/master/src/sound/snd_emu8k.c), [86Box](https://github.com/86Box/86Box).

## Distribution notes

SOFIA-Pure is an independent, AI-assisted project. No upstream project or contributor is represented as endorsing or supporting SOFIA-Pure. Keep all source-file copyright and license notices intact. The combined distribution selects GPLv3: the DOSBox Pure / DOSBox Pure Unleashed, DOSBox-X and 86Box materials consulted declare GPL-2.0-or-later, which permits selecting GPLv3 for the combined work; the xBRZ-derived shader notice specifies GPL-3.0. Keep all component-specific notices intact. When distributing binaries, provide the complete corresponding source and build/install materials required by the applicable licenses, and include all applicable license texts and this notice file.
