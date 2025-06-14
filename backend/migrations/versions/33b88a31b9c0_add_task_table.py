"""add task table

Revision ID: 33b88a31b9c0
Revises: c96507a67440
Create Date: 2025-06-11 19:10:59.255290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33b88a31b9c0'
down_revision = 'c96507a67440'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "task",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_token", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("is_completed", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("task")
