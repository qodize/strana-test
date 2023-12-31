"""initial

Revision ID: c3afe7e178a7
Revises: 
Create Date: 2023-10-29 22:16:10.737564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3afe7e178a7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metrics',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('serviceName', sa.String(), nullable=False),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('responseTimeMs', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('metrics')
    # ### end Alembic commands ###
