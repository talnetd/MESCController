"""empty message

Revision ID: 1148ec381aee
Revises: 0a24d676c940
Create Date: 2020-10-21 21:55:26.942319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1148ec381aee'
down_revision = '0a24d676c940'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bills', sa.Column('horsepower', sa.Float(), nullable=True))
    op.add_column('bills', sa.Column('ref_total_charge', sa.Float(), nullable=True))
    op.add_column('bills_detail', sa.Column('pricing_policy_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'bills_detail', 'pricing_policy', ['pricing_policy_id'], ['id'])
    op.add_column('customers', sa.Column('username', sa.String(length=512), nullable=True))
    op.add_column('providers', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('retailers', sa.Column('user_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('retailers', 'user_id')
    op.drop_column('providers', 'user_id')
    op.drop_column('customers', 'username')
    op.drop_constraint(None, 'bills_detail', type_='foreignkey')
    op.drop_column('bills_detail', 'pricing_policy_id')
    op.drop_column('bills', 'ref_total_charge')
    op.drop_column('bills', 'horsepower')
    # ### end Alembic commands ###
