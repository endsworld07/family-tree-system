# Government Family Relationship System (GFRS)

Version：1.0

---

# 一、專案目標

本系統用於建立固定格式之政府版親屬關係圖。

本系統依據使用者輸入的人物及父母關係，
自動產生親屬關係圖。

本系統以簡單、穩定、容易維護為最高原則。

---

# 二、設計原則

## 2.1 Keep It Simple

永遠優先選擇最簡單的實作方式。

不要為了未來可能發生的需求，
增加目前不需要的複雜功能。

---

## 2.2 關係決定排版

所有排版只依據：

- 父
- 母

建立。

不依據：

- 稱謂
- 世代
- 親等

---

## 2.3 稱謂只負責顯示

label 為使用者自行輸入。

例如：

- 申請人
- 父
- 母
- 祖父
- 曾祖父
- 先考
- 顯妣

系統不做任何推論。

---

## 2.4 一個檔案只做一件事

每個 Python 檔案只負責自己的工作。

不得跨模組處理其它工作。

---

# 三、資料模型

每位人物(Person)包含：

- id
- name
- label
- father
- mother
- spouses

---

# 四、輸入規則

第一筆資料固定為：

申請人：

父：

母：

其它人物：

姓名：

父：

母：

配偶：

可輸入多位。

---

# 五、排版規則

## 主幹

永遠上下排列。

父在上。

母在下。

一直向上延伸。

一直向下延伸。

---

## 旁系

同父同母人物排列於主幹左右。

左右順序依照輸入順序。

不得自行重新排序。

---

## 配偶

配偶固定顯示於人物下方。

可有多位配偶。

依輸入順序排列。

---

## 子女

子女依父母關係建立。

顯示於父母下方。

---

# 六、人物判斷規則

若：

father 相同

且

mother 相同

則判定為兄弟姐妹。

除此之外，

系統不做任何其它親屬推論。

---

# 七、Version 1 不包含功能

本版本不實作：

- 伯叔判斷
- 姑姨判斷
- 堂表判斷
- 親等推論
- 世代推論
- 養子
- 過房
- 收養
- 特殊戶籍案例
- OCR
- AI辨識

以上功能留待未來版本討論。

---

# 八、專案結構

app.py

models.py

family.json

data_loader.py

relationship_engine.py

layout_engine.py

connection_engine.py

svg_renderer.py

templates/

static/

README.md

SPEC.md

---

# 九、開發流程

依照以下順序完成：

1. models.py
2. family.json
3. data_loader.py
4. relationship_engine.py
5. layout_engine.py
6. connection_engine.py
7. svg_renderer.py
8. app.py
9. templates

不得跳步。

每完成一個模組即測試。

確認正常後再開始下一步。