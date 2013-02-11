# -*- coding: utf-8 -*-

# These are found in Repack-MPQ/fileset.{locale}#Mods#Core.SC2Mod#{locale}.SC2Data/LocalizedData/Editor/EditorCategoryStrings.txt
# EDSTR_CATEGORY_Race
# EDSTR_PLAYERPROPS_RACE
# The ??? means that I don't know what language it is.
# If multiple languages use the same set they should be comma separated
LOCALIZED_RACES = {

    # enUS
    'Terran': 'Terran',
    'Protoss': 'Protoss',
    'Zerg': 'Zerg',

    # ruRU
    'Терран': 'Terran',
    'Протосс': 'Protoss',
    'Зерг': 'Zerg',

    # koKR
    '테란': 'Terran',
    '프로토스': 'Protoss',
    '저그': 'Zerg',

    # ??eu
    'Terranie': 'Terran',
    'Protosi': 'Protoss',
    'Zergi': 'Zerg',

    # zhCH
    '人类': 'Terran',
    '星灵': 'Protoss',
    '异虫': 'Zerg',

    # zhTW
    '人類': 'Terran',
    '神族': 'Protoss',
    '蟲族': 'Zerg',

    # ???
    'Terrano': 'Terran',

    # deDE
    'Terraner': 'Terran',

    # esES - Spanish
    # esMX - Latin American
    # frFR - French - France
    # plPL - Polish Polish
    # ptBR - Brazilian Portuguese
}

MESSAGE_CODES = {
    '0': 'All',
    '2': 'Allies',
    '128': 'Header',
    '125': 'Ping',
}



GAME_SPEED_FACTOR = {
    'Slower':   0.6,
    'Slow':     0.8,
    'Normal':   1.0,
    'Fast':     1.2,
    'Faster':   1.4
}

GATEWAY_CODES = {
    'US': 'Americas',
    'KR': 'Asia',
    'EU': 'Europe',
    'SG': 'South East Asia',
    'XX': 'Public Test',
}

COLOR_CODES = {
    'B4141E': 'Red',
    '0042FF': 'Blue',
    '1CA7EA': 'Teal',
    'EBE129': 'Yellow',
    '540081': 'Purple',
    'FE8A0E': 'Orange',
    '168000': 'Green',
    'CCA6FC': 'Light Pink',
    '1F01C9': 'Violet',
    '525494': 'Light Grey',
    '106246': 'Dark Green',
    '4E2A04': 'Brown',
    '96FF91': 'Light Green',
    '232323': 'Dark Grey',
    'E55BB0': 'Pink'
}

COLOR_CODES_INV = dict(zip(COLOR_CODES.values(),COLOR_CODES.keys()))

REGIONS = {
    # United States
    'us': {
        1: 'us',
        2: 'la',
    },

    # Europe
    'eu': {
        1: 'eu',
        2: 'ru',
    },

    # Korea - appear to both map to same place
    'kr': {
        1: 'kr',
        2: 'tw',
    },
    # Taiwan - appear to both map to same place
    'tw': {
        1: 'kr',
        2: 'tw',
    },

    # China - different url scheme (www.battlenet.com.cn)?
    'cn': {
        1: 'cn',
    },

    # South East Asia
    'sea': {
        1: 'sea',
    },

    # Singapore
    'sg': {
        1: 'sg',
    },

    # Public Test
    'xx': {
        1: 'xx',
    },
}

""" Still unknown
    bbe: 3, 5, 7, 10, 15, 20, 25, 30
"""
LOBBY_PROPERTIES = {
    # Default seems to be the only value possible.
    # This arcade entry is just a hunch, need to confirm with an arcade game
    0x03E8: ("???", {
                'Dflt': 'Default'
            }),
    0x03E9: ("Arcade", {
                'no':'no',
                'yes':'yes'
            }),

    0x01F4: ("Controller",  {
                'Humn': 'Human',
                'Comp': 'Computer',
                'Open': 'Open',
                'Clsd': 'Closed',
            }),

    0x07D1: ("Game Mode", {
                '1v1': '1v1',
                '2v2': '2v2',
                '3v3': '3v3',
                '4v4': '4v4',
                '5v5': '5v5',
                '6v6': '6v6',
                'FFA': 'FFA',
            }),

    0x07D0: ("Team Count", lambda value: value), #T1,2,3,4,5,6, or Custom
    0x07D2: ("Teams1v1", lambda value: int(value[1:])),
    0x07D3: ("Teams2v2", lambda value: int(value[1:])),
    0x07D4: ("Teams3v3", lambda value: int(value[1:])),
    0x07D5: ("Teams4v4", lambda value: int(value[1:])),
    0x07D6: ("TeamsFFA", lambda value: int(value[1:])),
    0x07D7: ("Teams5v5", lambda value: int(value[1:])),
    0x07D8: ("Teams6v6", lambda value: int(value[1:])),

    0x07DB: ("2 Teams", lambda value: int(value[1:])),
    0x07DC: ("3 Teams", lambda value: int(value[1:])),
    0x07DD: ("4 Teams", lambda value: int(value[1:])),
    0x07DE: ("5 Teams", lambda value: int(value[1:])),

    0x07E1: ("FFA Teams", lambda value: int(value[1:])),
    0x07E2: ("Custom Teams", lambda value: int(value[1:])),

    0x0FA0: ("Game Privacy", {
                'Norm': 'Normal',
                'NoBO': 'No Build Order',
                'NoMH': 'No Match History',
            }),

    0x0BB8: ("Game Speed", {
                'Slor': 'Slower',
                'Slow': 'Slow',
                'Norm': 'Normal',
                'Fast': 'Fast',
                'Fasr': 'Faster',
            }),
    0x0BB9: ("Race", {
                'Terr': 'Terran',
                'Zerg': 'Zerg',
                'Prot': 'Protoss',
                'RAND': 'Random',
            }),
    0x0BBA: ("Color", {
                'tc01': "Red",
                'tc02': "Blue",
                'tc03': "Teal",
                'tc04': "Purple",
                'tc05': "Yellow",
                'tc06': "Orange",
                'tc07': "Green",
                'tc08': "Light Pink",
                'tc09': "Violet",
                'tc10': "Light Grey",
                'tc11': "Dark Green",
                'tc12': "Brown",
                'tc13': "Light Green",
                'tc14': "Dark Grey",
                'tc15': "Pink",
                'tc16': "??",
            }),
    0x0BBB: ("Handicap", {
                '50': '50',
                '60': '60',
                '70': '70',
                '80': '80',
                '90': '90',
                '100': '100',
            }),
    0x0BBC: ("Difficulty", {
                'VyEy': 'Very easy',
                'Easy': 'Easy',
                'Medi': 'Medium',
                'MdHd': 'Hard',
                'Hard': 'Harder',
                'HdVH': 'Very Hard',
                'VyHd': 'Elite',
                'ChVi': 'Cheater 1 (Vision)',
                'ChRe': 'Cheater 2 (Resources)',
                'Insa': 'Cheater 3 (Insane)',
            }),


    0x0BBF: ("Participant Role", {
                'Part':'Participant',
                'Watc':'Observer'
            }),

    0x0BC0: ("Watcher Type", {
                'Obs': 'Observer',
                'Ref':'Referee'
            }),
    0x0BC1: ("Category", {
                'Priv': 'Private',
                'Pub':  'Public',
                'Amm':  'Ladder',
                '':     'Single',
            }),
    0x0BC2: ("Locked Alliances", {
                'no':'unlocked',
                'yes':'locked',
            })
}
