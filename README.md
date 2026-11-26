# art-of-game-design-review

基于 Jesse Schell《游戏设计艺术（第 3 版）》（*The Art of Game Design: A Book of Lenses, 3rd Edition*, 2019）全书 **35 章核心设计原则** 与 **116 张官方透镜** 的游戏设计审视 Agent Skill。

帮助开发者在制作游戏的过程中，结合真实工程代码、配置表与设计文档，对当前游戏进行设计体检、研发阶段门禁审查或症状排雷，输出证据分级的 Top 3 致命风险排序与最小可证伪改进方案。

## 安装

```bash
npx -y skills add badDevBuild/art-of-game-design-review -g --all
```

## 适用条件与边界

- **适用场景**：审视当前正在开发的游戏项目、立项前验证、核心循环不好玩排查、数值失衡/经济崩溃检查、UI/HUD 困惑排查、兴趣曲线节奏诊断、谜题卡关分析、多人社群治理与试玩测试复盘。
- **支持 4 种审视模式**：
  1. **工程实景体检**：先读取工作区代码与设计文档还原现状，再抽镜核查。
  2. **阶段门禁审视**：覆盖 `concept`、`prototype`、`mechanics-balance`、`ux-pacing`、`narrative-world`、`social-live`、`playtest-ship` 七大研发阶段。
  3. **症状急诊**：覆盖 `not-fun`、`unclear-core`、`confusing-ux`、`broken-balance`、`flat-pacing`、`puzzle-stuck`、`weak-story`、`scope-creep`、`social-toxic`、`cheating`、`vr-discomfort`、`monetization-risk`、`team-alignment` 共 13 类症状。
  4. **全量 116 透镜深度审视**：按 8 大审视域逐域检查（包含 `#1`–`#112`、`#67½` 隐喻、`#93½` 临场感、`#95½` 可作弊性与 `#∞` 秘密目标）。
- **明确边界**：不用于纯引擎底层渲染/帧率性能优化、常规程序 Bug 修复或非游戏类产品运营；默认只做设计审视与提案，不擅自修改游戏代码。

## 使用示例

安装后，可以在对话中这样触发：

> 请使用 $art-of-game-design-review 结合当前游戏项目或设计方案，做一次游戏设计体检并给出 Top 3 风险与可落地改进建议。

也可以直接运行内置的确定性选镜脚本：

```bash
python3 skills/art-of-game-design-review/scripts/select_lenses.py --list-filters
python3 skills/art-of-game-design-review/scripts/select_lenses.py --stage prototype --tags puzzle,economy
python3 skills/art-of-game-design-review/scripts/select_lenses.py --symptom not-fun
python3 skills/art-of-game-design-review/scripts/select_lenses.py --ids 1,9,67.5,93.5,95.5,113 --format markdown
```

## 运行依赖

- 支持 Agent Skills 规范的客户端（如 Antigravity、Codex、Claude Code 等）
- Python 3（仅依赖标准库，无需安装任何第三方依赖包）

## 理论来源与致谢

- 理论框架、35 章结构与 116 张透镜题目来源：Jesse Schell, *The Art of Game Design: A Book of Lenses (3rd Edition)* (A K Peters / CRC Press, 2019) 与 Schell Games *Deck of Lenses*。
- 本仓库仅包含运行该 Skill 所需的指令、结构化参考数据与选镜脚本，不包含本地测试记录或私密项目材料。
