[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

# Language Learning Coach

一个自适应 Codex Skill，把语言学习变成可持续推进的训练：可靠输入、实用语块、主动生成、真实互动、聚焦反馈和延迟复测。

它会根据目标语言、变体、学习目标和学习者的实际表现改变课程。范围聚焦资料充足的现代有声和书面语言，例如英语、法语、德语、意大利语、西班牙语、葡萄牙语、韩语、日语和阿拉伯语；不宣称支持手语、古典语、构造语或资料稀缺语言。

> [!IMPORTANT]
> 这是一个受 Kazuma 公开分享的学习实践启发的独立开源项目，并非 Kazuma 官方、授权、合作或代言项目。

## 它有什么不同

许多 AI 语言练习只是一次性的聊天。Language Learning Coach 被设计成一门可持续课程：

- **先完成真实任务，再谈抽象进度：** 把目标改写成“完成点单”或“回答三个追问”等可观察动作。
- **学习实用语块，并迁移使用：** 保存完整表达的情境、回应方式和可替换槽位，而不是死背固定台词。
- **先练后讲：** 先接触输入并互动，再从刚刚使用的例子中解释一个高价值语法模式。
- **用表现证据代替打卡：** 掌握取决于无提示提取、迁移、互动和延迟表现，而不是学习时长或翻卡数量。
- **按能力分别记录证据：** 听懂一个表达，不会自动算作会说、会读、会写、能互动、发音正确或已经保持。
- **按语言特征适配：** 声调、文字系统、复杂词形、敬语、地区变体和双言现象都会改变课程设计。
- **在本地持续记录：** 用可读的 Markdown 保存学习档案、语块、表现证据和下一轮复测。

## 核心能力

- 首次建档只从一个问题开始：**“你要学习什么语言？”**
- 支持自适应日课、五分钟最低维护、深度学习和真实实战复盘。
- 有声语言先听后看；音源分为 `native_official`、`native_traceable` 和 `tts`，TTS 必须明确标注且不能证明已接受母语发音训练。
- 训练实用语法、主动词汇、对话、阅读、写作及考试目标。
- 通过延迟提取和迁移检查，从 `new` 到 `retained` 使用六级表现证据。
- 按真实目标追踪 Kazuma 风格起步功能，并为每项保存学习者版本、替换槽位、常见追问和沟通修复表达。
- 建立习惯触发点、五分钟备用任务、独白、短日记和兴趣输入，并区分 AI 模拟互动与真实世界使用。
- 默认一门语言主攻，其他语言进入维护轮换。
- 可按需导出 Anki；卡片以“情境 → 完整表达”为主，而不是孤立词义配对。
- 核实发音、变体、语域、含义和文化用法的来源，不把不确定内容当成答案。

## 使用条件与安装

你需要支持本地 Skill 的 Codex，并安装 Python 3 以验证音频和学习工作区。音频验证器只接受传统未压缩 RIFF PCM WAV，其他音频格式需先转换；使用 clone 方式还需要 Git。

### 使用 Codex 内置 Skill 安装器

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo ai-martin-lau/language-learning-coach \
  --path . \
  --name language-learning-coach
```

### 使用 Git 安装

```bash
git clone https://github.com/ai-martin-lau/language-learning-coach.git \
  ~/.codex/skills/language-learning-coach
```

也可以下载仓库，然后把仓库内容复制到：

```text
~/.codex/skills/language-learning-coach
```

安装后新建一个 Codex 任务，让 Codex 发现这个 Skill。

## 快速开始

直接调用 Skill：

```text
使用 $language-learning-coach 帮我学习一门语言。
```

如果你还没有说明语言，它的第一条回复只有：

```text
你要学习什么语言？
```

也可以直接给出具体目标：

```text
使用 $language-learning-coach。我从零开始学习日语，每天有 15 分钟，
目标是去日本旅行时完成基础交流。
```

```text
使用 $language-learning-coach。帮我练习用埃及阿拉伯语提出礼貌请求，
并区分当地口语与现代标准阿拉伯语。
```

```text
使用 $language-learning-coach。继续昨天的巴西葡萄牙语，今天只有五分钟。
```

教练只追问会改变下一课的信息，随后立刻开始一个小型真实任务，而不是返回长问卷或通用学习计划。

## 课程如何适配

| 语言或目标特征 | 适配方式 |
|---|---|
| 声调、音高重音、音长或重音对立 | 先做感知对比，再产出，并进入整句练习 |
| 新文字或复杂文字系统 | 声音与文字并行推进，为转写制定淡出计划 |
| 丰富屈折或黏着结构 | 在完整语块旁尽早拆解词干、词缀并做控制生成 |
| 语域、敬语、方言连续体或双言现象 | 为每个表达附上关系、地区和媒介 |
| 考试、阅读、写作、工作、旅行或传承目标 | 按真实目标改变技能比例和评估任务 |

以上示例不是固定名单：只要另一门现代有声或书面语言拥有可靠音频、词典、语法资料和用法证据，也在范围内。资料不足时，教练必须说明限制，而不是声称具备专门支持。

## 学习状态与隐私

当当前工作区可写时，教练可以维护：

```text
language-learning/<language-slug>/
├── profile.md
├── phrase-bank.md
├── function-map.md
└── progress.md
```

这些文件只保存课程需要的信息：目标与限制、习惯触发点、带情境的表达和音源类别、分能力证据、起步功能覆盖、纠正及复测安排。它们位于用户工作区，不会写入已安装的 Skill 目录。内置验证器只检查结构和内部一致性，不声称记录的学习结果一定真实。

本仓库不包含遥测、账号集成或后台服务。课程需要当前或可靠的语言材料时，Codex 及用户授权的工具仍可能访问外部来源；相应产品和工具的隐私规则仍然适用。

## 方法与研究证据

课程的运行闭环是：

```text
到期提取 → 分类可靠输入 → 情境语块 → 整句模仿
→ 生成与修复 → 互动 → 实用语法 → 主动使用 → 延迟提取
```

设计借鉴了 Kazuma 公开讨论的声音优先模仿、实用短语、主动词汇、实用语法、固定任务习惯及兴趣驱动输入。详见[方法总结及一手来源](references/kazuma-method.md)。

这些实践不会被包装成已经整体获得科学验证的体系。Skill 会用二语习得研究校正具体教学选择，包括发音教学、公式化语块、显性语法、互动与纠错、间隔和提取、意义导向输入及自我调节。详见[证据矩阵与硬性护栏](references/evidence-and-guardrails.md)。

教练**不会**承诺固定天数流利、母语口音、所有语言拥有相同资料质量，也不会仅凭打卡、学习时长、当天答对或 Anki 正确率判定掌握。

## 仓库结构

```text
.
├── SKILL.md                         # 主要行为与请求路由
├── agents/openai.yaml              # Codex 展示元数据
├── assets/learning-workspace/      # 持久化课程模板
├── references/
│   ├── kazuma-method.md             # 公开方法来源及边界
│   ├── evidence-and-guardrails.md   # 二语习得研究与科学边界
│   ├── language-adaptation.md       # 跨语言特征适配
│   └── session-protocols.md         # 课程、反馈、复测和状态协议
├── scripts/validate_audio.py        # 本地 PCM WAV 交付验证器
├── scripts/validate_workspace.py    # Markdown 学习状态验证器
├── tests/test_validate_audio.py     # 音频验证器回归测试
├── tests/test_validate_workspace.py # 工作区验证器回归测试
└── docs/plans/                      # 设计记录
```

## 参与贡献

欢迎提交 Issue 和 Pull Request，尤其欢迎：

- 由一手来源或社群认可资料支持的修正；
- 对主流语言变体或学习目标提供更好的适配；
- 更清晰的安全、文化、无障碍和研究证据边界；
- 对五种 README 翻译进行自然、准确的改进。

英文 `README.md` 是内容基准。修改文档时，请在同一 Pull Request 中同步所有受影响的翻译。不要加入无依据的流利承诺、虚构的母语者共识或 Kazuma 合作声明。

## 开源许可证

本项目采用 [MIT License](LICENSE)。
