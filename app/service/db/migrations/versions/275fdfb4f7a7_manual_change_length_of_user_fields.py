"""manual change length of user fields

Revision ID: 275fdfb4f7a7
Revises: d119454e1289
Create Date: 2023-12-21 17:56:10.778767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '275fdfb4f7a7'
down_revision = 'd119454e1289'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user_', schema=None) as batch_op:
        batch_op.alter_column('first_name',
               existing_type=sa.String(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.alter_column('last_name',
               existing_type=sa.String(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)

def downgrade():
    with op.batch_alter_table('user_', schema=None) as batch_op:
        batch_op.alter_column('first_name',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.alter_column('last_name',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(),
               existing_nullable=True)
