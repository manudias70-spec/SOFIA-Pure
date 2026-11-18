#!/usr/bin/env python3
"""Replace the two Explorer pane frames with one shared Commander double-line frame."""
from pathlib import Path

target = Path("dosbox-pure/dosbox_pure_osd.h")
if not target.is_file():
    raise SystemExit(f"Expected upstream OSD source not found: {target}")

source = target.read_text(encoding="utf-8")

def replace_once(label, old_text, new_text):
    global source
    count = source.count(old_text)
    if count != 1:
        raise SystemExit(f"Commander frame patch aborted: {label!r} expected one source match, found {count}")
    source = source.replace(old_text, new_text, 1)

replace_once(
    "DrawMenuBase frame-control parameter",
    "\tint DrawMenuBase(DBP_BufferDrawing& buf, Bit32u blend, const int lh, const int rows, const DBP_MenuMouse& m, bool mouseMoved, int menul, int menur, int menuu, bool centerv = false, bool nc_explorer = false)",
    "\tint DrawMenuBase(DBP_BufferDrawing& buf, Bit32u blend, const int lh, const int rows, const DBP_MenuMouse& m, bool mouseMoved, int menul, int menur, int menuu, bool centerv = false, bool nc_explorer = false, bool suppress_frame = false)"
)

replace_once(
    "suppress individual Explorer pane frame",
    """\t\tif (nc_explorer)
\t\t{
\t\t\tbuf.DrawBox(menul, menuu - 3, menur - menul, menuh + 6, 0xFF0000AA | blend, 0xFFFFFFFF);
\t\t\tbuf.DrawBox(menul + 3, menuu, menur - menul - 6, menuh, 0xFF0000AA | blend, 0xFFFFFFFF);
\t\t}
\t\telse buf.DrawBox(menul, menuu - 3, menur - menul, menuh + 6, buf.BGCOL_MENU | blend, buf.COL_LINEBOX);""",
    """\t\tif (!suppress_frame)
\t\t{
\t\t\tif (nc_explorer)
\t\t\t{
\t\t\t\tbuf.DrawBox(menul, menuu - 3, menur - menul, menuh + 6, 0xFF0000AA | blend, 0xFFFFFFFF);
\t\t\t\tbuf.DrawBox(menul + 3, menuu, menur - menul - 6, menuh, 0xFF0000AA | blend, 0xFFFFFFFF);
\t\t\t}
\t\t\telse buf.DrawBox(menul, menuu - 3, menur - menul, menuh + 6, buf.BGCOL_MENU | blend, buf.COL_LINEBOX);
\t\t}"""
)

replace_once(
    "suppress right-pane frame only in dual-pane Explorer",
    "int listu = DrawMenuBase(buf, blend, lh, rows, m, mouseMoved, panel_x + 8, w - 8, hdr, (list[0].type == IT_NONE), is_nc_explorer);",
    "int listu = DrawMenuBase(buf, blend, lh, rows, m, mouseMoved, panel_x + 8, w - 8, hdr, (list[0].type == IT_NONE), is_nc_explorer, is_filebrowse);"
)

replace_once(
    "remove left-pane individual frame",
    """\t\t\t\t// Same Norton Commander double-line frame and colors as the active right pane.
\t\t\t\tbuf.DrawBox(left_panel_x, hdr - 3, left_panel_w, rows*lh + 6, 0xFF0000AA | blend, 0xFFFFFFFF);
\t\t\t\tbuf.DrawBox(left_panel_x + 3, hdr, left_panel_w - 6, rows*lh, 0xFF0000AA | blend, 0xFFFFFFFF);
""",
    ""
)

replace_once(
    "draw one shared white double-line Commander frame",
    """\t\tbool autoboot_show = (DBP_Run::autoboot.use && listmode != IT_VARIANTLIST && !is_filebrowse && (list[sel].type < _IT_NO_AUTOBOOT || hide_sel) && first_shell);""",
    """\t\tif (DBP_FullscreenOSD && is_filebrowse)
\t\t{
\t\t\tconst int frame_x = content_x + 3, frame_y = hdr - 8;
\t\t\tconst int frame_w = content_w - 6, frame_h = rows * lh + 16;
\t\t\tconst Bit32u frame_color = 0xFFFFFFFF;
\t\t\t// Outer rectangle.
\t\t\tbuf.FillRect(frame_x, frame_y, frame_w, 1, frame_color);
\t\t\tbuf.FillRect(frame_x, frame_y + frame_h - 1, frame_w, 1, frame_color);
\t\t\tbuf.FillRect(frame_x, frame_y, 1, frame_h, frame_color);
\t\t\tbuf.FillRect(frame_x + frame_w - 1, frame_y, 1, frame_h, frame_color);
\t\t\t// Inner rectangle: the second white line.
\t\t\tbuf.FillRect(frame_x + 3, frame_y + 3, frame_w - 6, 1, frame_color);
\t\t\tbuf.FillRect(frame_x + 3, frame_y + frame_h - 4, frame_w - 6, 1, frame_color);
\t\t\tbuf.FillRect(frame_x + 3, frame_y + 3, 1, frame_h - 6, frame_color);
\t\t\tbuf.FillRect(frame_x + frame_w - 4, frame_y + 3, 1, frame_h - 6, frame_color);
\t\t}
\t\tbool autoboot_show = (DBP_Run::autoboot.use && listmode != IT_VARIANTLIST && !is_filebrowse && (list[sel].type < _IT_NO_AUTOBOOT || hide_sel) && first_shell);"""
)

target.write_text(source, encoding="utf-8")
print("Applied one shared white double-line frame around both Commander panels")
