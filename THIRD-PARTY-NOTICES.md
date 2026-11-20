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
- The patch adapts EMU8000 emulation to DOSBox Pure Unleashed and explicitly identifies `86Box snd_emu8k.c` as a technical reference, crediting Sarah Walker.
- The 86Box README and its vcpkg manifest declare GPL-2.0-or-later. GitHub's repository badge/metadata may display the shorter GPL-2.0 identifier, so the explicit README and manifest statements are the more informative licensing references. The patch's own header also states GPL version 2 or (at the recipient's option) any later version.
- DOSBox-X is acknowledged as a related implementation/reference for the AWE32/EMU8000 integration. This notice does not claim that every line of the patch originated from DOSBox-X.
- References: [DOSBox-X](https://github.com/joncampbell123/dosbox-x), [86Box](https://github.com/86Box/86Box).

## Distribution notes

SOFIA-Pure is an independent, AI-assisted project. No upstream project or contributor is represented as endorsing or supporting SOFIA-Pure. Keep all source-file copyright and license notices intact. The combined distribution selects GPLv3: the DOSBox Pure / DOSBox Pure Unleashed, DOSBox-X and 86Box materials consulted declare GPL-2.0-or-later, which permits selecting GPLv3 for the combined work; the xBRZ-derived shader notice specifies GPL-3.0. Keep all component-specific notices intact. When distributing binaries, provide the complete corresponding source and build/install materials required by the applicable licenses, and include all applicable license texts and this notice file.
