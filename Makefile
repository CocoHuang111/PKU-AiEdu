.PHONY: help install install-local backend frontend ingest ingest-reset salon salon-transcribe salon-structure check check-features check-syllabus check-dataset check-expert-rules expert-rules-ingest expert-rules-extract expert-rules-distill check-gb train-gb train-gb-2018 train-gb-2018-v7 train-gb-2018-v4 train-gb-live rejudge-2018-v7-effect rejudge-2018-v9 judge-overall-2018 smoke clean

PY ?= python
BACKEND_PORT ?= 8010

help:
	@echo "北大问教 2.0"
	@echo ""
	@echo "  make install        安装基础依赖（需先 conda activate pku2）"
	@echo "  make install-local  安装可选依赖（本地 embedding/rerank、说话人分离）"
	@echo "  make check          环境自检（ffmpeg / faster-whisper / API Key / providers）"
	@echo "  make check-features 客观特征自检（不调大模型，不花额度）"
	@echo "  make check-syllabus 大纲校验单元测试（不调大模型，不花额度）"
	@echo "  make check-dataset  微格数据集 inventory 匹配（不调大模型）"
	@echo "  make check-expert-rules 专家评分规则与可观察性测试（不调大模型）"
	@echo "  make expert-rules-ingest 四份评分表清洗成长表（不调大模型）"
	@echo "  make expert-rules-extract 从评语抽原子观点（会调大模型，可续跑）"
	@echo "  make expert-rules-distill 生成待人工审核的结构化规则（会调大模型）"
	@echo "  make check-gb       GB 训练约定（离散化/划分/玩具拟合）"
	@echo "  make train-gb       四个 GB 对照（同一 2022 预测集）再比较"
	@echo "  make train-gb-2018  2018 fixed_prompt / effect_inferred 上训四种 GB"
	@echo "  make train-gb-2018-v7  修正专家分制后，在 2018 v7 上训四种 GB"
	@echo "  make train-gb-2018-v4  恢复 2018 v4 快照后训六种 GB（含客观/二级）"
	@echo "  make train-gb-live  2018 v9 全量五维 5 分类 → 线上总分模型"
	@echo "  make rejudge-2018-v7-effect  v7.1 恢复教学效果预期效果兜底"
	@echo "  make rejudge-2018-v9  v9 严重度校准与五维诊断报告"
	@echo "  make judge-overall-2018 2018 测试集五维+客观特征 LLM 盲评总分"
	@echo "  make smoke          打分链路冒烟测试（会调大模型）"
	@echo "  make backend        启动 FastAPI     http://localhost:$(BACKEND_PORT)/docs"
	@echo "  make frontend       启动 Vite        http://localhost:5174"
	@echo "  make ingest         构建向量库（增量）"
	@echo "  make ingest-reset   重建向量库（清空后重建）"
	@echo "  make salon          沙龙视频 → 转写 + 教学知识 Markdown"
	@echo "  make salon-transcribe  只做沙龙 ASR 转写（small 模型）"
	@echo "  make salon-structure   只做沙龙 LLM 结构化（需已有转写）"

install:
	$(PY) -m pip install -r requirements.txt

install-local:
	$(PY) -m pip install -r requirements-local.txt

check:
	$(PY) -m scripts.check_env

check-features:
	$(PY) -m scripts.check_features

check-syllabus:
	$(PY) -m unittest scripts.test_syllabus_validation

check-dataset:
	$(PY) -m scripts.test_eval_dataset

check-expert-rules:
	$(PY) -m unittest scripts.test_expert_rules

expert-rules-ingest:
	$(PY) -m scripts.build_expert_rules ingest

expert-rules-extract:
	$(PY) -m scripts.build_expert_rules extract --resume

expert-rules-distill:
	$(PY) -m scripts.build_expert_rules distill

check-gb:
	$(PY) -m scripts.test_gb

# 四个 GB 对照，共用 dataset/gb_split.json（从 2022 划预测集）
train-gb:
	$(PY) -m scripts.train_gb_obj_reg
	$(PY) -m scripts.train_gb_llm_reg
	$(PY) -m scripts.train_gb_llm_cls5
	$(PY) -m scripts.train_gb_llm_cls8
	$(PY) -m scripts.compare_gb

train-gb-2018:
	$(PY) -m scripts.train_gb_2018_prompts

train-gb-2018-v7:
	$(PY) -m scripts.train_gb_obj_reg --data dataset/2018_spring/goal_v7/training_gb.csv --alignment dataset/2018_spring/goal_v7/alignment.csv --split dataset/2018_spring/gb_split.json --out-dir models/2018_goal_v7 --hold-year within
	$(PY) -m scripts.train_gb_llm_reg --data dataset/2018_spring/goal_v7/training_gb.csv --alignment dataset/2018_spring/goal_v7/alignment.csv --split dataset/2018_spring/gb_split.json --out-dir models/2018_goal_v7 --hold-year within
	$(PY) -m scripts.train_gb_llm_cls5 --data dataset/2018_spring/goal_v7/training_gb.csv --alignment dataset/2018_spring/goal_v7/alignment.csv --split dataset/2018_spring/gb_split.json --out-dir models/2018_goal_v7 --hold-year within
	$(PY) -m scripts.train_gb_llm_cls8 --data dataset/2018_spring/goal_v7/training_gb.csv --alignment dataset/2018_spring/goal_v7/alignment.csv --split dataset/2018_spring/gb_split.json --out-dir models/2018_goal_v7 --hold-year within
	$(PY) -m scripts.compare_gb --pred-dir models/2018_goal_v7 --out dataset/2018_spring/goal_v7/gb_predictions.csv --title "2018 goal_v7（修正分制）"

train-gb-2018-v4:
	$(PY) -m scripts.train_gb_2018_v4

train-gb-live:
	$(PY) -m scripts.train_gb_live

rejudge-2018-v7-effect:
	$(PY) -m scripts.build_eval_dataset rejudge --dir dataset/2018_spring --prompt-version v7.1-goal-effect-fallback --output-cache cache_goal_effect_v7_1 --resume

rejudge-2018-v9:
	$(PY) -m scripts.build_eval_dataset rejudge --dir dataset/2018_spring --prompt-version v9-calibrated --output-cache cache_v9 --resume

judge-overall-2018:
	$(PY) -m scripts.judge_overall --dir dataset/2018_spring --scores-cache cache_effect_inferred --split dataset/2018_spring/gb_split.json --gb-predictions dataset/2018_spring/effect_inferred/gb_predictions.csv --expert-detail dataset/2018_spring/effect_inferred/training_detail.csv --out-dir dataset/2018_spring/effect_inferred/llm_overall --prompt-version overall-v1 --resume

smoke:
	$(PY) -m scripts.smoke_test

backend:
	$(PY) -m uvicorn backend.app.main:app --reload --port $(BACKEND_PORT)

frontend:
	cd frontend && npm install && npm run dev

ingest:
	$(PY) -m knowledge.ingest

ingest-reset:
	$(PY) -m knowledge.ingest --reset

salon:
	$(PY) -m knowledge.process_salon

salon-transcribe:
	$(PY) -m knowledge.process_salon --transcribe

salon-structure:
	$(PY) -m knowledge.process_salon --structure

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
