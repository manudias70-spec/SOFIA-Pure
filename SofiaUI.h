#pragma once

namespace SofiaUI
{
	// Draw the first diagnostic overlay. Initialization is lazy and safe to call each frame.
	void Draw();

	// Release ImGui renderer resources while the host OpenGL context is still alive.
	void Shutdown();
}
