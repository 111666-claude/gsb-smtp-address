# smtp-address

邮箱地址解析与批量去重。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m address check --file addrs.txt
python3 -m address --sample=dots|label|case|internal|work
```

## 口径

- **形式**：恰好一个 `@`，两边都不能为空。
- **local**：不能以点开头或结尾，不能出现连续点；长度至少 3（内部域名的地址放宽到 1）。
- **domain**：点分标签，每个标签非空、不超过 63 字符，只含字母数字与连字符，不能以连字符开头或结尾。
- **归一化**：本地部分原样保留，域名一律小写；归一化后相同的地址算同一个。
- **覆盖层**：域名属于内部域名时，local 长度门槛放宽到 1。

## 不变量

- 每行输入给出一条结果，`valid` 不超过输入行数。
- `unique` 不超过 `valid`，且相同归一化地址只算一个。
- `scanned` 不随地址数平方级放大：两千个地址的 `scanned` 不超过 9000。

## 输出契约

`check` 打印一行 JSON：`rows`（每项含 `address`、`status`、`reason`、`normalized`、`scanned`）、`valid`、`unique`、`scanned`。
`--sample=work` 只打印 `{"addresses": N, "scanned": N}`。
