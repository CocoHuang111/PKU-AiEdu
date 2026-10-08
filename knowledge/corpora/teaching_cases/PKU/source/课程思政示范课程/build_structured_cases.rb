# encoding: UTF-8

require "cgi"
require "fileutils"
require "json"
require "open3"

abort "usage: ruby build_structured_cases.rb MASTER_JSON" unless ARGV.length == 1

source_dir = File.expand_path(__dir__)
pku_dir = File.expand_path("../..", source_dir)
output_dir = File.join(pku_dir, "course_ideology")
records_dir = File.join(source_dir, "records")
master_path = File.expand_path(ARGV.fetch(0))

FileUtils.mkdir_p(output_dir)
FileUtils.mkdir_p(records_dir)

archive = JSON.parse(File.binread(master_path))
records = archive.fetch("records")
abort "expected 66 records" unless records.length == 66

def html_to_markdown(value)
  html = value.to_s.strip
  return "原档案未填写。" if html.empty?

  html = html
    .gsub(/(?:\.\.\/){3}tp\//, "https://teaching.pku.edu.cn/dad/tp/")
    .gsub(/([\"'=])(\/dad\/)/, "\\1https://teaching.pku.edu.cn\\2")
  out, err, status = Open3.capture3(
    "pandoc", "-f", "html", "-t", "gfm", "--wrap=none",
    stdin_data: html
  )
  raise "pandoc failed: #{err}" unless status.success?

  cleaned = out
    .gsub(/<\/?span\b[^>]*>/i, "")
    .lines
    .reject { |line| line.strip == "\\" }
    .join
    .strip
  cleaned.empty? ? "原档案未填写。" : cleaned
end

def plain(value)
  text = value.to_s
    .gsub(/<br\s*\/?>/i, " ")
    .gsub(/<[^>]+>/, " ")
  CGI.unescapeHTML(text).gsub(/\s+/, " ").strip
end

def cell(value)
  text = plain(value)
  text = "—" if text.empty?
  text.gsub("|", "\\|")
end

def safe_name(value)
  value.to_s.gsub(/[\\\/:*?\"<>|]/, "-").gsub(/\s+/, "-").gsub(/-+/, "-").sub(/\A-/, "").sub(/-\z/, "")
end

def absolute_url(value)
  url = value.to_s
  return "" if url.empty?
  url.start_with?("/") ? "https://teaching.pku.edu.cn#{url}" : url
end

index_rows = []

records.sort_by { |record| record.dig("catalog", "ROW_ID").to_i }.each do |record|
  catalog = record.fetch("catalog")
  base = record.fetch("base")
  detail = record.fetch("detail")
  elements = record.fetch("elements")

  number = format("%02d", catalog.fetch("ROW_ID").to_i)
  course = catalog.fetch("KCMC")
  slug = safe_name(course)
  filename = "#{number}-#{slug}.md"
  record_filename = "#{number}-#{slug}.json"
  source_url = "https://teaching.pku.edu.cn/dad/kcsz/da/foreignview/#{catalog.fetch("DADM")}" 

  File.write(
    File.join(records_dir, record_filename),
    JSON.pretty_generate(record) + "\n",
    mode: "w:UTF-8"
  )

  element_rows = elements.map do |item|
    attachments = (item["fjs"] || []).map do |attachment|
      name = attachment["wjm"] || attachment["wjmc"] || File.basename(attachment["fjlj"].to_s)
      url = absolute_url(attachment["fjlj"])
      url.empty? ? name : "[#{name}](#{url})"
    end
    [
      cell(item["zj"]),
      cell(item["zsd"]),
      cell(item["szys"]),
      cell([item["szwd"], item["ejwd"]].compact.reject(&:empty?).join(" / ")),
      cell(item["jxff"]),
      attachments.empty? ? "—" : attachments.join("<br>")
    ]
  end

  attachments = []
  (detail["fjList"] || []).each do |attachment|
    attachments << {
      section: attachment["bs"],
      name: attachment["wjmc"] || attachment["wjm"] || File.basename(attachment["wjlj"].to_s),
      url: absolute_url(attachment["wjlj"])
    }
  end
  elements.each do |item|
    (item["fjs"] || []).each do |attachment|
      attachments << {
        section: "课程思政元素对应表",
        name: attachment["wjm"] || attachment["wjmc"] || File.basename(attachment["fjlj"].to_s),
        url: absolute_url(attachment["fjlj"])
      }
    end
  end

  metadata = [
    ["课程", course],
    ["教师/团队", catalog["td"]],
    ["负责人", catalog["JSXM"]],
    ["课程代码", catalog["KCDM"]],
    ["档案代码", catalog["DADM"]],
    ["课程性质", base["sfbxkc"].to_s == "1" ? "必修课（按平台字段）" : (base["sfbxkc"].to_s == "0" ? "选修课（按平台字段）" : "原档案未填写")],
    ["建档时间", base["cjsj"]],
    ["最后更新时间", base["xgsj"]]
  ]

  lines = []
  lines << "# 北京大学课程思政示范课程：#{course}"
  lines << ""
  lines << "**材料性质**：北京大学教学档案袋平台原始档案的忠实结构化整理（需统一身份认证访问）"
  lines << ""
  lines << "## 基本信息"
  lines << ""
  lines << "| 字段 | 平台原文 |"
  lines << "| --- | --- |"
  metadata.each { |key, value| lines << "| #{key} | #{cell(value)} |" }
  lines << ""
  lines << "## 课程简介"
  lines << ""
  lines << html_to_markdown(base["kcjj"])
  lines << ""
  lines << "## 对课程思政的认识与理解"
  lines << ""
  lines << html_to_markdown(detail["rsylj"])
  lines << ""
  lines << "## 课程思政元素对应表"
  lines << ""
  if element_rows.empty?
    lines << "原档案未填写。"
  else
    lines << "| 章节/周主题 | 知识点 | 思政元素 | 所属维度 | 教学方法 | 附件 |"
    lines << "| --- | --- | --- | --- | --- | --- |"
    element_rows.each { |row| lines << "| #{row.join(" | ")} |" }
  end
  lines << ""
  lines << "## 教学方法与实例"
  lines << ""
  lines << html_to_markdown(detail["jxffjal"])
  lines << ""
  lines << "## 效果评价"
  lines << ""
  lines << html_to_markdown(detail["xgpj"])
  lines << ""
  lines << "## 附件索引"
  lines << ""
  if attachments.empty?
    lines << "原档案未列出附件。"
  else
    attachments.uniq { |item| [item[:name], item[:url]] }.each do |attachment|
      label = attachment[:section].to_s.empty? ? "未标栏目" : attachment[:section]
      if attachment[:url].empty?
        lines << "- #{label}：#{attachment[:name]}"
      else
        lines << "- #{label}：[#{attachment[:name]}](#{attachment[:url]})"
      end
    end
  end
  lines << ""
  lines << "## 证据与使用边界"
  lines << ""
  lines << "本文件只重组平台已有栏目，不补写平台未提供的教学效果。教师陈述、课程荣誉、学生反馈与参与数据均保留其原始证据性质；没有对照或学习测量时，不应改写为教学方法的严格因果效果。附件链接可能需要北京大学统一身份认证。"
  lines << ""
  lines << "## 来源"
  lines << ""
  lines << "- 平台详情页：#{source_url}"
  lines << "- 本地原始API记录：`../source/课程思政示范课程/records/#{record_filename}`"
  lines << "- 总归档：`../source/课程思政示范课程/课程思政示范课程66门完整档案-认证抓取.json`"
  lines << "- 抓取日期：2026-09-22"

  File.write(File.join(output_dir, filename), lines.join("\n") + "\n", mode: "w:UTF-8")
  index_rows << [number, course, catalog["JSXM"], catalog["td"], filename, record_filename, source_url]
end

readme = []
readme << "# 北京大学课程思政示范课程结构化案例"
readme << ""
readme << "本目录收录北京大学教学档案袋平台课程思政示范课程66份。2026-09-22在用户授权的统一身份认证会话中取得课程正文API数据，并按平台原有栏目结构化；不保存账号、密码、Cookie或其他认证令牌。"
readme << ""
readme << "每份文件包含基本信息、课程简介、课程思政认识、元素对应表、教学方法与实例、效果评价、附件索引和来源。平台正文中的HTML由Pandoc转换为Markdown；每门课程的未改写JSON记录保存在 `../source/课程思政示范课程/records/`，总归档保存在同一来源目录。"
readme << ""
readme << "## 案例索引"
readme << ""
readme << "| 序号 | 课程 | 负责人 | 教师/团队 | 整理稿 | 原始记录 |"
readme << "| ---: | --- | --- | --- | --- | --- |"
index_rows.each do |number, course, lead, team, filename, record_filename, _url|
  readme << "| #{number.to_i} | #{cell(course)} | #{cell(lead)} | #{cell(team)} | [#{filename}](<#{filename}>) | [JSON](<../source/课程思政示范课程/records/#{record_filename}>) |"
end
readme << ""
readme << "## 使用边界"
readme << ""
readme << "- 这些材料是课程档案，不等同于经同行评审的教育研究论文。"
readme << "- 附件仅保留平台元数据和认证链接；视频、PDF、课件及图片二进制文件未批量复制。"
readme << "- 课程之间可能与 `PKU/01–32` 的教改案例或教师专访重叠，统计时不宜直接当作互不重复的课程。"
readme << "- 访问和再使用应遵守北京大学平台规则及原作者版权。"

File.write(File.join(output_dir, "README.md"), readme.join("\n") + "\n", mode: "w:UTF-8")

puts "generated #{records.length} structured cases in #{output_dir}"
