# 宠物等级图片生成操作指南

> 目标：为班级宠物园系统中的所有宠物品种生成8个等级的图片
> 技术：SiliconFlow FLUX.1-dev
> 核心：每个品种独立设计装饰，严格统一画风

---

## 一、设计理念

### 核心原则
- **一品种一设计**：每个犬种/猫种独立设计装饰，符合品种特性
- **严格画风统一**：所有图片使用完全相同的风格描述词
- **装饰升级体现成长**：从简单到华丽，体现等级提升

### 画风规范（严格统一，不可更改）
```
STYLE = "flat cartoon illustration, kawaii chibi style, consistent character design,
cute friendly expression, big round sparkling eyes with white highlights,
soft rounded shapes, smooth clean outlines, no sharp edges,
bright saturated warm colors, soft shading, 2D vector art style,
children book illustration style, standing pose, front facing,
white background, masterpiece, best quality"

NEGATIVE = "3D, realistic, photograph, scary, dark, complex background,
busy background, text, watermark, signature, blurry, low quality,
different style, inconsistent design"
```

---

## 二、系统宠物品种清单

### 犬类（15种）

| ID | 名称 | 品种特征 | 装饰设计状态 |
|----|------|---------|-------------|
| west-highland | 西高地 | 白色梗犬，立耳 | ⏳ 待设计 |
| bichon | 比熊 | 白色卷毛，圆脸 | ⏳ 待设计 |
| border-collie | 边牧 | 黑白/三色，聪明 | ⏳ 待设计 |
| shiba | 柴犬 | 日本柴犬，卷尾 | ⏳ 待设计 |
| golden-retriever | 金毛 | 金色长毛，温顺 | ⏳ 待设计 |
| samoyed | 萨摩耶 | 白色长毛，微笑 | ⏳ 待设计 |
| corgi | 柯基 | 短腿，大耳朵 | ⏳ 待设计 |
| pomeranian | 博美 | 小型，蓬松 | ⏳ 待设计 |
| poodle | 贵宾 | 卷毛，优雅 | ⏳ 待设计 |
| dachshund | 腊肠 | 长身，短腿 | ⏳ 待设计 |
| beagle | 比格 | 三色，大耳朵 | ⏳ 待设计 |
| husky | 哈士奇 | 蓝眼，狼-like | ⏳ 待设计 |
| alaska | 阿拉斯加 | 大型，长毛 | ⏳ 待设计 |
| chihuahua | 吉娃娃 | 小型，大耳 | ⏳ 待设计 |
| french-bulldog | 法斗 | 短毛，蝙蝠耳 | ⏳ 待设计 |

### 猫类（3种）

| ID | 名称 | 品种特征 | 装饰设计状态 |
|----|------|---------|-------------|
| short-leg-cat | 矮脚猫 | 短腿，可爱 | ⏳ 待设计 |
| ragdoll | 布偶 | 蓝眼，长毛 | ⏳ 待设计 |
| golden-gradient | 金渐层 | 金色渐变毛 | ⏳ 待设计 |

### 神兽（7种）

| ID | 名称 | 特征 | 装饰设计状态 |
|----|------|------|-------------|
| dragon | 小龙 | 龙形，翅膀 | ⏳ 待设计 |
| phoenix | 凤凰 | 火鸟，羽毛 | ⏳ 待设计 |
| unicorn | 独角兽 | 独角，马身 | ⏳ 待设计 |
| kirin | 麒麟 | 鹿角，鳞身 | ⏳ 待设计 |
| pegasus | 飞马 | 马+翅膀 | ⏳ 待设计 |
| nine-tailed-fox | 九尾狐 | 九尾，狐形 | ⏳ 待设计 |
| qilin | 青龙 | 龙形，青色 | ⏳ 待设计 |

---

## 三、品种装饰设计

### 设计原则
1. **符合品种特性**：柯基用皇室元素（英国女王），柴犬用日本元素
2. **等级递进清晰**：Lv.1简单 → Lv.8华丽神圣
3. **装饰可见性**：一眼可见，不模糊
4. **风格统一性**：所有品种使用相同画风描述

### 示例：柯基装饰设计

| 等级 | 装饰 | 具体元素 | 设计理念 |
|------|------|---------|---------|
| Lv.1 | 小红领结 | 红色蝴蝶结 | 简单可爱 |
| Lv.2 | 英国国旗项圈 | 米字旗元素 | 英国品种 |
| Lv.3 | 皇冠+短腿印记 | 小皇冠 | 皇室关联 |
| Lv.4 | 华丽项圈+宝石 | 金色+宝石 | 贵族气质 |
| Lv.5 | 小王冠+披风 | 皇冠+小披风 | 小国王 |
| Lv.6 | 皇冠+翅膀+光环 | 天使柯基 | 飞翔梦想 |
| Lv.7 | 大翅膀+皇家光环 | 皇家天使 | 高贵守护 |
| Lv.8 | 神圣皇冠+大翅膀+漂浮+英国符号 | 神圣皇家 | 完全神圣化 |

