# usatyo-geometry
サンプルテストケース付き Python 幾何ライブラリ

### 依存関係
`pillowManager` を使用する場合は
```
pip3 install pillow
```

### テストの実行
コード変更時に [AOJ 計算幾何学コース](https://onlinejudge.u-aizu.ac.jp/courses/library/4/CGL/all) のサンプルケースを実行（対応部分のみ）して最低限のチェックが可能
```
python3 geometrytest.py
```

### 注意事項
- 誤差によって WA となるケースが確認されています。各問題の許容誤差を確認しつつ `EPS` を調整してください。問題によっては別のアプローチが必要な場合もあります。
- 0 付近の値では float が指数形式で出力されることによって WA になる可能性があります。`print(f"{hoge:.{DIGITS}f}")` 等を使って出力すれば問題ありません。
- 提出の際は `pillowManager` をコメントアウトする必要があります。そのまま提出した場合、AtCoder では RE になります。
