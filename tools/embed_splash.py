#!/usr/bin/env python3
"""Convert the project splash PNG into a self-contained C++ byte array."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
source = root / "SOFIA-Splash.png"
target = root / "sofia_splash.h"

data = source.read_bytes()
if not data.startswith(b"\x89PNG\r\n\x1a\n"):
    raise SystemExit("SOFIA-Splash.png is not a valid PNG file")

with target.open("w", encoding="ascii", newline="\n") as out:
    out.write("// Generated from SOFIA-Splash.png by tools/embed_splash.py. Do not edit.\n")
    out.write("#ifndef SOFIA_SPLASH_H\n#define SOFIA_SPLASH_H\n")
    out.write("static const unsigned char sofia_splash_png[] = {\n")
    for offset in range(0, len(data), 16):
        chunk = data[offset:offset + 16]
        out.write("    " + ", ".join("0x%02X" % byte for byte in chunk) + ",\n")
    out.write("};\n#endif // SOFIA_SPLASH_H\n")

print(f"Embedded {len(data)} bytes from {source.name} into {target.name}")

skin_source = root / "neon_blue.png"
skin_target = root / "neon_blue.h"
skin_data = skin_source.read_bytes()
if not skin_data.startswith(b"\x89PNG\r\n\x1a\n"):
    raise SystemExit("neon_blue.png is not a valid PNG file")

with skin_target.open("w", encoding="ascii", newline="\n") as out:
    out.write("// Generated from neon_blue.png by tools/embed_splash.py. Do not edit.\n")
    out.write("#ifndef NEON_BLUE_H\n#define NEON_BLUE_H\n")
    out.write("static const unsigned char neon_blue_png[] = {\n")
    for offset in range(0, len(skin_data), 16):
        chunk = skin_data[offset:offset + 16]
        out.write("    " + ", ".join("0x%02X" % byte for byte in chunk) + ",\n")
    out.write("};\n#endif // NEON_BLUE_H\n")

print(f"Embedded {len(skin_data)} bytes from {skin_source.name} into {skin_target.name}")
