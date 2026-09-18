# 视频提交后体验与邮件通知

- 默认展示北大网盘链接导入，保留本地视频入口。
- 提交成功后展示估算完成时间，不展示队列人数；可关闭页面或一键转到智能问答/大纲优化。
- 使用近期成功任务的实际处理秒数中位数，加上前方任务负载估算范围；无样本时初步按每任务 2 小时估算，范围 50%–150%。
- 初步基准可通过 `EVALUATION_ESTIMATE_SECONDS` 调整，不是完成时间承诺。
- 邮件可选；缺少邮箱时转到个人资料，保存后自动为原任务登记通知并返回任务。
- 通知申请保存在个人设置 JSON 中，无数据库迁移；尚无服务时状态为 `waiting_service`，不能误报已开启发送。
- Worker 的独立异步循环约每分钟检查通知，不必等另一个视频的长时间解析结束。
- 邮件发送登录后查看报告的链接，不发送原视频/报告附件。失败最多尝试 5 次，指数退避；固定 Message-ID。
- SMTP 接受服务器确认后再标记成功；极端崩溃可能重复发送，不承诺 exactly-once。

## 服务端配置

```dotenv
SMTP_HOST=smtp.example.org
SMTP_PORT=587
SMTP_SECURITY=starttls
SMTP_FROM=service@example.org
SMTP_USERNAME=service@example.org
SMTP_PASSWORD=<仅在服务器配置授权码，不提交 Git>
APP_PUBLIC_URL=https://8.141.113.98
EVALUATION_ESTIMATE_SECONDS=7200
```

也支持 `SMTP_SECURITY=ssl` / 465；不允许明文 SMTP。
完成配置后重建后端/Worker 环境，已有待配置通知会自动等待任务完成后发送。
注意个人资料邮箱尚无验证流程，因此邮件仅包含需本人登录的报告入口，不附带敏感材料。
