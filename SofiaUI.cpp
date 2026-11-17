#include "SofiaUI.h"

#include "third_party/imgui/imgui.h"
#include "third_party/imgui/backends/imgui_impl_opengl3.h"
#include <ZL_Display.h>
#include <ZL_Input.h>
#include <ZL_Application.h>
#include <algorithm>
#include <cctype>
#include <string>
#include <vector>
#include <libretro-common/include/libretro.h>
#include <include/cross.h>
#include "vfs_implementation.h"
#include <dosbox_pure_sta.h>

namespace SofiaUI
{
	static bool initialized = false;
	static bool initializationAttempted = false;
	static bool visible = true; // Show SOFIA as the default home screen.
	static int activePage = 0;

	struct BrowserEntry
	{
		std::string name;
		bool isDirectory;
		unsigned size = 0;
	};

	static std::vector<BrowserEntry> browserEntries;
	static std::string browserCachedPath;
	static bool browserDirty = true;
	static bool browserReadError = false;
	static bool dosBrowserActive = false;
	static bool dosScanWaiting = false;
	static unsigned dosDrive = 2;
	static std::string dosPath;
	static std::vector<BrowserEntry> dosBrowserEntries;

	static bool IsSupportedContentFile(const char* name, const char* validExtensions)
	{
		if (!name || !validExtensions) return false;
		const char* dot = strrchr(name, '.');
		if (!dot || !dot[1]) return false;
		std::string extension(dot + 1);
		std::transform(extension.begin(), extension.end(), extension.begin(),
			[](unsigned char ch) { return (char)std::tolower(ch); });
		std::string extensions(validExtensions);
		std::transform(extensions.begin(), extensions.end(), extensions.begin(),
			[](unsigned char ch) { return (char)std::tolower(ch); });
		const std::string token = "|" + extension + "|";
		return ("|" + extensions + "|").find(token) != std::string::npos;
	}

	static void RefreshBrowser()
	{
		browserEntries.clear();
		if (DBPS_BrowsePath.empty()) Cross::MakePathAbsolute(DBPS_BrowsePath);
		else Cross::NormalizePath(DBPS_BrowsePath);

		retro_system_info info = {};
		retro_get_system_info(&info);
		libretro_vfs_implementation_dir* dir = retro_vfs_opendir_impl(DBPS_BrowsePath.c_str(), false);
		browserReadError = (dir == NULL);
		if (dir)
		{
			while (retro_vfs_readdir_impl(dir))
			{
				const char* entryName = retro_vfs_dirent_get_name_impl(dir);
				if (!entryName || !strcmp(entryName, ".")) continue;
				const bool isDirectory = retro_vfs_dirent_is_dir_impl(dir);
				if (isDirectory || IsSupportedContentFile(entryName, info.valid_extensions))
					browserEntries.push_back({ entryName, isDirectory });
			}
			retro_vfs_closedir_impl(dir);
		}

		std::sort(browserEntries.begin(), browserEntries.end(),
			[](const BrowserEntry& a, const BrowserEntry& b)
			{
				if (a.isDirectory != b.isDirectory) return a.isDirectory;
				std::string an = a.name, bn = b.name;
				std::transform(an.begin(), an.end(), an.begin(), [](unsigned char ch) { return (char)std::tolower(ch); });
				std::transform(bn.begin(), bn.end(), bn.begin(), [](unsigned char ch) { return (char)std::tolower(ch); });
				return an < bn;
			});
		browserCachedPath = DBPS_BrowsePath;
		browserDirty = false;
	}

	static void BrowserGoUp()
	{
		std::string& path = DBPS_BrowsePath;
		while (path.size() > 3 && (path.back() == 92 || path.back() == '/')) path.pop_back();
		const size_t slash = path.find_last_of(std::string(1, (char)92) + "/");
		if (slash == std::string::npos) path.clear();
		else if (slash == 2 && path.size() >= 3 && path[1] == ':') path.resize(3);
		else if (slash == 0) path.resize(1);
		else if (slash + 1 < path.size()) path.resize(slash);
		browserDirty = true;
	}

	static void BrowserEnterDirectory(const std::string& name)
	{
		if (name == "..") { BrowserGoUp(); return; }
		if (!DBPS_BrowsePath.empty() && DBPS_BrowsePath.back() != 92 && DBPS_BrowsePath.back() != '/')
			DBPS_BrowsePath += (char)92;
		DBPS_BrowsePath += name;
		browserDirty = true;
	}

	static void BrowserOpenFile(const std::string& name)
	{
		std::string fullPath = DBPS_BrowsePath;
		if (!fullPath.empty() && fullPath.back() != 92 && fullPath.back() != '/')
			fullPath += (char)92;
		fullPath += name;

		// DOSBox Pure reloads the selected content directly on its emulation thread.
		// Keep the SOFIA desktop hidden while the new DOS content starts.
		DBPS_OpenContent(fullPath.c_str());
		visible = false;
	}

	static void RequestDOSDirectory()
	{
		if (!dosScanWaiting && !DBPS_IsDriveDirectoryScanPending())
			dosScanWaiting = DBPS_RequestDriveDirectory(dosDrive, dosPath.c_str());
	}

