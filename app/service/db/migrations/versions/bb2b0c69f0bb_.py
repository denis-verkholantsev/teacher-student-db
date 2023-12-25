"""empty message

Revision ID: bb2b0c69f0bb
Revises: 275fdfb4f7a7
Create Date: 2023-12-22 00:56:35.547996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb2b0c69f0bb'
down_revision = '275fdfb4f7a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('file', schema=None) as batch_op:
        batch_op.alter_column('task_id',
               existing_type=sa.UUID(),
               nullable=True)
        batch_op.drop_constraint('file_task_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'task', ['task_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('file', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('file_task_id_fkey', 'task', ['task_id'], ['id'])
        batch_op.alter_column('task_id',
               existing_type=sa.UUID(),
               nullable=False)

    # ### end Alembic commands ###
