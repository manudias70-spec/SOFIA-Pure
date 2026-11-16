#pragma once

namespace SofiaUI
{
	// Draw the first diagnostic overlay. Initialization is lazy and safe to call each frame.
	void Draw();

	// Toggle the optional in-game overlay (Alt+F12).
	void Toggle();

	// Show the SOFIA home screen after a game exits.
	void Show();

	// Report whether the SOFIA interface currently owns the screen.
	bool IsVisible();

	// Release ImGui renderer resources while the host OpenGL context is still alive.
	void Shutdown();
}
