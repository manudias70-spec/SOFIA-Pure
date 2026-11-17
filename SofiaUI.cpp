#include "SofiaUI.h"

#include "third_party/imgui/imgui.h"
#include "third_party/imgui/backends/imgui_impl_opengl3.h"
#include <ZL_Display.h>
#include <ZL_Input.h>
#include <ZL_Application.h>
#include <string>
#include <vector>
#include <libretro-common/include/libretro.h>
#include <dosbox_pure_sta.h>

namespace SofiaUI
{
	static bool initialized = false;
	static bool initializationAttempted = false;
	static bool visible = true; // Show SOFIA as the default home screen.
	static int activePage = 0;

	static std::vector<DBPS_FileBrowserItem> browserEntries;
	static std::string browserPath;
	static unsigned browserRevision = 0;
	static int browserSelection = 0;
	static bool browserActive = false;
	static bool browserWasActive = false;

	static void RefreshBrowserSnapshot()
	{
		browserActive = DBPS_GetFileBrowserSnapshot(browserEntries, browserPath, browserSelection, browserRevision);
	}
 
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
		style.WindowRounding = 0.0f;
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
		{
			activePage = page;
			if (page == 1) DBPS_RequestFileBrowser();
		}
		if (activePage == page)
			ImGui::PopStyleColor();
	}

	void Toggle()
	{
		visible = !visible;
	}

	void Show()
	{
		visible = true;
	}

	bool IsVisible()
	{
		return visible;
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

		// SOFIA is the application home screen, not a floating diagnostic panel.
		ImGui::SetNextWindowPos(ImVec2(0.0f, 0.0f), ImGuiCond_Always);
		ImGui::SetNextWindowSize(io.DisplaySize, ImGuiCond_Always);

		if (ImGui::Begin("SOFIA-Pure  |  MODERN RETRO DOS", NULL,
			ImGuiWindowFlags_NoDecoration | ImGuiWindowFlags_NoMove |
			ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoCollapse |
			ImGuiWindowFlags_NoSavedSettings))
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
			// Reserve enough vertical space for the complete footer controls.
			// The previous 42px offset clipped the return button at the bottom.
			ImGui::SetCursorPosY(ImGui::GetWindowHeight() - 100.0f);
			ImGui::Separator();
			ImGui::TextDisabled("ALT + F12  |  Acceso rapido");
			if (ImGui::Button("Volver al explorador", ImVec2(-1.0f, 34.0f)))
				visible = false;
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
				{
					activePage = 1;
					DBPS_RequestFileBrowser();
				}
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
				RefreshBrowserSnapshot();
				ImGui::Text("Explorador de DOSBox Pure");
				ImGui::SameLine();
				if (ImGui::SmallButton("Actualizar##pure")) DBPS_RequestFileBrowser();
				ImGui::TextDisabled("%s", browserPath.c_str());
				ImGui::BeginChild("BrowserList", ImVec2(0.0f, 0.0f), true);
				if (!browserActive)
				{
					ImGui::TextDisabled("El explorador de Pure no esta activo.");
					if (ImGui::Button("Abrir explorador", ImVec2(180.0f, 34.0f)))
						DBPS_RequestFileBrowser();
				}
				else if (browserEntries.empty())
					ImGui::TextDisabled("Pure no devolvio elementos para esta ubicacion.");
				else for (size_t i = 0; i < browserEntries.size(); ++i)
				{
					const DBPS_FileBrowserItem& entry = browserEntries[i];
					if (entry.type == 0)
					{
						if (entry.text.empty()) ImGui::Spacing();
						else if (entry.info == 10) ImGui::TextColored(ImVec4(0.35f, 0.82f, 0.96f, 1.0f), "%s", entry.text.c_str());
						else if (entry.info == 12) ImGui::TextDisabled("%s", entry.text.c_str());
						else ImGui::TextWrapped("%s", entry.text.c_str());
						continue;
					}
					ImGui::PushID((int)i);
					if (ImGui::Selectable(entry.text.c_str(), (int)i == browserSelection, 0, ImVec2(0.0f, 27.0f)))
						DBPS_RequestFileBrowserSelection((unsigned)i, browserRevision);
					ImGui::PopID();
				}
				ImGui::EndChild();
				ImGui::TextDisabled("%u elementos  |  Lista y acciones administradas por DOSBox Pure", (unsigned)browserEntries.size());
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
			// Exit action lives in the conventional lower-right corner of the main area.
			ImGui::SetCursorPos(ImVec2(ImGui::GetWindowWidth() - 218.0f, ImGui::GetWindowHeight() - 48.0f));
			const ImVec2 exitButtonPos = ImGui::GetCursorScreenPos();
			if (ImGui::Button("     Salir al escritorio", ImVec2(198.0f, 36.0f)))
				ImGui::OpenPopup("Confirmar salida");
			// Small door-and-arrow pictogram, drawn directly so it works with the bundled font.
			ImDrawList* draw = ImGui::GetWindowDrawList();
			const ImU32 doorColor = IM_COL32(80, 195, 235, 255);
			draw->AddRect(ImVec2(exitButtonPos.x + 12.0f, exitButtonPos.y + 8.0f),
				ImVec2(exitButtonPos.x + 25.0f, exitButtonPos.y + 28.0f), doorColor, 1.5f, 0, 1.8f);
			draw->AddCircleFilled(ImVec2(exitButtonPos.x + 21.0f, exitButtonPos.y + 18.0f), 1.2f, doorColor);
			draw->AddLine(ImVec2(exitButtonPos.x + 4.0f, exitButtonPos.y + 18.0f),
				ImVec2(exitButtonPos.x + 10.0f, exitButtonPos.y + 18.0f), doorColor, 1.8f);
			draw->AddLine(ImVec2(exitButtonPos.x + 7.0f, exitButtonPos.y + 15.0f),
				ImVec2(exitButtonPos.x + 10.0f, exitButtonPos.y + 18.0f), doorColor, 1.8f);
			draw->AddLine(ImVec2(exitButtonPos.x + 7.0f, exitButtonPos.y + 21.0f),
				ImVec2(exitButtonPos.x + 10.0f, exitButtonPos.y + 18.0f), doorColor, 1.8f);
			ImGui::EndChild();
		}
		ImGui::End();

		if (ImGui::BeginPopupModal("Confirmar salida", NULL, ImGuiWindowFlags_AlwaysAutoResize))
		{
			ImGui::Text("¿Querés cerrar SOFIA-Pure y volver al escritorio?");
			ImGui::Spacing();
			if (ImGui::Button("Cancelar", ImVec2(110.0f, 32.0f)))
				ImGui::CloseCurrentPopup();
			ImGui::SameLine();
			if (ImGui::Button("Salir", ImVec2(110.0f, 32.0f)))
				ZL_Application::Quit();
			ImGui::EndPopup();
		}

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
