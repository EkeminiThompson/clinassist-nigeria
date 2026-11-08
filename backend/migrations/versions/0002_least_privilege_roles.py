"""Demote previously self-registered clinician accounts to least privilege.

The prior public registration endpoint assigned clinician to every new account.
Existing administrator accounts are preserved; other roles are unchanged.
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_least_privilege_roles"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade():
    users = sa.table("users", sa.column("role", sa.String(length=32)))
    op.execute(users.update().where(users.c.role == "clinician").values(role="viewer"))

def downgrade():
    # Intentionally do not restore clinician privileges on downgrade.
    pass
