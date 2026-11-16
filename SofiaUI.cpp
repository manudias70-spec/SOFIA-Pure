#include "SofiaUI.h"

#include "third_party/imgui/imgui.h"
#include "third_party/imgui/backends/imgui_impl_opengl3.h"
#include <ZL_Display.h>
#include <ZL_Input.h>

namespace SofiaUI
{
	static bool initialized = false;
	static bool initializationAttempted = false;
	static bool visible = false;
	static int activePage = 0;

	static bool Initialize()
	{
		if (initialized) return true;
		if (initializationAttempted) return false;
		initializationAttempted = true;

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
		style.ChildRounding = 6.0f;
		style.FrameRounding = 4.0f;
		style.WindowPadding = ImVec2(14.0f, 14.0f);
		style.ItemSpacing = ImVec2(9.0f, 8.0f);
		style.Colors[ImGuiCol_WindowBg] = ImVec4(0.025f, 0.045f, 0.070f, 0.97f);
		style.Colors[ImGuiCol_ChildBg] = ImVec4(0.035f, 0.065f, 0.095f, 1.0f);
		style.Colors[ImGuiCol_Border] = ImVec4(0.08f, 0.22f, 0.30f, 0.8f);
		style.Colors[ImGuiCol_TitleBg] = ImVec4(0.025f, 0.075f, 0.115f, 1.0f);
		style.Colors[ImGuiCol_TitleBgActive] = ImVec4(0.025f, 0.20f, 0.29f, 1.0f);
		style.Colors[ImGuiCol_CheckMark] = ImVec4(0.10f, 0.82f, 0.96f, 1.0f);
		style.Colors[ImGuiCol_SliderGrab] = ImVec4(0.08f, 0.68f, 0.84f, 1.0f);
		style.Colors[ImGuiCol_Button] = ImVec4(0.04f, 0.16f, 0.23f, 1.0f);
		style.Colors[ImGuiCol_ButtonHovered] = ImVec4(0.05f, 0.34f, 0.46f, 1.0f);
		style.Colors[ImGuiCol_ButtonActive] = ImVec4(0.04f, 0.48f, 0.62f, 1.0f);
		style.Colors[ImGuiCol_Header] = ImVec4(0.04f, 0.20f, 0.28f, 1.0f);
		style.Colors[ImGuiCol_HeaderHovered] = ImVec4(0.05f, 0.34f, 0.46f, 1.0f);
		style.Colors[ImGuiCol_HeaderActive] = ImVec4(0.04f, 0.48f, 0.62f, 1.0f);

		if (!ImGui_ImplOpenGL3_Init("#version 140"))
		{
			ImGui::DestroyContext();
			return false;
		}

		initialized = true;
		return true;
	}

	static void NavigationButton(const char* label, int page)
	{
		if (activePage == page)
			ImGui::PushStyleColor(ImGuiCol_Button, ImVec4(0.04f, 0.31f, 0.42f, 1.0f));
		if (ImGui::Button(label, ImVec2(-1.0f, 38.0f)))
			activePage = page;
		if (activePage == page)
			ImGui::PopStyleColor();
	}

	void Toggle()
	{
		visible = !visible;
	}

