/*
 *  Copyright (C) 2020-2026 Bernhard Schelling
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License along
 *  with this program; if not, write to the Free Software Foundation, Inc.,
 *  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 */

#include <ZL_Application.h>
#include <ZL_Display.h>
#include <ZL_Surface.h>
#include <ZL_Audio.h>
#include <ZL_Font.h>
#include <ZL_Data.h>
#include <ZL_Input.h>
#include <ZL_Thread.h>
#include <ZL_Math3D.h>
#include <ZL_Network.h>

#if defined(_MSC_VER) || defined(__MINGW32__) || defined(__WIN32__) || defined(WIN32) || defined(_WIN32)
#include <windows.h>
#include <commdlg.h>
#endif

#include <cfloat>
#include <vector>

#include <libretro-common/include/libretro.h>
#include <include/cross.h>
#include "vfs_implementation.h"
#include "xbrz_shader.h"
#include "sofia_splash.h"
#include "sofia_game_profile.h"
#include "imgui.h"
#include "imgui_internal.h"
#include "backends/imgui_impl_opengl3.h"
#include <algorithm>
#include <string>
#include <map>
#include <cmath>
#define STBI_NO_STDIO
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"
