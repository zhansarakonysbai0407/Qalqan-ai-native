"""Create initial Qalqan PostgreSQL schema."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("pin_hash", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "trusted_contacts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.UniqueConstraint("user_id", "phone", name="uq_contact_user_phone"),
    )
    op.create_index("ix_trusted_contacts_user_id", "trusted_contacts", ["user_id"])
    op.create_table(
        "sos_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("activated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_sos_events_user_id", "sos_events", ["user_id"])
    op.create_table(
        "location_updates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sos_event_id", sa.Integer(), sa.ForeignKey("sos_events.id", ondelete="CASCADE"), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("accuracy_m", sa.Float(), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_location_updates_sos_event_id", "location_updates", ["sos_event_id"])
    op.create_table(
        "safe_walks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("checked_in_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_safe_walks_user_id", "safe_walks", ["user_id"])

def downgrade():
    op.drop_index("ix_safe_walks_user_id", table_name="safe_walks")
    op.drop_table("safe_walks")
    op.drop_index("ix_location_updates_sos_event_id", table_name="location_updates")
    op.drop_table("location_updates")
    op.drop_index("ix_sos_events_user_id", table_name="sos_events")
    op.drop_table("sos_events")
    op.drop_index("ix_trusted_contacts_user_id", table_name="trusted_contacts")
    op.drop_table("trusted_contacts")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
