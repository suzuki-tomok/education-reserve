# AWS CloudFormation デプロイ手順

`cloudformation.yml` で以下のリソースを一括作成します。

## 作成されるリソース

| リソース | 名前 | 説明 |
|---------|------|------|
| VPC | education-reserve-vpc | 10.0.0.0/16 |
| Public Subnet × 2 | education-reserve-public-1, 2 | ALB + EC2 用（2AZ 必須） |
| Private Subnet × 2 | education-reserve-private-1, 2 | RDS 用（2AZ 必須） |
| Internet Gateway | education-reserve-igw | VPC のインターネット接続 |
| Route Table | education-reserve-public-rt | Public Subnet のルーティング |
| Security Group × 3 | alb-sg, ec2-sg, rds-sg | 各コンポーネントのファイアウォール |
| RDS | education-reserve-db | PostgreSQL（Private Subnet） |
| EC2 | education-reserve-ec2 | Docker Compose（Nginx + Gunicorn） |
| ALB | education-reserve-alb | ロードバランサー（HTTP:80） |

## パラメータ

| パラメータ | 説明 | 例 |
|-----------|------|-----|
| DBPassword | RDS のマスターパスワード（8文字以上） | mypassword123 |
| KeyPairName | EC2 の SSH キーペア名 | education-reserve-key |
| MyIP | SSH 許可する自分の IP（/32 付き） | 113.35.0.242/32 |
| GitHubRepo | リポジトリ URL（デフォルト設定済み） | — |

## 事前準備

### 1. AWS CLI の認証確認
```bash
aws sts get-caller-identity
```

自分のアカウント情報が表示されれば OK です。

### 2. EC2 キーペアの作成（初回のみ）
```bash
aws ec2 create-key-pair \
  --key-name education-reserve-key \
  --query 'KeyMaterial' \
  --output text > education-reserve-key.pem
chmod 400 education-reserve-key.pem
```

> ⚠️ `.pem` ファイルは SSH 接続に必要です。紛失するとサーバーにアクセスできなくなります。

### 3. 自分の IP アドレスを確認
```bash
curl ifconfig.me
```

表示された IP アドレスをメモしてください。

> ⚠️ この IP は次の「デプロイ」コマンドの `YOUR_IP` に使います。

## デプロイ

以下のコマンドの `YOUR_PASSWORD` と `YOUR_IP` を置き換えてから実行してください。

- `YOUR_PASSWORD` → 任意の文字列（8文字以上）。RDS の管理者パスワードになる
- `YOUR_IP` → 事前準備 3 の `curl ifconfig.me` で表示された IP アドレス
```bash
aws cloudformation create-stack \
  --stack-name education-reserve \
  --template-body file://infra/cloudformation.yml \
  --parameters \
    ParameterKey=DBPassword,ParameterValue=YOUR_PASSWORD \
    ParameterKey=KeyPairName,ParameterValue=education-reserve-key \
    ParameterKey=MyIP,ParameterValue=YOUR_IP/32 \
  --region ap-northeast-1
```

例：パスワードが `postgres123`、IP が `113.35.0.242` の場合：
```bash
aws cloudformation create-stack \
  --stack-name education-reserve \
  --template-body file://infra/cloudformation.yml \
  --parameters \
    ParameterKey=DBPassword,ParameterValue=postgres123 \
    ParameterKey=KeyPairName,ParameterValue=education-reserve-key \
    ParameterKey=MyIP,ParameterValue=113.35.0.242/32 \
  --region ap-northeast-1
```

作成に 10〜15 分かかります。

## 進捗確認
```bash
aws cloudformation describe-stacks \
  --stack-name education-reserve \
  --query "Stacks[0].StackStatus"
```

`"CREATE_COMPLETE"` になれば成功です。

## アクセス URL の確認
```bash
aws cloudformation describe-stacks \
  --stack-name education-reserve \
  --query "Stacks[0].Outputs"
```

以下が出力されます：

| 出力キー | 説明 | 例 |
|---------|------|-----|
| ALBURL | アプリの公開 URL | `http://education-reserve-alb-xxxxx.ap-northeast-1.elb.amazonaws.com` |
| AdminURL | Django Admin 画面 | 上記 URL + `/admin/` |
| SwaggerURL | Swagger UI | 上記 URL + `/api/docs/` |
| EC2PublicIP | SSH 接続用 IP | `13.113.214.72` |
| RDSEndpoint | RDS エンドポイント | `education-reserve-db.xxxxx.ap-northeast-1.rds.amazonaws.com` |

> ⚠️ 以降の手順で `EC2_PUBLIC_IP` と書かれている箇所は、ここの `EC2PublicIP` の値に置き換えてください。

## デプロイ後のセットアップ

> ⚠️ スタック作成完了後、EC2 の UserData（Docker build）に追加で 5 分ほどかかります。502 Bad Gateway が出る場合はしばらく待ってください。

### 管理者ユーザー作成

管理者ユーザーは自動作成されません。SSH で EC2 に接続して手動で作成します。

以下のコマンドの `EC2_PUBLIC_IP` を、上記 Outputs の `EC2PublicIP` の値に置き換えてください。
```bash
ssh -i education-reserve-key.pem ec2-user@EC2_PUBLIC_IP
```

- `education-reserve-key.pem` → 事前準備 2 で作成したキーペアファイル
- `ec2-user` → Amazon Linux 2023 のデフォルトユーザー名（固定値、変更不要）
- `@EC2_PUBLIC_IP` → Outputs の `EC2PublicIP`（例: `13.113.214.72`）

> 初回接続時に `Are you sure you want to continue connecting?` と聞かれたら `yes` を入力してください。

接続後、管理者ユーザーを作成：
```bash
cd education-reserve
docker-compose -f docker-compose.prod.yml exec app python manage.py createsuperuser --settings=config.settings_prod
```

作成完了後、SSH を切断：
```bash
exit
```

### 動作確認

ブラウザで Outputs に表示された `AdminURL` と `SwaggerURL` にアクセスしてください。

| 画面 | URL |
|------|-----|
| Admin 画面 | Outputs の `AdminURL` |
| Swagger UI | Outputs の `SwaggerURL` |

## トラブルシューティング

502 Bad Gateway が続く場合、SSH で UserData のログを確認してください。
```bash
ssh -i education-reserve-key.pem ec2-user@EC2_PUBLIC_IP
sudo tail -30 /var/log/cloud-init-output.log
```

確認が終わったら切断：
```bash
exit
```

## スタック削除
```bash
aws cloudformation delete-stack \
  --stack-name education-reserve \
  --region ap-northeast-1
```

全リソースが自動で削除されます。進捗確認：
```bash
aws cloudformation describe-stacks \
  --stack-name education-reserve \
  --query "Stacks[0].StackStatus"
```

`"DELETE_COMPLETE"` またはスタックが見つからないエラーになれば完了です。
