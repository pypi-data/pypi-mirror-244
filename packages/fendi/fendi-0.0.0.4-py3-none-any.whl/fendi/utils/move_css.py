import shutil
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
def move_dirs():
    """
        Moves a CSS file from a source directory to a destination directory.

        This function creates a 'styles' directory if it does not exist and copies a CSS file
        (named 'styles_chat.css') from the source location to the destination location.

        Args:
            None

        Returns:
            None
    """
    if not os.path.exists("styles"):
        os.makedirs("styles")

    css_file = "styles_chat.css"
    css_content = os.path.join(os.path.dirname(Path(__file__).parent.absolute()), f"styles/{css_file}")
    logger.warning(f"------------------- Creating chat style CSS -------------------")
    user_folder_path = "styles/"
    destination_path = os.path.join(user_folder_path, css_file)
    shutil.copy(css_content, destination_path)

# Example usage:
# move_dirs()