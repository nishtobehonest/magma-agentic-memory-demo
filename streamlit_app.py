"""Root entrypoint for Streamlit Community Cloud.

The main app lives in ``magma-demo/app.py``. Keeping this wrapper at the
repository root makes default Streamlit deployments work even if the app path
is set to ``streamlit_app.py`` instead of ``magma-demo/app.py``.
"""

from pathlib import Path
import runpy


APP_PATH = Path(__file__).parent / "magma-demo" / "app.py"

runpy.run_path(str(APP_PATH), run_name="__main__")
