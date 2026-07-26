# ==========================================================
# KinshipTitleResolver.py
# Part 1
# ==========================================================

from __future__ import annotations

from models.relationship import Relationship


class KinshipTitleResolver:
    """
    親屬稱謂解析器

    功能：
        Relationship -> Title

    僅負責建立親屬稱謂。

    不負責：
        Relationship 建立
        Layout
        SVG
        FamilyGroup
    """

    def __init__(
        self,
        relationships: dict[str, Relationship],
        applicant: Relationship,
    ) -> None:

        # 全部人物
        self.relationships = relationships

        # 申請人
        self.applicant = applicant

    # ==========================================================
    # Public
    # ==========================================================

    def build(self) -> None:
        """
        建立所有親屬稱謂
        """

        self._build_direct_titles()

        self._build_collateral_titles()

        self._build_spouse_titles()

        self._build_sibling_titles()

    # ==========================================================
    # Helper
    # ==========================================================

    def _set_title(
        self,
        relationship: Relationship,
        title: str,
    ) -> None:
        """
        設定稱謂
        """

        relationship.title = title

    def _father(
        self,
        relationship: Relationship,
    ) -> Relationship | None:

        return relationship.father

    def _mother(
        self,
        relationship: Relationship,
    ) -> Relationship | None:

        return relationship.mother

    # ==========================================================
    # Part 2
    # Direct Titles
    # ==========================================================

    def _build_direct_titles(self) -> None:
        """
        建立直系親屬稱謂

        SELF
            ↓
        父母
            ↓
        祖父母
            ↓
        曾祖父母
            ↓
        高祖父母
            ↓
        天祖父母
            ↓
        太祖父母
            ↓
        烈祖父母...
        """

        # -------------------------
        # 自己
        # -------------------------

        self._set_title(
            self.applicant,
            "SELF",
        )

        # -------------------------
        # 父母
        # -------------------------

        father = self._father(self.applicant)
        mother = self._mother(self.applicant)

        if father:
            self._set_title(
                father,
                "FATHER",
            )

        if mother:
            self._set_title(
                mother,
                "MOTHER",
            )

        # -------------------------
        # 父系祖先
        # -------------------------

        ancestor = father
        level = 1

        while ancestor:

            father_node = self._father(ancestor)
            mother_node = self._mother(ancestor)

            if father_node:

                self._set_title(
                    father_node,
                    self._ancestor_father_title(level + 1),
                )

            if mother_node:

                self._set_title(
                    mother_node,
                    self._ancestor_mother_title(level + 1),
                )

            ancestor = father_node
            level += 1

    # ==========================================================

    def _ancestor_father_title(
        self,
        generation: int,
    ) -> str:

        mapping = {

            1: "FATHER",

            2: "GRANDFATHER",

            3: "GREAT_GRANDFATHER",

            4: "HIGH_GRANDFATHER",

            5: "HEAVEN_GRANDFATHER",

            6: "TAI_GRANDFATHER",

        }

        return mapping.get(
            generation,
            "LIE_GRANDFATHER",
        )

    # ==========================================================

    def _ancestor_mother_title(
        self,
        generation: int,
    ) -> str:

        mapping = {

            1: "MOTHER",

            2: "GRANDMOTHER",

            3: "GREAT_GRANDMOTHER",

            4: "HIGH_GRANDMOTHER",

            5: "HEAVEN_GRANDMOTHER",

            6: "TAI_GRANDMOTHER",

        }

        return mapping.get(
            generation,
            "LIE_GRANDMOTHER",
        )

# ==========================================================
# Part 3
# Collateral Titles
# ==========================================================

    def _build_collateral_titles(self) -> None:
        """
        建立父系旁系稱謂

        父
            ├── 伯父／叔父

        祖父
            ├── 伯叔祖父

        曾祖父
            ├── 曾伯叔祖父

        高祖父
            ├── 高伯叔祖父
        """

        ancestor = self._father(self.applicant)

        generation = 1

        while ancestor:

            for sibling in ancestor.siblings:

                self._set_title(
                    sibling,
                    self._collateral_father_title(
                        generation
                    ),
                )

            ancestor = self._father(ancestor)

            generation += 1

    # ==========================================================

    def _collateral_father_title(
        self,
        generation: int,
    ) -> str:

        mapping = {

            1: "UNCLE",

            2: "GRAND_UNCLE",

            3: "GREAT_GRAND_UNCLE",

            4: "HIGH_GRAND_UNCLE",

            5: "HEAVEN_GRAND_UNCLE",

            6: "TAI_GRAND_UNCLE",

        }

        return mapping.get(
            generation,
            "LIE_GRAND_UNCLE",
        )

    # ==========================================================
    # Part 4
    # Spouse Titles
    # ==========================================================

    def _build_spouse_titles(self) -> None:
        """
        建立配偶稱謂

        配偶稱謂由另一半(title)推導。

        例如：

            FATHER      -> MOTHER
            GRANDFATHER -> GRANDMOTHER
            UNCLE       -> AUNT
        """

        for relationship in self.relationships.values():

            if not relationship.title:
                continue

            spouse_title = self._spouse_title(
                relationship.title
            )

            if spouse_title is None:
                continue

            for spouse in relationship.spouses:

                # 已有稱謂就不覆蓋
                if spouse.title:
                    continue

                self._set_title(
                    spouse,
                    spouse_title,
                )

    # ==========================================================

    def _spouse_title(
        self,
        title: str,
    ) -> str | None:

        mapping = {

            # -------------------------
            # 直系
            # -------------------------

            "FATHER": "MOTHER",

            "GRANDFATHER": "GRANDMOTHER",

            "GREAT_GRANDFATHER": "GREAT_GRANDMOTHER",

            "HIGH_GRANDFATHER": "HIGH_GRANDMOTHER",

            "HEAVEN_GRANDFATHER": "HEAVEN_GRANDMOTHER",

            "TAI_GRANDFATHER": "TAI_GRANDMOTHER",

            "LIE_GRANDFATHER": "LIE_GRANDMOTHER",

            # -------------------------
            # 旁系
            # -------------------------

            "UNCLE": "AUNT",

            "GRAND_UNCLE": "GRAND_AUNT",

            "GREAT_GRAND_UNCLE": "GREAT_GRAND_AUNT",

            "HIGH_GRAND_UNCLE": "HIGH_GRAND_AUNT",

            "HEAVEN_GRAND_UNCLE": "HEAVEN_GRAND_AUNT",

            "TAI_GRAND_UNCLE": "TAI_GRAND_AUNT",

            "LIE_GRAND_UNCLE": "LIE_GRAND_AUNT",

            # -------------------------
            # 申請人
            # -------------------------

            "SELF": "SPOUSE",

        }

        return mapping.get(title)

    # ==========================================================
    # Part 5
    # Sibling Titles
    # ==========================================================

    def _build_sibling_titles(self) -> None:
        """
        建立兄弟姐妹稱謂

        目前依性別判斷：

            男 -> BROTHER
            女 -> SISTER

        若未來 Person 增加出生排序，
        再細分為：

            哥哥
            弟弟
            姐姐
            妹妹
        """

        for sibling in self.applicant.siblings:

            gender = sibling.person.gender

            if gender == "男":

                self._set_title(
                    sibling,
                    "BROTHER",
                )

            elif gender == "女":

                self._set_title(
                    sibling,
                    "SISTER",
                )
