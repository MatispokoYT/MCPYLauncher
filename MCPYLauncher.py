from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox
from PySide6.QtCore import Qt
import subprocess
import threading
import minecraft_launcher_lib
import sys
import os

thewarning = ""

# Azure Application info (replace with your actual values)
CLIENT_ID = "YOUR CLIENT ID"
REDIRECT_URL = "YOUR REDIRECT URL"

# Get Minecraft directory and version
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
versions_dir = os.path.join(minecraft_directory, "versions")

if os.path.exists(versions_dir):
    versions = [d for d in os.listdir(versions_dir) if os.path.isdir(os.path.join(versions_dir, d))]
else:
    versions = []
    thewarning = "You need to provide your own versions!"
    print("You need to provide your own versions")


def launchgame():
    version = str(versiondropdown.currentText())
    username = namefield.text().strip()
    if not username:
        thewarning = "Please enter a username!"
        warninglabel.setText(thewarning)
        print("Please enter a username!")
        return
    
    # Offline mode: generate a random UUID
    import uuid
    player_uuid = str(uuid.uuid4()).replace("-", "")
    token = "0"

    thewarning = ""
    warninglabel.setText(thewarning)

    # Ensure Minecraft version is installed
    minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory)

    # Build launch command
    options = {
        "username": username,
        "uuid": player_uuid,
        "token": token,
        "game_directory": minecraft_directory,
        "java_path": javapath.text().strip() or None,  # Optional, will use default if None
        "resolution": {"width": 854, "height": 480},
    }
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)

    # Launch Minecraft
    subprocess.run(minecraft_command, cwd=minecraft_directory)

# Launches the game threaded
def launchgamethreaded():
    threading.Thread(target=launchgame, daemon=True).start()

# Window
app = QApplication([])
window = QWidget()
window.setWindowTitle("MCPY Launcher")
window.setFixedSize(350, 140)

# Widgets
namelabel = QLabel("User Name:")
namefield = QLineEdit()
namefield.setPlaceholderText("Enter your username")

javalabel = QLabel("Java Path (optional):")
javapath = QLineEdit()
javapath.setPlaceholderText("Leave empty to use default Java")

versiondropdown = QComboBox()
versiondropdown.addItems(versions)

playbutton = QPushButton("Play")
playbutton.clicked.connect(launchgamethreaded)

warninglabel = QLabel(thewarning)

# Layout
row1 = QHBoxLayout()
row1.addWidget(namelabel)
row1.addWidget(namefield)

row2 = QHBoxLayout()
row2.addWidget(javalabel)
row2.addWidget(javapath)

row3 = QHBoxLayout()
row3.addWidget(versiondropdown)
row3.addWidget(playbutton)

layout = QVBoxLayout()
layout.addLayout(row1)
layout.addLayout(row2)
layout.addLayout(row3)
layout.addWidget(warninglabel, alignment=Qt.AlignCenter)

# Show the Window

window.setLayout(layout)
window.show()
app.exec()
