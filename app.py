import os
import sys

# Add the project root to the Python path so src modules can be imported
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ui.app_layout import main  # noqa: E402

if __name__ == "__main__":
    main()
