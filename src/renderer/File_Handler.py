from PyQt5.QtWidgets import QFileDialog, QMessageBox

# Project Imports
from managers.Debug_Manager import debug
from managers.Sound_Manager import play_sound_by_name


#===================================================================================================================================
# Helper Functions for Encoding and Decoding Special Characters                                                                  
#===================================================================================================================================
# Convert visually marked-up text to raw bytes with control characters.
def encode_visible_to_bytes(visible_text: str) -> bytes:
    debug.debug("Encoding visible text to bytes (length=%d)", len(visible_text))
    clean_text = visible_text.replace('[LF]\r\n', '[LF]').replace('[LF]\n', '[LF]')
    clean_text = clean_text.replace('[CR]\r\n', '[CR]').replace('[CR]\n', '[CR]')
    
    encoded = (
        clean_text
        .replace('[NUL]', '\x00')
        .replace('[LF]', '\x0A')
        .replace('[CR]', '\x0D')
    ).encode('latin1')
    debug.debug("Finished encoding. Result length=%d", len(encoded))
    return encoded

# Convert raw bytes into visually marked-up text for the editor.
def decode_bytes_to_visible(raw_bytes: bytes) -> str:
    debug.debug("Decoding raw bytes to visible text (length=%d)", len(raw_bytes))
    content = raw_bytes.decode('latin1')
    decoded = (
        content
        .replace('\x00', '[NUL]')
        .replace('\x0A', '[LF]\n')
        .replace('\x0D', '[CR]\n')
    )
    debug.debug("Finished decoding. Result length=%d", len(decoded))
    return decoded

#===================================================================================================================================
#Save Handler for the save button (overwriting and to new file)                                                                    
#===================================================================================================================================
def save_file(parent, text_editor, status_label):
    debug.debug("Save operation triggered...")

    play_sound_by_name("menu_save_popup")

    # Ask user if they want to overwrite or save as a new file
    choice = QMessageBox.question(
        parent,
        "Save Options",
        "Do you want to overwrite the current file?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    debug.debug("Save choice made: %s", "Overwrite" if choice == QMessageBox.Yes else "Save As")

    def save_to_path(path):
        
        # Get text from editor
        visible_text = text_editor.toPlainText()
        debug.debug("Attempting to save file at: %s (length=%d)", path, len(visible_text))
        try:
            # Save with latin1 encoding to preserve bytes exactly
            with open(path, 'wb') as file:
                file.write(encode_visible_to_bytes(visible_text))

            status_label.setText(f'<span style="color: #32CD32; font-weight: bold; font-size: 12pt;">Saved to: {path}</span>')
            play_sound_by_name("menu_select")
            debug.info("File successfully saved: %s", path)
            
            # Refresh bubble view after saving
            if hasattr(parent, "refresh_view"):
                parent.refresh_view()
                debug.debug("Parent view refreshed after save")

        except Exception as e:
            debug.error("Error saving file at %s: %s", path, e)
            play_sound_by_name("menu_failed")
            QMessageBox.critical(parent, "Error", f"Could not save file:\n{e}")
            play_sound_by_name("menu_cancel")

    # Yes: Overwrite current file
    if choice == QMessageBox.Yes:
        if hasattr(parent, 'current_file_path') and parent.current_file_path:
            debug.debug("Overwriting existing file: %s", parent.current_file_path)
            save_to_path(parent.current_file_path)
            play_sound_by_name("menu_save_complete")
        else:
            debug.warning("No current file path to overwrite")
            play_sound_by_name("menu_failed")
            QMessageBox.warning(parent, "No File", "No file is currently open to save to.")
            play_sound_by_name("menu_cancel")
    else:
        # Save As
        debug.debug("Opening Save As dialog")
        play_sound_by_name("menu_select")

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            parent, "Save File As", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            debug.debug("Save As chosen: %s", file_name)
            save_to_path(file_name)
            parent.current_file_path = file_name
            parent.update_window_title()
        else:
            debug.info("Save As cancelled by user")
            play_sound_by_name("menu_cancel")

            status_label.setText('<span style="color:yellow; font-weight:bold; font-size:12pt;">Save cancelled.</span>')

#===================================================================================================================================
#Open Handler for the open button (only looks and opens txt's)                                                                     
#===================================================================================================================================
def open_file_or_folder(parent, text_editor, status_label, box_button, tag_button, icon_button):
    debug.debug("Open operation triggered...")

    play_sound_by_name("menu_open")

    # Popup box for selecting SPM text files
    options = QFileDialog.Options()
    
    file_name, _ = QFileDialog.getOpenFileName(
        parent, "Open SPM Text File", "", "SPM Text Files (*.txt);;All Files (*)")

    if file_name:
        debug.debug("User selected file: %s", file_name)
        try:
            # Only allow txt's to be read!
            if not file_name.lower().endswith('.txt'):
                debug.warning("Rejected file (not .txt): %s", file_name)
                raise ValueError("Only .txt files are supported.")
            
            # Read as binary to preserve special characters
            with open(file_name, "rb") as file:
                raw_bytes = file.read()
            debug.debug("Read %d bytes from file", len(raw_bytes))

            # Control character replacment (visually) 
            visible_content = decode_bytes_to_visible(raw_bytes)

            # Set the content as in text editor
            text_editor.setPlainText(visible_content)
            
            #Other things to do when the file is opened
            status_label.setText(f'<span style="color:#32CD32; font-weight:bold; font-size:12pt;">SPM Text File Opened at: {file_name}</span>')
            box_button.setEnabled(True)
            tag_button.setEnabled(True)
            icon_button.setEnabled(True)
            parent.current_file_path = file_name
            parent.update_window_title()

            # Make the main window rebuild the bubble view if it's enabled
            if hasattr(parent, "refresh_view"):
                debug.debug("Refreshing view for opened file")
                parent.refresh_view()
            
            # Select sound effect for the file that was selected (added a redundancy incase the file cannot be loaded)
            play_sound_by_name("menu_select")
            debug.info("File opened successfully: %s", file_name)

        # The scenario if an incompatible file is picked (basically a lot of fuck you and an appropriate sound effect being played)!
        except Exception as e:

            # Creating the error box explaining the issue
            debug.error("Failed to open file %s: %s", file_name, e)
            error_box = QMessageBox(parent)
            error_box.setIcon(QMessageBox.Critical)
            error_box.setWindowTitle("Error")
            error_box.setText(f"Could not open file:\n{str(e)}")
            error_box.setStandardButtons(QMessageBox.Ok)
            error_box.show()

            # Failed sound effect for opening an invalid file whomp whomp!
            play_sound_by_name("menu_failed")

            # Updating the status label to reflect what happened (in red because it's bad)!
            status_label.setText('<span style="color:red; font-weight:bold; font-size:12pt;">Failed to open file!</span>')
    
    # Scenario if you decide to cancel out of the "Open File" menu.
    else:
        debug.info("Open file operation cancelled by user")
        play_sound_by_name("menu_cancel")

        # Updating the status label to reflect what happened (in yellow because it's neutral)!
        status_label.setText('<span style="color:yellow; font-weight:bold; font-size:12pt;">No file selected.</span>')