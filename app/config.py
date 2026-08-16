from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

with open(ROOT / "config" / "profile.yaml", encoding="utf-8") as f:
    PROFILE = yaml.safe_load(f)

