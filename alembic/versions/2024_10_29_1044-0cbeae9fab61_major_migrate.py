"""Major migrate

Revision ID: 0cbeae9fab61
Revises: 
Create Date: 2024-10-29 10:44:04.718856

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0cbeae9fab61"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "images",
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("path", sa.String(length=256), nullable=False),
        sa.Column("resolution", sa.String(length=128), nullable=False),
        sa.Column("size", sa.Float(), nullable=False),
        sa.Column(
            "time_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_images")),
    )
    op.create_table(
        "users",
        sa.Column("first_name", sa.String(length=32), nullable=False),
        sa.Column("second_name", sa.String(length=32), nullable=False),
        sa.Column("nickname", sa.String(length=32), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "time_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("nickname", name=op.f("uq_users_nickname")),
    )
    op.execute("INSERT INTO users (first_name, second_name, nickname, hashed_password) VALUES ('Арсений', 'Глушков', 'ars', '$pbkdf2-sha256$29000$0Zqzdq71nnPu/d/bew.B0A$svMz2P9Me3u7H7ApWseyKnsbk5VOtwoYgadPa99TuiQ'),('Артем', 'Зайцев', 'art', '$pbkdf2-sha256$29000$0BqDsLbWWitlbC2FUKoV4g$VEhxa/rbC8ydq5VnvvVWn8wmFwVfYIBIByNtTPcG/10'),('Тимофей', 'Макаренко', 'tim', '$pbkdf2-sha256$29000$QShFSMl5r/Wec651jlGqNQ$.gYApFVaT3xyIZv/41ay4Ker/9KJIED4.HRxx30ACtk')")


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("images")
