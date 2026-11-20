#!/usr/bin/env python3
"""Replace DOSBox Pure's OSD mouse pointer with the fixed CP437 Alt+178 glyph."""
from pathlib import Path

target = Path("dosbox-pure/dosbox_pure_osd.h")
if not target.is_file():
    raise SystemExit(f"Expected upstream OSD source not found: {target}")

source = target.read_text(encoding="utf-8")
start_token = "\tvoid Draw(DBP_BufferDrawing& buf, bool joykbd)\n\t{"
end_token = "\n\t}\n};"
if source.count(start_token) != 1:
    raise SystemExit("DOS cursor patch aborted: expected exactly one DBP_MenuMouse::Draw")
start = source.index(start_token)
end = source.index(end_token, start) + len("\n\t}")
replacement = """\tvoid Draw(DBP_BufferDrawing& buf, bool joykbd, int lineHeight)
\t{
\t\tclick = right_up = wheel_up = wheel_down = false;
\t\tif (!realmouse && !joykbd) return;

\t\t// CP437 178 (Alt+178): render one white DOS shade-block character.
\t\t// Align it to the OSD's actual 8-pixel character cell and active line height.
\t\tconst int ch = (lineHeight == 8 ? 8 : 14);
\t\tconst Bit8u* font = (lineHeight == 8 ? int10_font_08 : int10_font_14);
\t\tint cellx = ((int)x / DBP_BufferDrawing::CW) * DBP_BufferDrawing::CW;
\t\tint celly = ((int)y / ch) * ch;
\t\tif (cellx > (int)buf.width - DBP_BufferDrawing::CW) cellx = (int)buf.width - DBP_BufferDrawing::CW;
\t\tif (celly > (int)buf.height - ch) celly = (int)buf.height - ch;
\t\tif (cellx < 0) cellx = 0;
\t\tif (celly < 0) celly = 0;
\t\tbuf.DrawChar(font, ch, cellx, celly, 178, 0xFFFFFFFF);
\t}"""
source = source[:start] + replacement + source[end:]
source = source.replace("mouse.Draw(buf, isOSK);", "mouse.Draw(buf, isOSK, lh);")
if source.count("mouse.Draw(buf, isOSK, lh);") != 1:
    raise SystemExit("DOS cursor patch aborted: OSD mouse draw call was not uniquely updated")
target.write_text(source, encoding="utf-8")
print("Applied fixed white CP437 Alt+178 OSD cursor")
