"""Table for municipalities

Revision ID: 87fcfb039704
Revises: 
Create Date: 2021-10-01 08:13:53.318632

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = '87fcfb039704'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('municipality',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column(
        'geom',
        geoalchemy2.types.Geometry(
            geometry_type='POLYGON',
            from_text='ST_GeomFromEWKT',
            name='geometry'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('real_estates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column(
        'coords',
        geoalchemy2.types.Geometry(
            geometry_type='POINT',
            from_text='ST_GeomFromEWKT',
            name='geometry', nullable=True)
        ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('municipality')
    op.drop_table('real_estates')
    # ### end Alembic commands ###