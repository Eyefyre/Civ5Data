import sqlite3

language_map = {"English":"Language_en_US","German":"Language_DE_DE","French":"Language_FR_FR","Italian":"Language_IT_IT","Spanish":"Language_ES_ES","Russian":"Language_RU_RU","Polish":"Language_PL_PL","Japanese":"Language_JA_JP","Korean":"Language_KO_KR","Chinese":"Language_ZH_HANT_HK"}
# con = sqlite3.connect("../DataBases/Civ5DebugDatabase.db")

# cur = con.cursor()

# cur.execute('SELECT * FROM Civilizations;')
# civilizations = cur.fetchall()

# con.close()

def get_Localization(tag,language):
    con = sqlite3.connect("../DataBases/Localization-Full.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM ' + language_map[language] + ' where Tag = "' + tag + '";')
    localization = cur.fetchall()
    return localization

print(get_Localization("TXT_KEY_POLICY_COLLECTIVE_RULE_HELP","English"))