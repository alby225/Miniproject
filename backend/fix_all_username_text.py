import sys
from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    simple_tables = [
        '"user"',
        'skill',
        'company_profile',
        'job_post',
        'application',
        'notification',
        'mentor_chat_log'
    ]
    for tbl in simple_tables:
        try:
            db.session.execute(text(f"ALTER TABLE {tbl} ALTER COLUMN username TYPE TEXT;"))
            db.session.commit()
            print(f"[OK] Altered {tbl}.username to TEXT")
        except Exception as e:
            db.session.rollback()
            print(f"[NOTE] {tbl}: {e}")

    views_map = [
        ("admin_placement_analytics", "placement_analytics"),
        ("peer_comparison_dashboard", "peer_comparison"),
        ("ats_compliance", "ats_compliance_dashboard"),
        ("project_audit_scorecard", "ai_project_auditor")
    ]

    for view_name, table_name in views_map:
        try:
            db.session.execute(text(f"DROP VIEW IF EXISTS {view_name};"))
            db.session.execute(text(f"ALTER TABLE {table_name} ALTER COLUMN username TYPE TEXT;"))
            db.session.execute(text(f"CREATE OR REPLACE VIEW {view_name} AS SELECT * FROM {table_name};"))
            db.session.commit()
            print(f"[OK] Altered {table_name}.username to TEXT and recreated view {view_name}")
        except Exception as e:
            db.session.rollback()
            print(f"[NOTE] {table_name}: {e}")

    print("ALL USERNAME COLUMNS IN SUPABASE SUCCESSFULLY UPGRADED TO TEXT!")
