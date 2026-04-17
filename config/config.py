import os

# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =========================
# ENV CONFIG
# =========================
BASE_URL = os.getenv("BASE_URL", "https://testing.sourceoptima.com/")

# =========================
# DOWNLOAD PATH
# =========================
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)   

DOWNLOAD_PATH = DOWNLOAD_DIR

# =========================
# TEST DATA PATH
# =========================
TESTDATA_DIR = os.path.join(BASE_DIR, "testdata")

# =========================
# TIMEOUT CONFIG
# =========================
TIMEOUT = int(os.getenv("TIMEOUT", "20"))