"""manual add title description constraints

Revision ID: f35647117c7b
Revises: 27c5a849d0d9
Create Date: 2023-12-24 00:27:59.203446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f35647117c7b'
down_revision = '27c5a849d0d9'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=500),
               existing_nullable=True)
        
    with op.batch_alter_table('solution', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=500),
               existing_nullable=True)
        
    with op.batch_alter_table('homework', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=500),
               existing_nullable=True)
        
    with op.batch_alter_table('exercise', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(),
               type_=sa.String(length=500),
               existing_nullable=True)
        


def downgrade():
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(),
               existing_nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        
    with op.batch_alter_table('solution', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        
    with op.batch_alter_table('homework', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(),
               existing_nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        
    with op.batch_alter_table('exercise', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(),
               existing_nullable=True)