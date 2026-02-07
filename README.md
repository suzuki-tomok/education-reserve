# Education Reserve

教育機関向け予約管理システム

## 技術スタック

- Python 3.11
- Django 5.2
- Django REST Framework
- drf-spectacular（Swagger）
- django-simple-history（変更履歴）
- SQLite（開発） / PostgreSQL（本番）

## アーキテクチャ

- **Django Admin** — スタッフ向け業務画面（マスタ管理、予約管理、シフト管理、変更履歴の確認）
- **DRF API** — 生徒向け（講座検索、予約、進捗確認、アンケート提出）
- **Swagger UI** — API仕様書・動作確認（/api/docs/）

## セットアップ
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API一覧

| メソッド | エンドポイント | 説明 |
|---------|--------------|------|
| POST | /api/auth/login/ | ログイン |
| GET | /api/auth/me/ | ユーザー情報取得 |
| GET | /api/courses/ | 講座一覧 |
| GET | /api/shifts/ | 空きシフト検索 |
| GET | /api/reservations/ | 自分の予約一覧 |
| POST | /api/reservations/ | 予約作成 |
| GET | /api/progress/ | 自分の進捗 |
| POST | /api/surveys/ | アンケート提出 |

## TODO

- [x] プロジェクト構成・settings
- [x] モデル定義（11テーブル + 制約）
- [x] Django Admin（業務画面、一覧編集、一括操作）
- [x] 生徒向けAPI（6エンドポイント）
- [x] TokenAuthentication（ログイン・ユーザー情報API）
- [x] django-simple-history（全モデルの変更履歴）
- [x] Swagger UI（drf-spectacular）
- [ ] テスト（pytest + factory-boy）
- [ ] CI（GitHub Actions）
- [ ] Docker化（アプリ + PostgreSQL + Nginx）
- [ ] EC2デプロイ（Nginx + Gunicorn）
- [ ] CloudFormation（EC2 + RDS + VPC + SG）
- [ ] ER図（Mermaid）
- [ ] 業務シーケンス図（Mermaid）