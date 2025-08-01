# Judy's Skin Web Application

一個基於 Flask 的皮膚護理產品電商網站，提供前台購物介面和後台管理系統。

## 🚀 功能特色

- **前台購物介面**: 用戶註冊、登入、商品瀏覽和購買
- **後台管理系統**: 商品管理、訂單處理、用戶管理
- **響應式設計**: 支援桌面和行動裝置
- **資料庫整合**: 使用 MySQL 資料庫儲存資料
- **安全性**: 用戶認證和授權機制

## 🛠️ 技術架構

- **後端框架**: Flask 3.1.1
- **資料庫**: MySQL (AWS RDS)
- **前端**: HTML, CSS, JavaScript
- **模板引擎**: Jinja2
- **環境配置**: python-dotenv

## 📋 系統需求

- Python 3.8+
- MySQL 資料庫
- 網頁瀏覽器

## 🔧 安裝與設定

### 1. 克隆專案

```bash
git clone <repository-url>
cd judys-skin-web
```

### 2. 建立虛擬環境

```bash
python -m venv venv
```

### 3. 啟動虛擬環境

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. 安裝依賴套件

```bash
pip install -r reqirements.txt
```

### 5. 環境變數設定

建立 `.env` 檔案並設定以下變數：

```env
SECRET_KEY=your-secret-key
RDS_HOST=your-mysql-host
RDS_USER=your-mysql-username
RDS_PASSWORD=your-mysql-password
RDS_DATABASE=judys-skin-db
RDS_PORT=3306
```

### 6. 資料庫初始化

確保 MySQL 資料庫已建立並可連線。

## 🚀 執行應用程式

### 本地開發模式

```bash
python app.py
```

應用程式將在 `http://localhost:5004` 啟動

### 生產環境部署

使用 Gunicorn 部署：

```bash
gunicorn -w 4 -b 0.0.0.0:5004 app:app
```

## 📁 專案結構

```
judys-skin-web/
├── app.py                 # 主應用程式入口
├── config.py              # 配置檔案
├── reqirements.txt        # Python 依賴套件
├── db/                    # 資料庫相關模組
│   ├── __init__.py
│   ├── db_init.py
│   ├── db_orders.py
│   ├── db_products.py
│   └── db_users.py
├── routes/                # 路由模組
│   ├── admin.py          # 後台管理路由
│   ├── auth.py           # 認證路由
│   ├── backend.py        # 後端 API 路由
│   └── frontend.py       # 前台路由
├── static/                # 靜態檔案
│   ├── css/
│   └── js/
├── templates/             # HTML 模板
│   ├── backend/
│   └── frontend/
└── venv/                  # Python 虛擬環境
```

## 🔐 主要功能模組

### 認證系統 (`routes/auth.py`)

- 用戶註冊
- 用戶登入/登出
- 密碼加密

### 前台介面 (`routes/frontend.py`)

- 首頁展示
- 商品瀏覽
- 購物車功能

### 後台管理 (`routes/admin.py`)

- 商品管理
- 訂單處理
- 用戶管理

### 後端 API (`routes/backend.py`)

- RESTful API 端點
- 資料處理邏輯

## 🗄️ 資料庫結構

專案使用 MySQL 資料庫，主要包含以下表格：

- `users`: 用戶資料
- `products`: 商品資料
- `orders`: 訂單資料

## 🔧 開發指南

### 新增路由

1. 在 `routes/` 目錄下建立新的路由檔案
2. 在 `app.py` 中註冊 Blueprint

### 新增模板

1. 在 `templates/` 目錄下建立 HTML 檔案
2. 使用 Jinja2 語法進行模板渲染

### 資料庫操作

使用 `db/` 目錄下的模組進行資料庫操作。

## 🐛 故障排除

### 常見問題

1. **資料庫連線失敗**

   - 檢查 `.env` 檔案中的資料庫設定
   - 確認 MySQL 服務正在運行

2. **套件安裝失敗**

   - 確認 Python 版本符合需求
   - 重新建立虛擬環境

3. **端口被占用**
   - 修改 `app.py` 中的端口設定
   - 或終止占用端口的程序

## 📝 版本資訊

- **當前版本**: 1.0.0
- **最後更新**: 2024 年

## 📄 授權條款

本專案採用 MIT 授權條款。

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request 來改善這個專案。

## 📞 聯絡資訊

如有任何問題或建議，請聯絡開發團隊。
