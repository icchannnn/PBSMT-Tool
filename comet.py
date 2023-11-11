import subprocess
import comet

# Example scoring command
PYTHONPATH = ""
scoring_command = "C:/Users/itcha/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0/LocalCache/local-packages/Python311/site-packages/comet/cli/score.py -s src.fil -t hyp1.en -r ref.en"

# Run the scoring command using subprocess
process = subprocess.Popen(scoring_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

# Check for any errors
if process.returncode != 0:
    print("Error:", error)
else:
    print("Scoring Output:")
    print(output.decode('utf-8'))
