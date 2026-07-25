"""
政府版親屬關係固定位置設定
"""

RELATION_LAYOUT = {

    # ===== 本人 =====
    "SELF": {
        "generation": 0,
        "order": 0,
    },

    # ===== 配偶 =====
    "SPOUSE": {
        "generation": 0,
        "order": 1,
    },

    # ===== 父母 =====
    "FATHER": {
        "generation": -1,
        "order": 0,
    },

    "MOTHER": {
        "generation": -1,
        "order": 1,
    },

    # ===== 父系祖父母 =====
    "PATERNAL_GRANDFATHER": {
        "generation": -2,
        "order": 0,
    },

    "PATERNAL_GRANDMOTHER": {
        "generation": -2,
        "order": 1,
    },

    # ===== 母系祖父母 =====
    "MATERNAL_GRANDFATHER": {
        "generation": -2,
        "order": 2,
    },

    "MATERNAL_GRANDMOTHER": {
        "generation": -2,
        "order": 3,
    },

    # ===== 父系旁系 =====
    "PATERNAL_ELDER_UNCLE": {
        "generation": -1,
        "order": -2,
    },

    "PATERNAL_YOUNGER_UNCLE": {
        "generation": -1,
        "order": -1,
    },

    "PATERNAL_AUNT": {
        "generation": -1,
        "order": 2,
    },

    # ===== 母系旁系 =====
    "MATERNAL_UNCLE": {
        "generation": -1,
        "order": 3,
    },

    "MATERNAL_AUNT": {
        "generation": -1,
        "order": 4,
    },

    # ===== 兄弟姐妹 =====
    "ELDER_BROTHER": {
        "generation": 0,
        "order": -2,
    },

    "ELDER_SISTER": {
        "generation": 0,
        "order": -1,
    },

    "YOUNGER_BROTHER": {
        "generation": 0,
        "order": 2,
    },

    "YOUNGER_SISTER": {
        "generation": 0,
        "order": 3,
    },

    # ===== 子女 =====
    "SON": {
        "generation": 1,
        "order": 0,
    },

    "DAUGHTER": {
        "generation": 1,
        "order": 1,
    },
}