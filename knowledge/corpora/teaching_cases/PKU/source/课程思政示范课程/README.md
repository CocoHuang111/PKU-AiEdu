# 北京大学课程思政示范课程原始数据

本目录归档北京大学教学档案袋平台课程思政示范课程的目录和正文API数据：

- `index.json`：公开目录接口快照，共66条。
- `课程思政示范课程66门完整档案-认证抓取.json`：2026-09-22在用户授权的北京大学统一身份认证会话中取得的完整API归档，包含课程基本信息、课程简介、课程思政认识、教学方法与实例、效果评价、元素对应表以及附件元数据。
- `records/`：从总归档无改写拆分出的66份单课程JSON，便于逐项核验。
- `build_structured_cases.rb`：把原始记录转换为 `PKU/course_ideology/` 中结构化Markdown的可复现脚本。

列表接口：

https://teaching.pku.edu.cn/dad/kcsz/da/queryTjKcszkc?pageNum=1&pageSize=500&yxdm=&kcmc=

平台列表页：

https://teaching.pku.edu.cn/dad/kcsz/da/list

详情页格式：

https://teaching.pku.edu.cn/dad/kcsz/da/foreignview/{DADM}

## 认证与使用边界

- 目录覆盖心理学、地学、图书情报、哲学、物理、软件工程、考古、医药政策、流行病学、护理、法律、天文学、经济学、计算机、社会工作、艺术、化学、口腔医学、解剖学和工学等领域，可作为后续寻找案例的线索。
- 正文接口需要北京大学统一身份认证；归档中不含账号、密码、Cookie或其他认证令牌。
- 附件只保留平台返回的文件名、栏目和认证URL，未批量复制视频、PDF、课件或图片二进制文件。
- 原始JSON保持平台返回内容；结构化稿只做栏目重组和HTML到Markdown转换，不推测缺失内容。
