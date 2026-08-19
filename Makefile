.PHONY: help install install-local backend frontend ingest ingest-reset salon salon-transcribe salon-structure check check-features check-syllabus check-dataset smoke clean

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
