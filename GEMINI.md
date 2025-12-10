# Splatoon3 Assistant

> **同步说明**: 本文件与 `GEMINI.md` 内容保持一致，修改任意一个时请同时更新另一个。

## 项目简介

Splatoon3 游戏助手 - 通过获取 Splatoon3 的战斗数据及其他辅助数据进行数据分析。

## 参考项目

主要参考 `../reference-project/splatoon3-nso`，其他 `../reference-project` 下的项目作为辅助参考。

> **注意**: 不要直接引用 `../reference-project` 下的代码，如需引用则将代码复制到本项目中。

---

## 项目结构

```
splatoon3-assistant/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── config.py            # 配置管理
│   ├── http_client.py       # HTTP 客户端封装
│   ├── nso_auth.py          # NSO 认证 (参照 S3S 类)
│   ├── graphql_utils.py     # GraphQL 工具
│   └── splatnet3_api.py     # SplatNet3 API (参照 Splatoon 类)
├── tests/
│   └── test_full_flow.py    # 功能测试
├── requirements.txt         # Python 依赖
├── CLAUDE.md               # 项目文档
└── GEMINI.md               # 项目文档 (与 CLAUDE.md 同步)
```

---

## 核心 API

### NSOAuth - 认证 (参照 splatoon3-nso 的 S3S 类)

```python
from src import NSOAuth

auth = NSOAuth()

# Step 1: 生成登录 URL
url, verifier = await auth.login_in()

# Step 2: 获取 session_token
session_token = await auth.login_in_2(callback_url, verifier)

# Step 3: 获取 g_token
access_token, g_token, nickname, lang, country, user_info = await auth.get_gtoken(session_token)

# Step 4: 获取 bullet_token
bullet_token = await auth.get_bullet(g_token)
```

### SplatNet3API - 数据查询 (参照 splatoon3-nso 的 Splatoon 类)

```python
from src import SplatNet3API

api = SplatNet3API(g_token, bullet_token)

# 对战查询
battles = await api.get_recent_battles()      # 最近对战
bankara = await api.get_bankara_battles()     # 蛮颓对战
x_battles = await api.get_x_battles()         # X 赛
detail = await api.get_battle_detail(id)      # 对战详情

# 打工查询
coops = await api.get_coops()                 # 打工历史
coop_detail = await api.get_coop_detail(id)   # 打工详情

# 其他查询
friends = await api.get_friends()             # 好友列表
schedule = await api.get_schedule()           # 日程
```

---

## 快速开始

```bash
# 1. 创建虚拟环境
cd splatoon3-assistant
python3 -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行功能测试
python tests/test_full_flow.py
```

---

## 开发日志

### 2024-12-10: NSO API 集成完成

**完成项目**:
- [x] 完全参照 `splatoon3-nso` 项目实现认证模块
- [x] 方法名与参考项目保持一致 (`login_in`, `login_in_2`, `get_bullet`)
- [x] 使用全局变量管理版本号缓存
- [x] 实现完整的 GraphQL API 封装
- [x] 创建功能测试文件
- [x] 所有 8 个 Python 模块语法检查通过

---

## 修改建议

如果在思考过程中觉得需要修改该文件，请将修改建议补充到此处。