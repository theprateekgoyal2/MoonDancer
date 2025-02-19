from common.routes import configure_app_routes
from common.models import all_models


def configure_current_application():
    configure_app_routes()
    configure_database()


def configure_database():
    from sql_config import Base, engine
    print("✅ Running Database Configuration...")
    Base.metadata.create_all(engine, checkfirst=True)  # Creates tables if missing
    print("✅ Tables Created (if not exist)")
