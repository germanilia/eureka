"""Added time stamps to conversations

Revision ID: 2fd6c416d370
Revises: 43b63fb8d918
Create Date: 2024-07-28 13:26:27.306908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fd6c416d370'
down_revision: Union[str, None] = '43b63fb8d918'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('conversations', sa.Column('last_updated', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('conversations', 'last_updated')
    # ### end Alembic commands ###
