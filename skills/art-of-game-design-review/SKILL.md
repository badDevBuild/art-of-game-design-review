---
name: art-of-game-design-review
description: >
  基于 Jesse Schell《游戏设计艺术（第 3 版）》全书 35 章核心原则与 116 张官方透镜，对正在开发的游戏进行设计体检、阶段门禁审查或症状排雷，输出证据分级的风险排序与可证伪改进方案。当用户要求审视当前游戏、排查不好玩/数值失衡/界面困惑/节奏平淡/叙事割裂/社群问题或立项试玩自查时使用；不用于纯引擎渲染/性能优化、底层 Bug 修复或非游戏产品运营。
---

# 游戏设计艺术审视（The Art of Game Design Review）

用 Jesse Schell *The Art of Game Design: A Book of Lenses (3rd Edition)* 的 **35 章核心原则** 与 **116 张官方透镜**（含 `#67½` 隐喻、`#93½` 临场感、`#95½` 可作弊性与 `#∞` 秘密目标），对当前正在制作的游戏进行结构化、证据导向的设计审视。

## 核心原则与不变量

1. **先读真实工程与文档，禁止脱离事实空谈**：如果当前工作区存在游戏代码、配置表、关卡数据或设计文档，先读取并还原真实循环、规则、数值与界面现状，再开始审视；能从文件读出的信息，不反问用户。
2. **严格区分三类陈述**：所有结论必须拆分为「已核实事实（代码/规则/试玩原话）」「设计结构推断」「待真实试玩验证的体验假设」。禁止把模型脑补体验包装成既定事实。
3. **体验与安全优先的冲突裁决序**：出现取舍冲突时，按以下顺序裁决：
   `安全/合规/未成年人保护` ＞ `真实游玩场景下的本质体验` ＞ `可观察的玩家行为证据` ＞ `四元素与统一主题` ＞ `研发与商业可行性` ＞ `设计师个人偏好`。
4. **审视默认只读**：输出审视报告、风险排序与最小可证伪改动方案；除非用户明确授权修改，否则不直接改动游戏工程代码。

## 四模式路由

根据用户意图与当前项目形态选择一种模式：

| 模式 | 触发场景 | 选镜与阅读方式 |
| --- | --- | --- |
| **A. 工程实景体检（默认）** | 用户说“审视我当前做的游戏 / 帮我看看这个项目”且工作区有代码或 GDD | 先读工程现状；用 `--stage` + `--tags` 抽镜，并按需读 [checklist-principles.md](references/checklist-principles.md) 对应模块 |
| **B. 阶段门禁审视** | 用户处于特定研发阶段（立项、原型、数值平衡、UX 节奏、叙事世界、社交商业、试玩交付） | 运行 `scripts/select_lenses.py --stage <阶段> [--tags <标签>]` 抽取该阶段必检透镜 |
| **C. 症状急诊** | 用户带着明确痛点来查（如“不好玩”“数值崩了”“新手看不懂”“总卡关”） | 运行 `scripts/select_lenses.py --symptom <症状>`（6–15 张高命中透镜直击根因） |
| **D. 全量 116 透镜深度审视** | 用户明确要求“按全书 116 透镜/完整清单逐项过一遍” | 读取 [checklist-lenses.md](references/checklist-lenses.md) 与 [checklist-principles.md](references/checklist-principles.md)，按 8 大审视域逐域输出完整评估 |

> 运行 `python3 scripts/select_lenses.py --list-filters` 可查看全部合法的 `--stage`、`--symptom`、`--domain`、`--tags` 与 `--suit` 取值。

## 标准执行流程（5 步）

### 第 1 步：盘点项目现状与最小缺口提问
- 若工作区有项目文件：提取核心循环、操作输入、胜利/失败条件、数值经济、界面反馈、目标平台与游玩场景（Venue）。
- 若信息缺失且会直接改变审视结论（例如不知道目标受众、游玩设备或当前卡住的具体环节），**一次最多只问 1–3 个关键问题**；若已有足够材料或用户希望直接给假设，先标明假设并继续推进。

### 第 2 步：确定性抽镜与原则对照
使用脚本抽取本次审视所需的透镜清单，禁止凭记忆漏选关键透镜：

```bash
# 示例 1：原型期 + 经济/解谜标签
python3 scripts/select_lenses.py --stage prototype --tags puzzle,economy

# 示例 2：症状急诊（机制都能跑但不好玩）
python3 scripts/select_lenses.py --symptom not-fun

# 示例 3：精准调取特定透镜（支持 67½ / 93½ / 95½ / ∞）
python3 scripts/select_lenses.py --ids 1,2,9,15,67.5,93.5,95.5,113 --format markdown
```

同时根据命中领域，按需读取 [checklist-principles.md](references/checklist-principles.md) 中对应的非透镜核心法则（如元素四分法、八大过滤器、7 大机制、12 种平衡、谜题 10 原则、信息通道 4 步法、间接控制 6 手段、临场感 6 破/6 建、试玩 6 问与 FFWWDD）。

### 第 3 步：逐项对抗式审视
- 用「本质体验句」与「元素四分法（机制/故事/美学/技术）」检验是否存在表里割裂或伪装成体验的功能堆砌。
- 对抽中的每张透镜给出明确状态：`PASS`（已满足，附证据）、`WARN`（有隐患/待验证）、`FAIL`（存在明确设计冲突或缺失）、`N/A`（明确不适用并说明理由）。

### 第 4 步：提炼 Top 3 致命风险
按 **`致命度 (1–5) × 未知度 (1–5) ÷ 验证成本 (1–5)`** 排序，选出最值得立刻处理的前 3 项风险，拒绝平铺直叙罗列 20 条同等权重的意见。

### 第 5 步：交付审视报告与最小可证伪行动
严格按 [audit-routing-and-template.md](references/audit-routing-and-template.md) 的报告模板输出：
- 给出总体裁决与本质体验句；
- 列出 Top 3 风险与逐透镜检查明细；
- 明确分离「已核实事实 / 结构推断 / 待试玩假设」；
- 给出 1–3 个**成本最低、可直接动手或组织 3–5 人试玩验证**的改动与失败止损线。

## 资源与脚本索引

- **透镜筛选脚本**：[scripts/select_lenses.py](scripts/select_lenses.py)
- **116 透镜完整数据库**：[references/lenses-full.json](references/lenses-full.json)
- **116 透镜完整检查清单**：[references/checklist-lenses.md](references/checklist-lenses.md)
- **非透镜全书核心原则清单（Ch01–35）**：[references/checklist-principles.md](references/checklist-principles.md)
- **阶段/症状路由与报告模板**：[references/audit-routing-and-template.md](references/audit-routing-and-template.md)

## 停止与边界条件

- 信息不足且用户未授权基于假设继续时，提出最多 3 个关键问题后停止等待。
- 当发现核心体验或本质玩法尚未成立时，明确建议暂停堆砌美术/剧情/外围系统，先做可丢弃最小原型（Build the Toy First）后再复审。
- 涉及真实玩家心理/留存/付费合规/未成年人保护等结论时，不得把 AI 推理当成真实试玩或合规审查的替代品。
