# DroneControlPro

**Description**  
This is a software project that allows for the remote management of drones. It was developed for use in civil aviation.

**Functionality**  
- UI for interaction with the drone  
- Flight to specified coordinates  
- Flight according to a previously developed plan  
- Object/person detection using neural networks  
- Video recording from the camera during flight missions  
- Logging and tracking of telemetry during flight missions  

**Installation**  
Download the `requirements.txt` from the repository.

**In the file:**  
- `opencv-python`  
- `pillow`  

**Installation Instructions**  

**Installing Python libraries via pip:**  
- Make sure you have pip installed, then run the following command:  
```bash
pip install -r requirements.txt

Installing ROS and related packages:
These packages should be installed in a ROS environment. For example, installation for Ubuntu can occur like this (assuming you already have a ROS system installed and configured):
sudo apt-get install ros-<your-ros-version>-rospy  
sudo apt-get install ros-<your-ros-version>-sensor-msgs  
sudo apt-get install ros-<your-ros-version>-cv-bridge  
sudo apt-get install ros-<your-ros-version>-clover

Replace <your-ros-version> with your version of ROS (e.g., melodic, noetic, etc.). ```markdown Additional Dependencies:
You may need to install tkinter, but this will depend on your operating system:

On Ubuntu:
sudo apt-get install python3-tk

Remember that using ROS requires having a ROS distribution installed and a configured working environment. Ensure that ROS is correctly installed and initialized in your project.

## Windows

Installing Python libraries via pip:

Make sure pip is installed, then run the following command in the Command Prompt:

pip install opencv-python pillow

Installing tkinter:

On Windows, tkinter may be installed with Python by default. If it is not, try reinstalling Python and ensure that the tkinter option is selected in the installer.
ROS on Windows:

Support for ROS on Windows exists in the latest versions of ROS 2. If you are using ROS 2, follow the official installation instructions.
For ROS 1 on Windows, there is no official support, and solutions may require using Windows Subsystem for Linux (WSL) to simulate a Linux environment.
macOS

Installing Python libraries via pip:

Make sure pip is installed, then run the following command in the terminal:
pip install opencv-python pillow

Installing tkinter:

Typically, tkinter is included in the standard library when installing Python through official distributions. If it is not, consider installing Python via Homebrew to ensure tkinter is included:
brew install python

ROS on macOS:

On macOS, ROS is installed via Homebrew or Docker. Ensure you have Homebrew installed and follow the official instructions for installing ROS 2 via Homebrew. For ROS 1, you can use Docker containers with a Linux-ROS environment installed.
ROS packages (common for Windows and macOS):
If you need to use cv_bridge or other native ROS packages that are not directly available for your platform, consider using Docker environments with suitable Linux distributions where ROS is officially supported.

These steps ensure the installation of necessary libraries and dependencies for developing applications that use the specified libraries on Windows and macOS. Ensure that your system fully meets the requirements of each technology you are using.

Clone the repository:
git clone https://github.com/R0mBab/DroneControlPro

Navigate to the project directory:
cd your-repo-name

Install dependencies:
npm install