	void Draw()
	{
		if (!visible || !Initialize()) return;

		ImGuiIO& io = ImGui::GetIO();
		io.DisplaySize = ImVec2((float)ZL_Display::Width, (float)ZL_Display::Height);
		io.DisplayFramebufferScale = ImVec2(1.0f, 1.0f);
		io.DeltaTime = 1.0f / 60.0f;

		// Feed ImGui from the same ZillaLib input layer used by the standalone host.
		// ZillaLib's pointer uses a bottom-left origin; ImGui uses a top-left origin.
		const ZL_Vector pointer = ZL_Input::Pointer();
		io.AddMousePosEvent(pointer.x, (float)ZL_Display::Height - pointer.y);
		io.AddMouseButtonEvent(0, ZL_Input::Held(ZL_BUTTON_LEFT));
		io.AddMouseButtonEvent(1, ZL_Input::Held(ZL_BUTTON_RIGHT));
		io.AddMouseButtonEvent(2, ZL_Input::Held(ZL_BUTTON_MIDDLE));
		const float wheel = (float)ZL_Input::MouseWheel();
		if (wheel != 0.0f) io.AddMouseWheelEvent(0.0f, wheel);

		ImGui_ImplOpenGL3_NewFrame();
		ImGui::NewFrame();

		const float windowWidth = (io.DisplaySize.x > 800.0f ? 760.0f : io.DisplaySize.x - 36.0f);
		const float windowHeight = (io.DisplaySize.y > 500.0f ? 440.0f : io.DisplaySize.y - 36.0f);
		ImGui::SetNextWindowPos(ImVec2(18.0f, 18.0f), ImGuiCond_Always);
		ImGui::SetNextWindowSize(ImVec2(windowWidth, windowHeight), ImGuiCond_Always);

		if (ImGui::Begin("SOFIA-Pure  |  MODERN RETRO DOS", NULL,
			ImGuiWindowFlags_NoCollapse | ImGuiWindowFlags_NoResize))
		{
			ImGui::BeginChild("Navigation", ImVec2(164.0f, 0.0f), true);
			ImGui::TextColored(ImVec4(0.18f, 0.82f, 0.96f, 1.0f), "SOFIA");
			ImGui::TextDisabled("PURE ENVIRONMENT");
			ImGui::Separator();
			ImGui::Spacing();
			NavigationButton("Inicio", 0);
			NavigationButton("Biblioteca", 1);
			NavigationButton("Configuracion", 2);
			NavigationButton("Acerca de", 3);
			ImGui::SetCursorPosY(ImGui::GetWindowHeight() - 42.0f);
			ImGui::Separator();
			ImGui::TextDisabled("ALT + F12  |  Cerrar");
			ImGui::EndChild();

			ImGui::SameLine();
			ImGui::BeginChild("MainContent", ImVec2(0.0f, 0.0f), true);
			if (activePage == 0)
			{
				ImGui::TextColored(ImVec4(0.18f, 0.82f, 0.96f, 1.0f), "CENTRO DE CONTROL");
				ImGui::Separator();
				ImGui::Spacing();
				ImGui::Text("Bienvenido a SOFIA-Pure");
				ImGui::TextDisabled("Tu entorno DOS, renovado.");
				ImGui::Spacing();
				ImGui::BeginChild("EngineStatus", ImVec2(0.0f, 92.0f), true);
				ImGui::TextColored(ImVec4(0.25f, 0.88f, 0.62f, 1.0f), "MOTOR ACTIVO");
				ImGui::Text("Resolucion actual: %.0f x %.0f", io.DisplaySize.x, io.DisplaySize.y);
				ImGui::TextDisabled("La base original y sus funciones se mantienen.");
				ImGui::EndChild();
				ImGui::Spacing();
				ImGui::Text("Acceso rapido");
				if (ImGui::Button("Abrir biblioteca", ImVec2(180.0f, 38.0f)))
					activePage = 1;
				ImGui::SameLine();
				if (ImGui::Button("Ver configuracion", ImVec2(180.0f, 38.0f)))
					activePage = 2;
				ImGui::Spacing();
				ImGui::TextDisabled("Interfaz en construccion. No modifica la configuracion del emulador.");
			}
			else if (activePage == 1)
			{
				ImGui::TextColored(ImVec4(0.18f, 0.82f, 0.96f, 1.0f), "BIBLIOTECA");
				ImGui::Separator();
				ImGui::Spacing();
				ImGui::Text("Explorador de juegos y archivos");
				ImGui::TextDisabled("Proxima etapa: navegador de doble panel inspirado en Norton Commander.");
				ImGui::Spacing();
				ImGui::BeginChild("LibraryPreview", ImVec2(0.0f, 150.0f), true);
				ImGui::TextDisabled("Aun no hay elementos para mostrar.");
				ImGui::EndChild();
			}
			else if (activePage == 2)
			{
				ImGui::TextColored(ImVec4(0.18f, 0.82f, 0.96f, 1.0f), "CONFIGURACION");
				ImGui::Separator();
				ImGui::Spacing();
				ImGui::Text("Ajustes de SOFIA-Pure");
				ImGui::TextDisabled("Los controles se incorporaran por etapas.");
				ImGui::TextDisabled("Por ahora, esta pantalla es solo una vista previa.");
			}
			else
			{
				ImGui::TextColored(ImVec4(0.18f, 0.82f, 0.96f, 1.0f), "ACERCA DE");
				ImGui::Separator();
				ImGui::Spacing();
				ImGui::Text("SOFIA-Pure");
				ImGui::Text("Modern Retro DOS");
				ImGui::Spacing();
				ImGui::TextDisabled("Una interfaz nueva sobre una base DOSBox conservada.");
				ImGui::TextDisabled("Proyecto independiente. Solo Windows por ahora.");
			}
			ImGui::EndChild();
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
		initializationAttempted = false;
	}
}
