import sys
from PyQt5.QtWidgets import QApplication

# Project Imports
from managers.Icon_Manager import program_icon_loader
from frames.Main_Frame import MainFrame
from managers.Theme_Manager import apply_theme_to
from managers.Resource_Manager import ensure_settings_ini_exists
from managers.Debug_Manager import debug
from managers.Theme_Manager import configure_qt_environment

#===================================================================================================================================
# Main Method for Launching the program                                                                                            
#===================================================================================================================================
def main():
    # =====================================================================
    # Enable the debugger if complied with it
    # =====================================================================
    if debug.is_debug():
        debug.info("Debug mode enabled!")
    debug.debug("Starting Flint application...")

    # =====================================================================
    # Configure the app style
    # =====================================================================
    configure_qt_environment()

    # =====================================================================
    # Qt App args adn instance
    # =====================================================================
    debug.debug("Creating QApplication instance...")
    app = QApplication(sys.argv)
    app.setApplicationName("Flint")
    app.setOrganizationName("Luma48")
    debug.info("QApplication instance created successfully!")

    # =====================================================================
    # Icon Handler (OS dependant)
    # =====================================================================
    debug.debug("Ensuring Icon loading for any OS...")
    program_icon_loader(app)

    # =====================================================================
    # Check if the settings file exists
    # =====================================================================
    debug.debug("Ensuring Settings.ini exists...")
    ensure_settings_ini_exists()

    # =====================================================================
    # Applying Theme
    # =====================================================================
    debug.debug("Applying theme to application...")
    apply_theme_to(app)

    # =====================================================================
    # Main Window
    # =====================================================================
    debug.debug("Launching Main Window...")
    window = MainFrame()
    window.show()

    debug.info("Starting Qt event loop!")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()