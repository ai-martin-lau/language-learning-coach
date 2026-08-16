[English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md)

# Language Learning Coach｜主流小语种旅行 A2 教练

**为下一次旅行，在实际表现支持的范围内，沿最短实用路径建立可验证的 A2 基础。**

![从火车站、酒店到餐厅的旅行语言学习场景插画](assets/readme/travel-hero.webp)

Language Learning Coach 是一个自适应 Codex Skill，通过真实任务、可靠输入、实用语块、主动提取、互动、聚焦反馈和延迟复测来学习语言。

项目首先面向法语、德语、意大利语、西班牙语、葡萄牙语、韩语、日语、阿拉伯语等资料充足的主流小语种，也支持英语。目标语言、地区变体、文字系统、可用时间和你实际表现出来的能力，都会改变下一课。

> [!IMPORTANT]
> “旅行 A2”是本项目的训练路线，不是 CEFR 官方子等级或证书。A2 主要覆盖熟悉、常规场景中的简单直接信息交换；CEFR 把“能应对旅行中大多数可能出现的情况”放在 B1。因此本项目追求的是：**在常见、可预测的旅行任务中更从容**，而不是承诺所有旅行和突发情况都无压力。参见欧洲委员会的 [CEFR 全局等级表](https://www.coe.int/en/web/common-european-framework-reference-languages/table-1-cefr-3.3-common-reference-levels-global-scale)和[口语表现描述](https://www.coe.int/en/web/common-european-framework-reference-languages/table-3-cefr-3.3-common-reference-levels-qualitative-aspects-of-spoken-language-use)。

> [!NOTE]
> 这是一个受 Kazuma 公开分享的学习实践启发的独立开源项目，并非 Kazuma 官方、授权、合作或代言项目。

## 为旅行而学，不为打卡而学

![六类旅行训练场景：交通、住宿、餐饮、问路、购物和沟通修复](assets/readme/travel-scenarios.svg)

默认旅行路线集中训练六类结果：

- **交通：** 询问车票、站台、时间、路线和变更。
- **住宿：** 办理入住、核对信息并描述简单问题。
- **餐饮：** 点餐、表达偏好、听懂一个常见追问并付款。
- **问路：** 提问、识别地标并确认自己是否理解正确。
- **购物：** 处理价格、数量、尺寸、库存和支付。
- **沟通修复：** 请对方重复、放慢、写下来、指出来或换一种说法。

每个在学语块都会保存你的版本、可替换槽位、常见追问和修复表达。目标不是背下一本固定短语书，而是当地点、时间、数量或条件变化时，依然能完成任务。

严重医疗、法律、出入境和安全紧急情况，不会被包装成仅凭 A2 就能独立安全处理的场景。

## 一句话开始

```text
使用 $language-learning-coach。我从零开始学日语，每天有 15 分钟，
希望去日本旅行时能完成基础交流。
```

如果你还没有说明语言，第一条回复只会是：

```text
你要学习什么语言？
```

此后教练一次只问一个问题，而且只问会改变下一课的信息。你会立刻开始一个小型真实任务，而不是先收到长问卷或通用日历。

也可以这样开始：

```text
使用 $language-learning-coach。帮我练习用埃及阿拉伯语提出礼貌请求，
并区分当地口语与现代标准阿拉伯语。
```

```text
使用 $language-learning-coach。继续昨天的巴西葡萄牙语，
今天我只有五分钟。
```

## 最短实用路线必须自适应

![从真实旅行任务到可靠输入、主动提取、互动、反馈和延迟迁移的八步闭环](assets/readme/adaptive-loop.svg)

有听说目标时，一节典型的旅行课会经过：

1. 选择一个真实任务和目标变体；
2. 先听完整、已分类的示范，再看答案；
3. 理解沟通意图和一个关键信息；
4. 学习一至三个带可替换槽位的完整语块；
5. 随提示逐步撤去，主动提取并改变内容；
6. 完成一次带常见追问和修复选项的短互动；
7. 只修正一至两个最影响任务的问题，并马上重做；
8. 隔一段时间，更换地点、时间、人物、物品或条件后再做。

纯阅读或写作目标、无障碍需求、新文字系统、声调或音高重音、复杂词形、敬语、地区变体和双言现象都会改变顺序。旅行是项目的首要路线；只要有可靠资料，工作、考试、阅读、写作、影视和传承语目标仍然支持。

## 一节微课，四个看得见的动作

![四格课程：听完整示范、尝试任务、只修正一个关键问题、改变条件后重做](assets/readme/lesson-storyboard.svg)

1. **示范：** 从已分类的来源听完整表达；适合时再显示文字。
2. **尝试：** 在售票柜台、酒店前台、餐厅、商店或问路任务中使用。
3. **聚焦反馈：** 先保住交流，只纠正最影响任务完成的问题。
4. **重做：** 马上再完成一次，然后改变一个条件，让提取而不是照抄发挥作用。

AI 角色扮演是有用的模拟训练，但不能证明你已经处理过母语者、自然语速、环境噪音、新口音或不可预测的真实回应。

## 以 A2 为方向，按能力保存证据

![听力、口语产出、阅读、写作、互动和发音分别进入有支持、独立、变化迁移和延迟保持阶梯](assets/readme/evidence-ladder.svg)

听力、口语产出、阅读、写作、互动和发音分别记录。听懂一个表达，不会自动算作会说；朗读不等于能互动；同一课答对也不等于已经保持。

证据阶梯是：

```text
有支持 → 独立完成 → 改变条件 → 延迟保持
```

工作区会记录任务、提示级别、证据环境、结果、日期和下次复测。真人或现实任务可以增强证据，但项目不会颁发 A2 证书。进步速度取决于语言距离、起点、练习时间、资料质量，以及你的表现能否经得住迁移和延迟。

## 音源类别不会藏起来

有听说目标且音频可播放时，新语块会先听完整声音，再显示文字答案。每个示范都归入以下类别：

| 来源类别 | 含义 | 能支持什么 |
|---|---|---|
| `native_official` | 由目标变体母语者提供的官方或机构录音 | 对来源实际覆盖材料的强示范 |
| `native_traceable` | 说话者和出处可追溯，且变体、情境和语域合适 | 在来源记录范围内作为示范 |
| `tts` | 明确标注的合成语音后备 | 初步听辨和排练，不能证明母语示范或发音掌握 |
| `pending` | 尚未交付可靠示范 | 暂停听说或发音步骤，不临时编造 |

本地 WAV 交付前会验证文件结构。技术上能解码，不等于来源可靠、变体正确、已经实际播放或可以评估真实发音。

## 安装

你需要支持本地 Skill 的 Codex，以及用于音频和学习工作区验证的 Python 3。音频验证器只接受传统未压缩 RIFF PCM WAV，其他格式需先转换；使用 Git 安装还需要 Git。

### 使用 Codex 内置 Skill 安装器

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo ai-martin-lau/language-learning-coach \
  --path . \
  --name language-learning-coach
```

### 使用 Git

```bash
git clone https://github.com/ai-martin-lau/language-learning-coach.git \
  ~/.codex/skills/language-learning-coach
```

也可以下载仓库，然后把内容复制到：

```text
~/.codex/skills/language-learning-coach
```

安装后新建一个 Codex 任务，让 Codex 重新发现这个 Skill。

## 不同语言如何改变路线

| 语言或目标特征 | 适配方式 |
|---|---|
| 声调、音高重音、音长或重音对立 | 先做感知对比，再产出，并进入整句练习 |
| 新文字或复杂文字系统 | 声音与文字并行推进，并为转写设置淡出计划 |
| 丰富屈折或黏着结构 | 保留完整语块，同时尽早拆解词干、词缀并做控制生成 |
| 语域、敬语、方言连续体或双言现象 | 为每个表达附上关系、地区和媒介 |
| 阅读、写作、工作、考试、影视或传承语目标 | 按真实目标改变技能比例和证据任务 |

这些例子不是永久支持名单。另一门现代有声或书面语言只有在拥有可靠音频、词典、语法资料和用法证据时才进入范围。手语、古典语、构造语和资料稀缺语言需要本 Skill 当前范围之外的专门资料或教练。

## 本地学习状态与隐私

当当前工作区可写时，教练可以维护：

```text
language-learning/<language-slug>/
├── profile.md
├── phrase-bank.md
├── function-map.md
└── progress.md
```

这些可读的 Markdown 文件保存课程相关目标、限制、习惯触发点、情境语块、音源类别、分能力证据、起步功能覆盖、纠正和复测安排。它们位于用户工作区，而不是已安装的 Skill 目录。内置验证器只检查结构和内部一致性，不声称记录的学习结果一定真实。

本仓库不包含遥测、账号集成或后台服务。课程需要可靠语言材料时，Codex 和用户授权的工具仍可能访问外部来源；相应产品的隐私规则仍然适用。

## 方法与研究证据

设计借鉴了 Kazuma 公开讨论的声音优先模仿、实用短语、主动词汇、实用语法、固定任务习惯和兴趣驱动输入。详见[方法总结及一手来源](references/kazuma-method.md)。

这些实践不会被当作一个已经整体获得科学验证的体系。Skill 会用二语习得研究校正具体选择，包括发音教学、公式化语块、显性语法、互动与纠错、间隔和提取、意义导向输入及自我调节。详见[证据矩阵与硬性护栏](references/evidence-and-guardrails.md)。

本 README 的可视化导航方式参考了 [byoungd/up](https://github.com/byoungd/up) 的语言学习部分。仓库内文案和视觉资产均为原创，没有复用其照片或插画。

## 仓库结构

```text
.
├── SKILL.md                         # 主要行为与请求路由
├── agents/openai.yaml              # Codex 展示元数据
├── assets/
│   ├── learning-workspace/          # 持久化课程模板
│   └── readme/                      # 原创 README 视觉资产
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

欢迎提交 Issue 和 Pull Request，尤其欢迎有来源支持的修正、对主流语言变体和旅行任务更好的适配、更清晰的安全与证据边界，以及五种 README 的自然翻译改进。

英文 `README.md` 是内容基准。修改文档时，请在同一 Pull Request 中同步所有受影响的翻译。不要加入固定时间达 A2、无依据流利承诺、虚构母语者共识、伪造学习评价或 Kazuma 合作声明。

## 开源许可证

本项目采用 [MIT License](LICENSE)。
