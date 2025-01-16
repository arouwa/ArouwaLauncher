AROUWA Launcher
![image](https://github.com/user-attachments/assets/ef2b55bd-b660-4b69-91cb-0cd9be2596ec)

Overview

The AROUWA Launcher is a customizable launcher application designed for Minecraft. It provides users with an easy-to-use interface for managing their game configurations, accessing news, and managing mods. The launcher features a modern, sleek design with a dark and bluish theme.

Features

Navigation Bar

Menu Button: Opens the main configuration panel where users can set their username and select the Minecraft version.

News Button: Opens the News page to display the latest releases fetched from the Arouwa GitHub Releases.

Menu Page

Username Input: Allows the user to enter their preferred username.

Version Selection: Dropdown menu to select from various Minecraft versions, including Fabric releases.

Start Button: Launches Minecraft with the specified username and version.

Progress Bar: Displays the loading progress during game launch.

News Page

Fetches and displays the latest news and release notes from the Arouwa GitHub Releases.

Provides dynamic updates whenever the news button is clicked.

Mods Management

Open Mods Folder: Opens the mods folder directly from the launcher for quick access.

Mods List: Displays a list of all installed mods in the user's mods folder.

System Requirements

Python 3.8+

Required Libraries:

customtkinter

tkinter

requests

subprocess

os

threading

How to Use

Open the launcher by running the Python script.

Use the navigation bar to toggle between the Menu and News pages.

In the Menu page:

Enter your username in the designated field.

Select your desired Minecraft version from the dropdown.

Click "Start" to launch the game.

In the News page:

View the latest updates fetched from the GitHub repository.

To manage mods:

Click "Open Mods Folder" to access the folder.

View the list of installed mods directly in the launcher.

Customization

Appearance: The launcher supports a modern dark theme with a bluish accent.

Navigation: Easily switch between menu and news functionalities with dedicated buttons.

Troubleshooting

News Not Loading: Ensure you have an active internet connection. The launcher fetches data from GitHub releases.

Game Not Starting: Verify that PortableMC is installed and properly configured.

Mods Not Displayed: Ensure that the mods folder is located in the default Minecraft directory.

Future Enhancements

Improved error handling for network and file operations.

Additional customization options for themes and layout.

Integration with other modding platforms.

License

This project is open-source and available under the MIT License.

For more details, visit the Arouwa GitHub Repository.

