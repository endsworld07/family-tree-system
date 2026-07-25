from models.layout_node import LayoutNode


class LayoutEngine:
    """
    Government Family Tree Layout V4

    Layout Rules
    ------------------------
    1. 申請人永遠位於主幹中央
    2. 主幹為固定座標
    3. 配偶永遠上下排列
    4. 不使用動態累加座標
    5. 所有座標由 Position Table 控制
    """

    # ==========================================================
    # Node Size
    # ==========================================================

    NODE_WIDTH = 120
    NODE_HEIGHT = 40

    # ==========================================================
    # Layout
    # ==========================================================

    CENTER_X = 700

    SPOUSE_GAP = 45
    GENERATION_GAP = 130

    SIDE_GAP = 260

    # ==========================================================
    # Main Line Position
    # ==========================================================

    MAIN_LINE = {

        # ---------- 九代祖 ----------

        "NOSE_ANCESTOR_FATHER": 60,
        "NOSE_ANCESTOR_MOTHER": 105,

        "DISTANT_ANCESTOR_FATHER": 190,
        "DISTANT_ANCESTOR_MOTHER": 235,

        "GREAT_ANCESTOR_FATHER": 320,
        "GREAT_ANCESTOR_MOTHER": 365,

        "FIERCE_ANCESTOR_FATHER": 450,
        "FIERCE_ANCESTOR_MOTHER": 495,

        "HEAVEN_ANCESTOR_FATHER": 580,
        "HEAVEN_ANCESTOR_MOTHER": 625,

        "HIGH_ANCESTOR_FATHER": 710,
        "HIGH_ANCESTOR_MOTHER": 755,

        "GREAT_GRANDFATHER": 840,
        "GREAT_GRANDMOTHER": 885,

        "GRANDFATHER": 970,
        "GRANDMOTHER": 1015,

        "FATHER": 1100,
        "MOTHER": 1145,

        # ---------- 主角 ----------

        "SELF": 1280,
    }

    # ==========================================================
    # Public
    # ==========================================================

    def layout(self, relationships):

        nodes = []

        # 目前 Part1
        # 只建立主幹
        # 伯叔父 / 姑姑 / 子女
        # 將於 Part2~Part4 完成

        self._build_main_line(nodes, relationships)

        return nodes

    # ==========================================================
    # Main Line
    # ==========================================================

    def _build_main_line(self, nodes, relationships):

        for title, y in self.MAIN_LINE.items():

            relation = self._find(relationships, title)

            if relation is None:
                continue

            nodes.append(
                self._create_node(
                    relation,
                    self.CENTER_X,
                    y
                )
            )

    # ==========================================================
    # Create Node
    # ==========================================================

    def _create_node(self, relationship, x, y):

        return LayoutNode(
            relationship=relationship,
            x=x,
            y=y
        )

    # ==========================================================
    # Helpers
    # ==========================================================

    def _find(self, relationships, title):

        for relationship in relationships:

            if relationship.title == title:
                return relationship

        return None

    # ==========================================================

    def _find_all(self, relationships, title):

        return [

            relationship

            for relationship in relationships

            if relationship.title == title

        ]