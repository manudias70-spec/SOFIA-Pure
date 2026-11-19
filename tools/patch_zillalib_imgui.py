from pathlib import Path

def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one patch anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="")

header = Path("ZillaLib/Include/ZL_Surface.h")
source = Path("ZillaLib/Source/ZL_Surface.cpp")

replace_once(
    header,
    "int GetHeight() const;\n\tZL_Vector GetSize() const;",
    "int GetHeight() const;\n\tZL_Vector GetSize() const;\n\tunsigned GetGLTexture() const;"
)
replace_once(
    header,
    "void SetPixels(const unsigned char* pixels, int sub_x, int sub_y, int sub_width, int sub_height, int BytesPerPixel = 4);",
    "void SetPixels(const unsigned char* pixels, int sub_x, int sub_y, int sub_width, int sub_height, int BytesPerPixel = 4);\n\tvoid SetPixelsBGRA(const unsigned char* pixels, int sub_x, int sub_y, int sub_width, int sub_height);"
)
replace_once(
    source,
    "int ZL_Surface::GetHeight() const { return impl ? impl->tex->hRep : 0; }\nZL_Vector ZL_Surface::GetSize() const { return impl ? ZL_Vector(s(impl->tex->wRep), s(impl->tex->hRep)) : ZL_Vector(); }",
    "int ZL_Surface::GetHeight() const { return impl ? impl->tex->hRep : 0; }\nZL_Vector ZL_Surface::GetSize() const { return impl ? ZL_Vector(s(impl->tex->wRep), s(impl->tex->hRep)) : ZL_Vector(); }\nunsigned ZL_Surface::GetGLTexture() const { return (impl && impl->tex ? (unsigned)impl->tex->gltexid : 0); }"
)
replace_once(
    source,
    """void ZL_Surface::SetPixels(const unsigned char* pixels, int sub_x, int sub_y, int sub_width, int sub_height, int BytesPerPixel)
{
\tstatic const GLenum fmts[] = { GL_RGBA, GL_LUMINANCE, GL_LUMINANCE_ALPHA, GL_RGB, GL_RGBA };
\tglBindTexture(GL_TEXTURE_2D, impl->tex->gltexid);
\tglTexSubImage2D(GL_TEXTURE_2D, 0, sub_x, sub_y, sub_width, sub_height, (BytesPerPixel < 5 ? fmts[BytesPerPixel] : GL_RGBA), GL_UNSIGNED_BYTE, pixels);
}""",
    """void ZL_Surface::SetPixels(const unsigned char* pixels, int sub_x, int sub_y, int sub_width, int sub_height, int BytesPerPixel)
{
\tstatic const GLenum fmts[] = { GL_RGBA, GL_LUMINANCE, GL_LUMINANCE_ALPHA, GL_RGB, GL_RGBA };
\tglBindTexture(GL_TEXTURE_2D, impl->tex->gltexid);
\tglTexSubImage2D(GL_TEXTURE_2D, 0, sub_x, sub_y, sub_width, sub_height, (BytesPerPixel < 5 ? fmts[BytesPerPixel] : GL_RGBA), GL_UNSIGNED_BYTE, pixels);
}

void ZL_Surface::SetPixelsBGRA(const unsigned char* pixels, int sub_x, int sub_y, int sub_width, int sub_height)
{
\tif (!impl || !impl->tex) return;
\tglBindTexture(GL_TEXTURE_2D, impl->tex->gltexid);
\tglTexSubImage2D(GL_TEXTURE_2D, 0, sub_x, sub_y, sub_width, sub_height, GL_BGRA, GL_UNSIGNED_BYTE, pixels);
}"""
)
