"""empty message

Revision ID: 9f5634ab5893
Revises: 87fcfb039704
Create Date: 2021-10-10 12:24:52.046379

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = '9f5634ab5893'
down_revision = '87fcfb039704'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('municipality',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POLYGON', from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('real_estates', sa.Column('resource_link', sa.String(), nullable=True))
    op.alter_column('real_estates', 'price', nullable=True, existing_type=sa.String())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('real_estates', 'resource_link')
    op.alter_column('real_estates', 'price', nullable=True, existing_type=sa.Integer())
    op.drop_table('municipality')
    # ### end Alembic commands ###
