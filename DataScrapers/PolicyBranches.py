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
        text = text.replace(r, " ")
    return text.strip()

def get_prereq_policies(policyTag):
    cur.execute('SELECT PrereqPolicy FROM Policy_PrereqPolicies where PolicyType = "' + policyTag + '";')
    prereqs = cur.fetchall()
    prereqpolicies = []
    if prereqs != []:
        for pre in prereqs:
            prereqpolicies.append(get_Localization("TXT_KEY_" + pre[0],lang))
    return prereqpolicies

def get_policies_of_branch(branchTag):
    cur.execute('SELECT * FROM Policies where PolicyBranchType = "' + branchTag + '";')
    policies = cur.fetchall()
    pols = []
    for policy in policies:
        pol = {
            "name": get_Localization(policy[2],lang),
            "civilopedia": get_Localization(policy[3],lang),
            "help_text": get_Localization(policy[5],lang).replace(get_Localization(policy[2],lang),"").strip(),
            "level": policy[11],
            "prereq_policies": get_prereq_policies(policy[1])
        }
        pols.append(pol)
    return pols


cur.execute('SELECT * FROM PolicyBranchTypes;')
PolicyBranches = cur.fetchall()

for lang in languages:
    branch_list = []
    for branch in PolicyBranches:
        era = None
        if branch[7] != None:
            cur.execute('SELECT Description FROM Eras where Type = "'+ branch[7] +'";')
            era = cur.fetchone()[0]
            era = get_Localization(era,lang)
        get_policies_of_branch(branch[1])
        policybranch = {
            "id": int(branch[0]) + 1,
            "name": get_Localization(branch[2], lang),
            "help_text": get_Localization(branch[5],lang),
            "era_requirement": era,
            "policies": get_policies_of_branch(branch[1])
        }
        branch_list.append(policybranch)

    json_object = json.dumps(branch_list)
    with open("../Data/" + lang + "/PolicyBranches.json", "w") as outfile:
        outfile.write(json_object)

con.close()
