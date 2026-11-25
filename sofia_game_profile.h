#ifndef SOFIA_GAME_PROFILE_H
#define SOFIA_GAME_PROFILE_H

#include <map>
#include <string>

// Base template for one game entry in the permanent launcher library.
//
// The user-provided name is the permanent, visible identity of the card.
// The stable ID is the internal key used to associate the card with its
// executable, setup program, artwork and per-game option data. Option data
// must be stored by profile ID, never by the editable filesystem path.
class SofiGameProfileTemplate
{
public:
    explicit SofiGameProfileTemplate(const std::string& stableId,
                                     const std::string& userGameName)
        : m_id(stableId), m_name(userGameName), filter(0), hasCyclesMax(false)
    {
    }

    const std::string& Id() const { return m_id; }
    const std::string& Name() const { return m_name; }

    // These paths belong to this card only. Empty means not configured yet.
    std::string exePath;
    std::string setupPath;
    std::string imagePath;

    // Per-game settings are owned by this profile and keyed by option name.
    int filter;
    std::string cyclesMax;
    bool hasCyclesMax;
    std::map<std::string, std::string> videoOptions;
    std::map<std::string, std::string> audioOptions;
    std::map<std::string, std::string> coreOptions;

private:
    // Intentionally no public name setter: the name is fixed at creation.
    std::string m_id;
    std::string m_name;
};

#endif // SOFIA_GAME_PROFILE_H