	static void RefreshDOSDirectoryCache()
	{
		if (!dosScanWaiting || DBPS_IsDriveDirectoryScanPending()) return;
		dosBrowserEntries.clear();
		const size_t count = DBPS_GetDriveDirectoryCount();
		for (size_t i = 0; i < count; ++i)
		{
			DBPS_DriveDirectoryEntry entry;
			if (DBPS_GetDriveDirectoryEntry(i, entry))
				dosBrowserEntries.push_back({ entry.name, entry.isDirectory, entry.size });
		}
		std::sort(dosBrowserEntries.begin(), dosBrowserEntries.end(),
			[](const BrowserEntry& a, const BrowserEntry& b)
			{
				if (a.isDirectory != b.isDirectory) return a.isDirectory;
				std::string an = a.name, bn = b.name;
				std::transform(an.begin(), an.end(), an.begin(), [](unsigned char ch) { return (char)std::tolower(ch); });
				std::transform(bn.begin(), bn.end(), bn.begin(), [](unsigned char ch) { return (char)std::tolower(ch); });
				return an < bn;
			});
		dosScanWaiting = false;
	}

	static void DOSGoUp()
	{
		while (!dosPath.empty() && (dosPath.back() == '\\\\' || dosPath.back() == '/')) dosPath.pop_back();
		const size_t slash = dosPath.find_last_of("\\\\/");
		if (slash == std::string::npos) dosPath.clear();
		else dosPath.resize(slash);
		dosScanWaiting = false;
		RequestDOSDirectory();
	}

	static void DOSEnterDirectory(const std::string& name)
	{
		if (!dosPath.empty() && dosPath.back() != '\\\\' && dosPath.back() != '/') dosPath += '\\\\';
		dosPath += name;
		dosScanWaiting = false;
		RequestDOSDirectory();
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
			activePage = page;
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
				if (ImGui::Button("Archivos del equipo"))
				{
					dosBrowserActive = false;
					browserDirty = true;
				}
				ImGui::SameLine();
				if (ImGui::Button("Unidades DOS montadas"))
				{
					dosBrowserActive = true;
					dosPath.clear();
					dosScanWaiting = false;
				}
				ImGui::Separator();

				if (!dosBrowserActive)
				{
					if (browserDirty || browserCachedPath != DBPS_BrowsePath) RefreshBrowser();
					ImGui::Text("Explorador del equipo");
					ImGui::SameLine();
					if (ImGui::SmallButton("Actualizar##host")) { browserDirty = true; RefreshBrowser(); }
					ImGui::TextDisabled("%s", DBPS_BrowsePath.c_str());
					if (ImGui::Button("Subir un nivel##host", ImVec2(130.0f, 30.0f)))
					{
						BrowserGoUp();
						RefreshBrowser();
					}
					ImGui::BeginChild("BrowserList", ImVec2(0.0f, 0.0f), true);
					if (browserReadError) ImGui::TextDisabled("No se pudo leer este directorio.");
					else if (browserEntries.empty()) ImGui::TextDisabled("No hay carpetas ni archivos compatibles en esta ubicacion.");
					else for (size_t i = 0; i < browserEntries.size(); ++i)
					{
						const BrowserEntry& entry = browserEntries[i];
						const std::string label = (entry.isDirectory ? "[DIR]  " : "[FILE] ") + entry.name;
						if (ImGui::Selectable(label.c_str(), false, 0, ImVec2(0.0f, 27.0f)))
						{
							if (entry.isDirectory) { BrowserEnterDirectory(entry.name); RefreshBrowser(); }
							else BrowserOpenFile(entry.name);
							break;
						}
					}
					ImGui::EndChild();
					ImGui::TextDisabled("%u elementos  |  Seleccioná una ISO o ZIP para iniciarlo", (unsigned)browserEntries.size());
				}
				else
				{
					const unsigned mounted = DBPS_GetMountedDriveMask();
					ImGui::Text("Unidades detectadas por DOSBox Pure");
					bool selectedDriveStillMounted = (mounted & (1u << dosDrive)) != 0;
					for (unsigned drive = 0; drive < 26; ++drive)
					{
						if (!(mounted & (1u << drive))) continue;
						std::string label(1, (char)('A' + drive)); label += ":";
						ImGui::SameLine();
						if (ImGui::SmallButton(label) && drive != dosDrive)
						{
							dosDrive = drive;
							dosPath.clear();
							dosScanWaiting = false;
						}
					}
					if (!selectedDriveStillMounted)
					{
						ImGui::TextDisabled("No hay una unidad DOS seleccionada.");
					}
					else
					{
						ImGui::TextDisabled("%c:\\%s", 'A' + dosDrive, dosPath.c_str());
						if (ImGui::Button("Subir un nivel##dos", ImVec2(130.0f, 30.0f))) DOSGoUp();
						ImGui::SameLine();
						if (ImGui::SmallButton("Actualizar##dos")) { dosScanWaiting = false; RequestDOSDirectory(); }
						RequestDOSDirectory();
						RefreshDOSDirectoryCache();
						ImGui::Separator();
						ImGui::BeginChild("DOSBrowserList", ImVec2(0.0f, 0.0f), true);
						if (dosScanWaiting || DBPS_IsDriveDirectoryScanPending())
							ImGui::TextDisabled("Leyendo la unidad DOS...");
						else if (dosBrowserEntries.empty())
							ImGui::TextDisabled("Esta carpeta esta vacia o Pure no devolvio entradas.");
						else for (size_t i = 0; i < dosBrowserEntries.size(); ++i)
						{
							const BrowserEntry& entry = dosBrowserEntries[i];
							const std::string label = (entry.isDirectory ? "[DIR]  " : "[FILE] ") + entry.name;
							if (ImGui::Selectable(label.c_str(), false, 0, ImVec2(0.0f, 27.0f)) && entry.isDirectory)
								DOSEnterDirectory(entry.name);
						}
						ImGui::EndChild();
						ImGui::TextDisabled("%u elementos  |  Vista de solo lectura del contenido montado", (unsigned)dosBrowserEntries.size());
					}
				}
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
