# relationship.py
"""
Government Family Tree v2.0
--------------------------------
此檔案只定義親屬資料。

不要放：
- x/y 座標
- CSS Class
- HTML
- 線條資訊

所有版面配置皆由 family_tree.css 控制。
"""

RELATIONS = [

    # =========================
    # 第一代
    # =========================
    {
        "id": "great_grandfather",
        "title": "烈祖父",
        "group": "great_grandparents"
    },
    {
        "id": "great_grandmother",
        "title": "烈祖母",
        "group": "great_grandparents"
    },

    # =========================
    # 第二代
    # =========================
    {
        "id": "grandfather",
        "title": "祖父",
        "group": "grandparents"
    },
    {
        "id": "grandmother",
        "title": "祖母",
        "group": "grandparents"
    },

    {
        "id": "maternal_grandfather",
        "title": "外祖父",
        "group": "grandparents"
    },
    {
        "id": "maternal_grandmother",
        "title": "外祖母",
        "group": "grandparents"
    },

    # =========================
    # 第三代
    # =========================
    {
        "id": "father",
        "title": "父親",
        "group": "parents"
    },
    {
        "id": "mother",
        "title": "母親",
        "group": "parents"
    },

    {
        "id": "father_in_law",
        "title": "岳父",
        "group": "parents"
    },
    {
        "id": "mother_in_law",
        "title": "岳母",
        "group": "parents"
    },

    # =========================
    # 本人
    # =========================
    {
        "id": "self",
        "title": "本人",
        "group": "self"
    },
    {
        "id": "spouse",
        "title": "配偶",
        "group": "self"
    },

    # =========================
    # 子女
    # =========================
    {
        "id": "son1",
        "title": "長子",
        "group": "children"
    },
    {
        "id": "son2",
        "title": "次子",
        "group": "children"
    },
    {
        "id": "son3",
        "title": "三子",
        "group": "children"
    },
    {
        "id": "son4",
        "title": "四子",
        "group": "children"
    },

    {
        "id": "daughter1",
        "title": "長女",
        "group": "children"
    },
    {
        "id": "daughter2",
        "title": "次女",
        "group": "children"
    },
    {
        "id": "daughter3",
        "title": "三女",
        "group": "children"
    },
    {
        "id": "daughter4",
        "title": "四女",
        "group": "children"
    },

    # =========================
    # 孫輩
    # =========================
    {
        "id": "grandson1",
        "title": "長孫",
        "group": "grandchildren"
    },
    {
        "id": "grandson2",
        "title": "次孫",
        "group": "grandchildren"
    },
    {
        "id": "grandson3",
        "title": "三孫",
        "group": "grandchildren"
    },
    {
        "id": "grandson4",
        "title": "四孫",
        "group": "grandchildren"
    },

    {
        "id": "granddaughter1",
        "title": "長孫女",
        "group": "grandchildren"
    },
    {
        "id": "granddaughter2",
        "title": "次孫女",
        "group": "grandchildren"
    },
    {
        "id": "granddaughter3",
        "title": "三孫女",
        "group": "grandchildren"
    },
    {
        "id": "granddaughter4",
        "title": "四孫女",
        "group": "grandchildren"
    },
]