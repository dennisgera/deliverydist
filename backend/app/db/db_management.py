# app/db_management.py
from alembic.config import Config
from alembic import command

def upgrade_database():
    """Upgrade database to latest revision."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

def downgrade_database():
    """Downgrade database by one revision."""
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, "-1")

def reset_database():
    """Reset database to initial state."""
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, "base")
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "upgrade":
            upgrade_database()
        elif action == "downgrade":
            downgrade_database()
        elif action == "reset":
            reset_database()
        else:
            print("Invalid action. Use: upgrade, downgrade, or reset")
    else:
        print("Please specify an action: upgrade, downgrade, or reset")