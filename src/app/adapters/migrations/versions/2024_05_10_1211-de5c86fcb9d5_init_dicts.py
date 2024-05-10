"""init dicts

Revision ID: de5c86fcb9d5
Revises: 5c79a9bc475e
Create Date: 2024-05-10 12:11:40.187822

"""
from typing import Sequence, Union

from pathlib import Path

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de5c86fcb9d5'
down_revision: Union[str, None] = '5c79a9bc475e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

sql_path = Path(__file__).parent.parent.joinpath('scripts').joinpath('init_dictionaries.sql')


def upgrade() -> None:
    with open(sql_path, 'r') as f:
        for line in f.readlines():
            op.execute(line)


def downgrade() -> None:
    op.execute('TRUNCATE TABLE user_roles;')
    op.execute('TRUNCATE TABLE dataset_types;')
    op.execute('TRUNCATE TABLE model_types;')
    op.execute('TRUNCATE TABLE metrics;')
