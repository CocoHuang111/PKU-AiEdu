"""add durable evaluation worker lease fields

Revision ID: 20260909_0002
Revises: 20260907_0001
Create Date: 2026-09-09
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260909_0002"
down_revision: Union[str, Sequence[str], None] = "20260907_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("eval_tasks", sa.Column("worker_id", sa.String(64), nullable=True))
    op.add_column("eval_tasks", sa.Column("heartbeat_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column(
        "eval_tasks",
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_eval_tasks_worker_heartbeat", "eval_tasks", ["worker_id", "heartbeat_at"])


def downgrade() -> None:
    op.drop_index("ix_eval_tasks_worker_heartbeat", table_name="eval_tasks")
    op.drop_column("eval_tasks", "attempt_count")
    op.drop_column("eval_tasks", "heartbeat_at")
    op.drop_column("eval_tasks", "worker_id")
