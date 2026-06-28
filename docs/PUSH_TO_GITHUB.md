# Push to GitHub

Recommended repository name: `mcms-118`.

```bash
unzip mcms-118-standard-github.zip
cd mcms-118

git init
git add .
git commit -m "initial MCMS-118 standard scaffold"
git branch -M main
git remote add origin https://github.com/tamirat-wubie/mcms-118.git
git push -u origin main
```

Before pushing, run:

```bash
python scripts/verify_repo.py
python -m pytest
```

Do not push secrets, tokens, private keys, cloud credentials, local `.env` files, or production data.
