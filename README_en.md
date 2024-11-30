Description

This is a software project that allows for remote control of drones. It was developed for use in civil aviation.

Functionality:

UI for interaction with the machine
Flight to specified coordinates
Flight according to a previously developed plan
Object/person detection using neural networks
Video recording from the camera during flight missions
Logging and tracking telemetry during flight missions
Installation

Create (download from the repository) requirements.txt

In the file:

opencv-python
pillow
Installation Instructions

Installing Python Libraries via pip:

Ensure you have pip installed, and run the following command:
bash

Verify

Open In Editor
Edit
Copy code
pip install -r requirements.txt
Installing ROS and related packages:
These packages need to be installed in a ROS environment. For example, installation for Ubuntu can be done as follows (assuming you already have ROS installed and configured):

bash

Verify

Open In Editor
Edit
Copy code
sudo apt-get install ros-<your_version>-rospy  
sudo apt-get install ros-<your_version>-sensor-msgs  
sudo apt-get install ros-<your_version>-cv-bridge  
sudo apt-get install ros-<your_version>-clover  
Replace <your_version> with your version of ROS (e.g., melodic, noetic, etc.).

Additional Dependencies:
You may need to install tkinter, but this will depend on your operating system:

On Ubuntu:
bash

Verify

Open In Editor
Edit
Copy code
sudo apt-get install python3-tk  
Remember that using ROS requires an installed ROS distribution and a configured workspace. Ensure that ROS is correctly installed and initialized in your project.

Windows

Installing Python Libraries via pip:

Ensure pip is installed, and run the following command in the Command Prompt:
bash

Verify

Open In Editor
Edit
Copy code
pip install opencv-python pillow  
Installing tkinter:
In Windows, tkinter may be installed with Python by default. If it is not, try reinstalling Python and ensuring the tkinter option is selected in the installer.

ROS on Windows:
Support for ROS on Windows exists in the latest versions of ROS 2. If you are using ROS 2, follow the official installation instructions.
For ROS 1 on Windows, there is no official support, and you may need to use solutions with Windows Subsystem for Linux (WSL) to simulate a Linux environment.

macOS

Installing Python Libraries via pip:

Ensure pip is installed, and run the following command in the terminal:
bash

Verify

Open In Editor
Edit
Copy code
pip install opencv-python pillow  
Installing tkinter:
Tkinter is usually included in the standard library when installing Python via official distributions. If it is not, consider installing Python via Homebrew to ensure tkinter is available:

bash

Verify

Open In Editor
Edit
Copy code
brew install python  
ROS on macOS:
On macOS, ROS is installed via Homebrew or Docker. Ensure you have Homebrew installed and follow the official instructions for installing ROS 2 via Homebrew. For ROS 1, you can use Docker containers with an installed Linux-ROS environment.

ROS Packages (common for Windows and macOS):
If you need to use cv_bridge or other native ROS packages that are not directly available for your platform, consider using Docker environments with suitable Linux distributions where ROS is officially supported.

These steps ensure the installation of necessary libraries and dependencies for developing applications that use the specified libraries on Windows and macOS. Ensure that your system fully meets the requirements of each technology you are using.

Clone the repository:

bash

Verify

Open In Editor
Edit
Copy code
git clone https://github.com/R0mBab/DroneControlPro  
Navigate to the project directory:

bash

Verify

Open In Editor
Edit
Copy code
cd your-repo-name  
Install dependencies:

bash

Verify

Open In Editor
Edit
Copy code
npm install  
Detailed video about testing and functionality will be available soon.