### 示例：柴犬装饰设计

| 等级 | 装饰 | 具体元素 | 设计理念 |
|------|------|---------|---------|
| Lv.1 | 日式小铃铛 | 红色铃铛 | 日本元素 |
| Lv.2 | 樱花项圈 | 樱花装饰 | 日本国花 |
| Lv.3 | 武士小头盔 | 日式头盔 | 武士文化 |
| Lv.4 | 金色和服腰带 | 和服元素 | 传统服饰 |
| Lv.5 | 日式皇冠+家纹 | 皇冠+家纹 | 贵族气质 |
| Lv.6 | 天狗翅膀+面具 | 天狗元素 | 日本神话 |
| Lv.7 | 大天狗翅膀+光环 | 大天狗 | 强大守护 |
| Lv.8 | 神圣天狗+大翅膀+漂浮+樱花符号 | 神圣天狗 | 完全神圣化 |

### 待设计品种

按优先级设计：
1. **bichon** - 比熊（白色卷毛，适合可爱装饰）
2. **golden-retriever** - 金毛（温顺，适合温暖装饰）
3. **corgi** - 柯基（短腿，皇室关联）
4. **shiba** - 柴犬（日本元素）
5. **husky** - 哈士奇（蓝眼，狼-like）
6. **ragdoll** - 布偶（蓝眼，长毛）
7. ...（继续其他品种）

---

## 四、Prompt模板（严格统一）

### 基础结构
```
A cute [品种主体描述], [等级装饰描述],
[严格统一风格词],
[背景描述],
masterpiece, best quality, 8k
```

### 风格词（所有品种完全相同）
```
flat cartoon illustration, kawaii chibi style, consistent character design,
cute friendly expression, big round sparkling eyes with white highlights,
soft rounded shapes, smooth clean outlines, no sharp edges,
bright saturated warm colors, soft shading, 2D vector art style,
children book illustration style, standing pose, front facing
```

### 负面词（所有品种完全相同）
```
3D, realistic, photograph, scary, dark, complex background,
busy background, text, watermark, signature, blurry, low quality,
different style, inconsistent design
```

### 完整Prompt示例（柯基 Lv.5）
```
A cute corgi with short legs, fluffy butt, big ears, orange and white fur,
wearing small golden crown with royal cape,
flat cartoon illustration, kawaii chibi style, consistent character design,
cute friendly expression, big round sparkling eyes with white highlights,
soft rounded shapes, smooth clean outlines, no sharp edges,
bright saturated warm colors, soft shading, 2D vector art style,
children book illustration style, standing pose, front facing,
golden light rays background, soft glow,
masterpiece, best quality, 8k
```

---

## 五、操作流程

### 1. 设计品种装饰
为每个品种设计8个等级的装饰，记录在 `scripts/pet_designs/{品种id}.json`

### 2. 生成图片
```bash
python scripts/generate_pets.py --pet [品种id] --all
```

### 3. 画风检查
- 对比已生成的图片
- 确认风格统一
- 不统一则调整Prompt重新生成

### 4. 装饰审核
- 检查装饰是否清晰可见
- 检查是否符合品种特性
- 不通过则重新生成

### 5. 完成确认
8张图风格统一、装饰清晰后，标记完成

---

## 六、质量把控

### 画风统一策略
1. **使用完全相同的风格词**（复制粘贴，不改动）
2. **先生成Lv.1和Lv.8作为基准**
3. **中间等级与基准对比**，确保一致
4. **发现问题立即调整**，不累积

### 常见问题处理
| 问题 | 原因 | 解决 |
|------|------|------|
| 画风不一致 | 风格词被修改 | 复制粘贴统一风格词 |
| 太写实 | 缺少风格词 | 添加`flat cartoon illustration` |
| 品种特征不明显 | 描述不足 | 添加品种特征词（如`short legs` for corgi） |
| 装饰不清晰 | 描述不够强调 | 添加`prominently displayed` |

---

## 七、文件结构

```
scripts/
├── generate_pets.py       # 生成工具
├── strict_audit.py        # 严格审核
├── auto_regenerate.py     # 自动重生成
├── pet_designs/           # 品种装饰设计
│   ├── corgi.json
│   ├── shiba.json
│   └── ...
└── ...

public/pets/
├── corgi/
│   ├── lv1.png
│   └── ...
├── shiba/
│   └── ...
└── ...
```

---

## 八、成本估算

| 项目 | 数量 | 单价 | 总价 |
|------|------|------|------|
| 品种数量 | 25 | - | - |
| 等级 | 8 | - | - |
| 单张成本 | - | ¥0.03 | - |
| 总计 | 25 × 8 = 200 | ¥0.03 | 约¥6 |

---

**关键：严格使用统一的风格词，确保所有品种画风一致！**
