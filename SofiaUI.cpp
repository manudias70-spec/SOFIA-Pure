#include "SofiaUI.h"

#include "third_party/imgui/imgui.h"
#include "third_party/imgui/backends/imgui_impl_opengl3.h"
#include <ZL_Display.h>

namespace SofiaUI
{
	static bool initialized = false;

	static bool Initialize()
	{
		if (initialized) return true;

		IMGUI_CHECKVERSION();
		ImGui::CreateContext();

		ImGuiIO& io = ImGui::GetIO();
		io.IniFilename = NULL;
		io.LogFilename = NULL;
		io.DisplaySize = ImVec2((float)ZL_Display::Width, (float)ZL_Display::Height);
		io.DisplayFramebufferScale = ImVec2(1.0f, 1.0f);

		ImGui::StyleColorsDark();
		ImGuiStyle& style = ImGui::GetStyle();
		style.WindowRounding = 8.0f;
		style.FrameRounding = 4.0f;
		style.Colors[ImGuiCol_WindowBg] = ImVec4(0.025f, 0.045f, 0.070f, 0.96f);
		style.Colors[ImGuiCol_TitleBg] = ImVec4(0.025f, 0.075f, 0.115f, 1.0f);
		style.Colors[ImGuiCol_TitleBgActive] = ImVec4(0.025f, 0.20f, 0.29f, 1.0f);
		style.Colors[ImGuiCol_CheckMark] = ImVec4(0.10f, 0.82f, 0.96f, 1.0f);
		style.Colors[ImGuiCol_SliderGrab] = ImVec4(0.08f, 0.68f, 0.84f, 1.0f);
		style.Colors[ImGuiCol_Button] = ImVec4(0.04f, 0.20f, 0.28f, 1.0f);
		style.Colors[ImGuiCol_ButtonHovered] = ImVec4(0.05f, 0.34f, 0.46f, 1.0f);
		style.Colors[ImGuiCol_ButtonActive] = ImVec4(0.04f, 0.48f, 0.62f, 1.0f);

		if (!ImGui_ImplOpenGL3_Init("#version 140"))
		{
			ImGui::DestroyContext();
			return false;
		}

		initialized = true;
		return true;
	}

	void Draw()
	{
		if (!Initialize()) return;

		ImGuiIO& io = ImGui::GetIO();
		io.DisplaySize = ImVec2((float)ZL_Display::Width, (float)ZL_Display::Height);
		io.DisplayFramebufferScale = ImVec2(1.0f, 1.0f);
		io.DeltaTime = 1.0f / 60.0f;

		ImGui_ImplOpenGL3_NewFrame();
		ImGui::NewFrame();

		ImGui::SetNextWindowPos(ImVec2(18.0f, 18.0f), ImGuiCond_FirstUseEver);
		ImGui::SetNextWindowSize(ImVec2(360.0f, 158.0f), ImGuiCond_FirstUseEver);
		if (ImGui::Begin("SOFIA-Pure | Diagnostico", NULL, ImGuiWindowFlags_NoCollapse))
		{
			ImGui::TextColored(ImVec4(0.18f, 0.82f, 0.96f, 1.0f), "SOFIA UI / OPENGL CORE");
			ImGui::Separator();
			ImGui::Text("Estado: inicializado");
			ImGui::Text("Ventana: %.0f x %.0f", io.DisplaySize.x, io.DisplaySize.y);
			ImGui::Text("Renderer: OpenGL3 | GLSL 140");
			ImGui::Text("Motor DOSBox: sin modificaciones");
		}
		ImGui::End();

		ImGui::Render();
		ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
	}

	void Shutdown()
	{
		if (!initialized) return;
		ImGui_ImplOpenGL3_Shutdown();
		ImGui::DestroyContext();
		initialized = false;
	}
}
