import sqlite3
import json
language_map = {"English": "Language_en_US", "German": "Language_DE_DE", "French": "Language_FR_FR", "Italian": "Language_IT_IT", "Spanish": "Language_ES_ES",
                "Russian": "Language_RU_RU", "Polish": "Language_PL_PL", "Japanese": "Language_JA_JP", "Korean": "Language_KO_KR", "Chinese": "Language_ZH_HANT_HK"}
languages = ["English", "German", "French", "Italian", "Spanish",
             "Russian", "Polish", "Japanese", "Korean", "Chinese"]
text_replacements = ["[ICON_CAPITAL]","[ICON_CITIZEN]","[ICON_CONNECTED]","[ICON_DIPLOMAT]", "[ICON_TOURISM]", "[ICON_RES_URANIUM]", "[TAB]", "[NEWLINE]", "[COLOR_POSITIVE_TEXT]", "[ENDCOLOR]", "[ICON_FOOD]", "[ICON_PEACE]", "[ICON_RES_COW]", "[ICON_RES_SHEEP]", "[ICON_RES_HORSE]", "[ICON_PRODUCTION]", "[ICON_RES_FISH]", "[ICON_RES_PEARLS]", "[ICON_HAPPINESS_1]",
                     "[ICON_RESEARCH]", "[ICON_RES_DEER]","[ICON_RANGE_STRENGTH]","[ICON_MOVES]", "[ICON_RES_ALUMINUM]", "[NEWLINE", "[ICON_RES_OIL]","[ICON_INFLUENCE]", "[ICON_RES_COAL]", "[ICON_STRENGTH]", "[ICON_GREAT_PEOPLE]", "[ICON_RES_IVORY]", "[ICON_RES_FUR]", "[ICON_RES_TRUFFLES]", "[ICON_GOLD]", "[ICON_RES_MARBLE]", "[ICON_OCCUPIED]", "[ICON_HAPPINESS_4]", "[ICON_GOLDEN_AGE]", "[ICON_CULTURE]", "[ICON_RES_IRON]","   ","  "]
con = sqlite3.connect("../DataBases/Civ5DebugDatabase.db")
cur = con.cursor()


def get_Localization(tag, language):
    connection = sqlite3.connect("../DataBases/Localization-Full.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM ' + language_map[language] + ' where Tag = "' + tag + '";')
    localization = cursor.fetchone()
    return clean_text(localization[1])

def clean_text(text):
    for r in text_replacements:
        text = text.replace(r,"")
    return text.strip()

def get_prereq_techs(techTag,lang):
    prerequisiteTechs = []
    cur.execute('SELECT PrereqTech FROM Technology_PrereqTechs where TechType = "' + techTag + '";')
    prereqs = cur.fetchall()
    if prereqs != []:
        for prereq in prereqs:
            if prereq[0] == "TECH_PLASTIC":
                prerequisiteTechs.append(get_Localization("TXT_KEY_"+prereq[0]+"S_TITLE",lang))
            else:
                prerequisiteTechs.append(get_Localization("TXT_KEY_"+prereq[0]+"_TITLE",lang))
    return prerequisiteTechs

def get_unit_unlocks(techTag,lang):
    unit_unlocks = []
    cur.execute('SELECT Description FROM Units where Prereqtech = "' + techTag + '";')
    units = cur.fetchall()
    for unit in units:
        unit_unlocks.append(get_Localization(unit[0],lang))
    return unit_unlocks

def get_building_unlocks(techTag,lang):
    building_unlocks = []
    cur.execute('SELECT Description FROM Buildings where Prereqtech = "' + techTag + '";')
    buildings = cur.fetchall()
    for building in buildings:
        building_unlocks.append(get_Localization(building[0],lang))
    return building_unlocks

cur.execute('SELECT * FROM Technologies;')
Technologies = cur.fetchall()

for lang in languages:
    tech_list = []
    for technology in Technologies:
        cur.execute('SELECT Description FROM Eras where Type = "'+ technology[9] +'";')
        era = cur.fetchone()[0]
        tech = {
            "id": int(technology[0]) + 1,
            "name": get_Localization(technology[2], lang),
            "civilopedia": get_Localization(technology[3], lang),
            "help_text": get_Localization(technology[4], lang),
            "era_requirement": get_Localization(era, lang),
            "quote": get_Localization(technology[47], lang),
            "prereq_techs": get_prereq_techs(technology[1],lang),
            "cost": technology[7],
            "building_unlocks": get_building_unlocks(technology[1],lang),
            "unit_unlocks": get_unit_unlocks(technology[1],lang)
        }
        tech_list.append(tech)

    json_object = json.dumps(tech_list)
    with open("../Data/" + lang + "/Technologies.json", "w") as outfile:
        outfile.write(json_object)

con.close()

