# デプロイ手順

## venv を初期化して立ち上げる

```bash
python3 -m venv .venv
source .venv/bin/activate
```

windows の人は ↓

```powershell
python3 -m venv .venv
.venv\Scripts\activate.bat
```

## 必要なモジュールをインストール

```bash
pip install -r requirements.txt
```

## デプロイ

```bash
cdk deploy TodoappPyStack
```

# 動作確認手順

↓ のコマンドを実行

```bash
export ENDPOINT="API Gatewayのエンドポイント"
bash tests/test.bash
```
