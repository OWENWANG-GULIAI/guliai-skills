# 本机素材合同

只有配置缺失、素材路径失效或需要重新安装时读取本文件。

## 私有配置

配置文件位于 Skill 的 `state/local-config.json`，只存在于用户本机。源 Skill 不打包肖像、二维码、Logo、聊天原文或绝对私人路径。

首次配置：

```bash
python3 scripts/daily_signature_ops.py configure \
  --portrait "/absolute/path/to/portrait.png" \
  --logo "/absolute/path/to/logo.png" \
  --qr "/absolute/path/to/wechat-qr.jpg" \
  --output-dir "/absolute/path/to/output"
```

脚本会写入画布和当前基准坐标。配置文件不得复制到公开仓库。

## 素材角色

- `portrait.path`：兼容旧配置的默认身份参考。
- `portrait_variants`：可选人物资产池。每项包含 `id`、`path`、`kind` 与简短 `use_case`；每张日签选择其中一项作为人物身份、服装、姿态或插画风格参考。真人肖像优先用于身份保持；插画版只在需要明确水彩/插画表达时作为风格与构图参考。
- `qr.path`：最终联系入口。由 ffmpeg 以最近邻插值缩放后覆盖；生图模型不接触二维码。
- `logo.path`：官方横向 Logo。由 ffmpeg 等比使用源画布叠加；生图模型不重绘品牌字标。
- `output_directory`：只管理 `今日日签海报.png` 与 `朋友圈文案.md` 两个固定文件。

二维码缺失时不交付最终版。人物或 Logo 缺失时可以做待补素材的预览底图，但不得发布或替换上一组正式文件。

人物资产池示例：

```json
{
  "portrait_variants": [
    {
      "id": "white-seat",
      "path": "/absolute/path/to/white-suit-seat.png",
      "kind": "photo",
      "use_case": "沉静思考、判断、复盘"
    },
    {
      "id": "watercolor-profile",
      "path": "/absolute/path/to/watercolor-profile.png",
      "kind": "illustration",
      "use_case": "转向、新局、轻情绪视觉表达"
    }
  ]
}
```

## 确定性命令

```bash
python3 scripts/daily_signature_ops.py compose \
  --base /path/to/generated-base.png \
  --output /path/to/.tmp-date-poster.png

python3 scripts/daily_signature_ops.py validate \
  --poster /path/to/.tmp-date-poster.png \
  --copy /path/to/.tmp-date-copy.md

python3 scripts/daily_signature_ops.py publish \
  --poster /path/to/.tmp-date-poster.png \
  --copy /path/to/.tmp-date-copy.md
```

`publish` 先验证，再替换固定文件；第二个替换失败时恢复上一组文件。
