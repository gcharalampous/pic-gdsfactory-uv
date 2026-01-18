from __future__ import annotations
from pathlib import Path
import gdsfactory as gf
from pic_template.chips.top import top
from pic_template.config import get_config

# Activate the generic PDK (required before creating components)
gf.gpdk.PDK.activate()

def main() -> None:
    config = get_config()
    gds_path = Path(config["gds"]["top"])
    gds_path.parent.mkdir(parents=True, exist_ok=True)
    
    c = top()
    c.write_gds(str(gds_path))
    print(f"Wrote {gds_path}")

if __name__ == "__main__":
    main()
