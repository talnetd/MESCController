"""empty message

Revision ID: 7235f2652b45
Revises: 95c40fb2ae77
Create Date: 2020-10-27 19:12:08.161104

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7235f2652b45'
down_revision = '95c40fb2ae77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('providers')
    op.drop_table('retailers')
    op.add_column('ab_user', sa.Column('commission_fee', sa.Float(), nullable=True))
    op.add_column('ab_user', sa.Column('ref_code', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ab_user', 'ref_code')
    op.drop_column('ab_user', 'commission_fee')
    op.create_table('retailers',
    sa.Column('created_on', mysql.DATETIME(), nullable=False),
    sa.Column('changed_on', mysql.DATETIME(), nullable=False),
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=512), nullable=True),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('created_by_fk', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('changed_by_fk', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id'], name='retailers_ibfk_2'),
    sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id'], name='retailers_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('providers',
    sa.Column('created_on', mysql.DATETIME(), nullable=False),
    sa.Column('changed_on', mysql.DATETIME(), nullable=False),
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('provider_code', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=512), nullable=True),
    sa.Column('name', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=512), nullable=True),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('created_by_fk', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('changed_by_fk', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('commission_fee', mysql.FLOAT(), nullable=True),
    sa.ForeignKeyConstraint(['changed_by_fk'], ['ab_user.id'], name='providers_ibfk_2'),
    sa.ForeignKeyConstraint(['created_by_fk'], ['ab_user.id'], name='providers_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
