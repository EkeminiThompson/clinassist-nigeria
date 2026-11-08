"""Initial ClinAssist identity, audit and offline receipt tables."""
from alembic import op
import sqlalchemy as sa
revision="0001_initial"
down_revision=None
branch_labels=None
depends_on=None
def upgrade():
    op.create_table("users",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("email",sa.String(length=320),nullable=False),
        sa.Column("full_name",sa.String(length=160),nullable=False),
        sa.Column("hashed_password",sa.String(length=255),nullable=False),
        sa.Column("role",sa.String(length=32),nullable=False),
        sa.Column("is_active",sa.Boolean(),nullable=False),
        sa.Column("created_at",sa.DateTime(timezone=True),nullable=False))
    op.create_index("ix_users_email","users",["email"],unique=True)
    op.create_table("audit_logs",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("user_id",sa.Integer(),sa.ForeignKey("users.id"),nullable=True),
        sa.Column("action",sa.String(length=80),nullable=False),
        sa.Column("resource",sa.String(length=120),nullable=False),
        sa.Column("details",sa.Text(),nullable=False),
        sa.Column("created_at",sa.DateTime(timezone=True),nullable=False))
    op.create_index("ix_audit_logs_user_id","audit_logs",["user_id"])
    op.create_index("ix_audit_logs_action","audit_logs",["action"])
    op.create_index("ix_audit_logs_created_at","audit_logs",["created_at"])
    op.create_table("sync_receipts",
        sa.Column("id",sa.Integer(),primary_key=True),
        sa.Column("user_id",sa.Integer(),sa.ForeignKey("users.id"),nullable=False),
        sa.Column("client_id",sa.String(length=80),nullable=False),
        sa.Column("record_type",sa.String(length=32),nullable=False),
        sa.Column("client_created_at",sa.DateTime(timezone=True),nullable=False),
        sa.Column("received_at",sa.DateTime(timezone=True),nullable=False),
        sa.UniqueConstraint("user_id","client_id",name="uq_sync_receipt_user_client"))
    op.create_index("ix_sync_receipts_user_id","sync_receipts",["user_id"])
def downgrade():
    op.drop_index("ix_sync_receipts_user_id",table_name="sync_receipts")
    op.drop_table("sync_receipts")
    op.drop_index("ix_audit_logs_created_at",table_name="audit_logs")
    op.drop_index("ix_audit_logs_action",table_name="audit_logs")
    op.drop_index("ix_audit_logs_user_id",table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index("ix_users_email",table_name="users")
    op.drop_table("users")
