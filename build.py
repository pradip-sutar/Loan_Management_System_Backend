import os
import sys
import django
import logging
import signal
import shutil
import io
from pathlib import Path
from datetime import datetime
import traceback

# ---------- Version ----------
APP_VERSION = "1.0.7"  # 🔁 Update this when you change version

# ---------- Path & Logging Setup ----------
IS_FROZEN = getattr(sys, 'frozen', False)
APP_NAME = "Loan_Management_System_Backend"

if IS_FROZEN:
    base_path = Path(sys.executable).parent
    app_data_dir = Path(os.getenv("APPDATA")) / APP_NAME
    os.makedirs(app_data_dir, exist_ok=True)
    os.chdir(base_path)
    sys.path.insert(0, str(base_path))
else:
    base_path = Path(__file__).parent.resolve()
    app_data_dir = base_path
    os.chdir(base_path)
    sys.path.insert(0, str(base_path))

LOG_FILE = app_data_dir / "app.log"
sys.stdout = open(str(LOG_FILE), "a", buffering=1)
sys.stderr = open(str(LOG_FILE), "a", buffering=1)

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)
logger = logging.getLogger(__name__)
logger.info(f"📦 Starting Loan_Management_System_Backend (version {APP_VERSION})")

# ---------- Django Setup ----------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Loan_Management_System_Backend.settings")
django.setup()

# ---------- DB Path Setup ----------
from django.conf import settings
from django.core.management import call_command

db_path = app_data_dir / "db.sqlite3"
version_file = app_data_dir / "db_version.txt"
settings.DATABASES["default"]["NAME"] = str(db_path)

# ---------- Utility ----------
def is_new_version():
    return not version_file.exists() or version_file.read_text().strip() != APP_VERSION

def apply_migrations():
    fake_out = io.StringIO()
    call_command("migrate", interactive=False, stdout=fake_out, stderr=fake_out)
    logger.info("🔄 Migrations applied:\n" + fake_out.getvalue())
    version_file.write_text(APP_VERSION)

# ---------- Initial DB Setup ----------
try:
    if not db_path.exists():
        if IS_FROZEN:
            bundled_template = Path(sys._MEIPASS) / "template_db" / "db.sqlite3"
        else:
            bundled_template = base_path / "template_db" / "db.sqlite3"
        shutil.copy(bundled_template, db_path)
        logger.info("✅ Default DB copied to AppData.")

    if is_new_version():
        apply_migrations()
    else:
        logger.info("⏩ DB up-to-date. No migrations needed.")

except Exception as e:
    logger.error(f"❌ Initialization failed:\n{traceback.format_exc()}")
    sys.exit(1)

# ---------- WSGI Server Startup ----------
def run_wsgi():
    import logging
    from django.core.wsgi import get_wsgi_application
    from wsgiref.simple_server import make_server

    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting WSGI server...")

    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Loan_Management_System_Backend.settings")

        application = get_wsgi_application()
        port = 8004
        with make_server("0.0.0.0", port, application) as httpd:
            logger.info(f"✅ WSGI server running on http://0.0.0.0:{port} ...")
            httpd.serve_forever()
    except Exception as e:
        logger.error(f"❌ Failed to start WSGI server: {e}")
        raise


# ---------- Graceful Shutdown ----------
if __name__ == "__main__":
    def signal_handler(sig, frame):
        logger.info("🛑 Shutting down ASGI server...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        run_wsgi()
    except KeyboardInterrupt:
        logger.info("⛔ Keyboard interrupt received. Exiting.")
    except Exception as e:
        logger.error(f"❌ Main process error: {e}")
