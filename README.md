# Hand Tracking with Mediapipe

Welcome to the Hand Tracking with Mediapipe repository! This project requires certain Python packages to run. Follow the steps below to set up a virtual environment and install the dependencies.

## Prerequisites

- [Python](https://www.python.org/) installed on your machine.

## Getting Started

1. Clone the repository to your local machine:
   ```bash
   git clone git@github.com:rcrtss/handtracking.git
   ```

2. Navigate to the project directory:
   ```bash
   cd handtracking
   ```

3. Create a virtual environment (you can replace `venv` with your preferred virtual environment name):
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install project dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

Now, you have set up a virtual environment and installed the required dependencies. You can proceed to run the project using the provided instructions in the project documentation.

## Additional Notes

- Ensure that you activate the virtual environment (`venv`) before running the project to isolate dependencies.

- If you make changes to the project or install additional packages, update the `requirements.txt` file using:
  ```bash
  pip freeze > requirements.txt
  ```

- To deactivate the virtual environment when you're done:
  ```bash
  deactivate
  ```

## Updates

Applying Low Pass filter and buffering coordinates for drawing detection
* Display both hand and target and looks smooth
* Prints coordinates and timestamp
* 1st order Low Pass filter, clean