# DataSciProject - AI 研究工具开发指南

## 项目概述
这是一个基于深度学习和大语言模型的研究工具项目，用于新闻数据获取、分析和可视化。项目采用 Python 后端 + Web 前端架构，集成机器学习、深度学习和 LLM 能力。

## 架构设计

### 核心模块
1. **数据获取模块**: 新闻 API 集成、网络爬虫、自定义数据上传
2. **分析处理模块**: 文本预处理、ML/DL 模型、LLM 集成
3. **可视化模块**: 自动图表生成 (matplotlib/plotly)
4. **用户接口**: Web UI (React) 和 CLI

### 技术栈规范
- **后端框架**: Flask (RESTful API)
- **深度学习**: PyTorch
- **NLP 处理**: transformers, spacy
- **数据处理**: pandas, numpy
- **可视化**: plotly (交互式), matplotlib (静态图表)
- **数据库**: SQLite (本地开发) → PostgreSQL (生产环境)
- **前端**: React (create-react-app 或 Vite)
- **开发环境**: macOS (本地) → 阿里云 (生产)

## 开发约定

### 本地开发环境 (macOS)
```bash
# 后端设置
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# 前端设置
cd frontend
npm install
npm start
```

### 文件组织
```
├── backend/
│   ├── api/              # Flask 路由和接口
│   ├── models/           # ML/DL 模型定义
│   ├── data/             # 数据获取和爬虫模块
│   ├── analysis/         # 数据预处理和分析
│   ├── visualization/    # 图表生成
│   ├── utils/            # 工具函数
│   ├── app.py            # Flask 应用入口
│   └── requirements.txt  # Python 依赖
├── frontend/
│   ├── src/
│   │   ├── components/   # React 组件
│   │   ├── services/     # API 调用服务
│   │   ├── pages/        # 页面组件
│   │   └── App.js        # 主应用
│   └── package.json      # Node 依赖
├── tests/                # 单元测试和集成测试
├── config/               # 配置文件
├── data/                 # 本地数据存储
└── docs/                 # 文档
```

### API 端点设计
- `GET /api/news/fetch?keyword=xxx&limit=10` - 拉取新闻数据
- `GET /api/news/sources` - 获取新闻来源列表
- `POST /api/analysis/sentiment` - 情感分析
- `POST /api/analysis/topic` - 主题建模
- `POST /api/viz/generate` - 生成图表配置
- `GET /api/viz/types` - 获取图表类型
- 所有响应使用 JSON 格式
- 前端通过 `http://localhost:5000` 访问后端 API

### React 前端约定
- 使用 functional components + hooks
- API 调用统一封装在 `services/` 目录
- 状态管理: 初期使用 Context API，后续可升级 Redux
- 使用 `axios` 进行 HTTP 请求
- 图表使用 `react-plotly.js` 组件

### 代码风格
- Use English for all code comments and docstrings
- Follow PEP 8 for Python code (snake_case for functions/variables, PascalCase for classes)
- Include detailed comments for model hyperparameters and business logic
- Use meaningful variable names that are self-documenting

### 数据处理约定
- 文本预处理: 使用 `transformers` 的 tokenizer，支持中英文
- 停用词处理: 根据语言自动选择停用词表
- 数据清洗: 去重、去噪、标准化必须在分析前完成

### LLM 集成规范
- 支持 OpenAI API 和本地化 LLM (Llama, Falcon)
- 实现自然语言到图表的转换 (用户描述 → 自动生成代码和图表)
- 使用 Fine-tuned 模型进行数据总结和提取

### 可视化规范
- 默认使用 `plotly` 生成交互式图表
- 报告导出使用 `matplotlib` 静态图表
- 支持图表定制: 颜色、样式、图例可配置
- 图表类型: 折线图、柱状图、散点图、饼图、热力图

## 关键实现模式

### 模型加载示例
```python
from transformers import pipeline
# 情感分析模型
sentiment_analyzer = pipeline("sentiment-analysis", model="xxx")
```

### 数据流程
1. 数据拉取 (API/爬虫) → 2. 预处理 (清洗/分词) → 3. 模型分析 (ML/DL/LLM) → 4. 可视化 (图表生成)

### 新闻抓取模式
- 优先使用官方 API (Google News, Bing News)
- 备用方案: RSS 源 + BeautifulSoup 爬虫
- 中文新闻源: 百度新闻 (Baidu News) 和雪球财经 (Snowball/Xueqiu)
- 实现定时任务自动拉取热点数据
- 雪球适用于财经和股票相关新闻分析

## 测试要求
- 每个模块提供单元测试
- API 端点需要集成测试
- 模型性能测试 (准确率、速度)

## 部署说明
- 开发环境: 
  - 后端: macOS 本地运行 (Flask development server)
  - 前端: macOS 本地运行 (React dev server)
  - 数据库: SQLite (无需额外配置)
- 生产环境: 阿里云 ECS
  - 后端: Gunicorn + Nginx
  - 前端: 静态文件部署或 CDN
  - 数据库: PostgreSQL (阿里云 RDS)
- 配置管理: 使用环境变量和配置文件分离

## 注意事项
- LLM 调用需要错误处理和降级机制
- 大数据集分批处理避免内存溢出
- 异步任务使用 Celery 或 asyncio
- API 限流保护 (新闻源 API)
