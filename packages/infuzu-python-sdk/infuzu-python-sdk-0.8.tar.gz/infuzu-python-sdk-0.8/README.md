
# Clockwise Assignment Completion SDK

## Overview

### Description

This SDK provides a set of tools to manage assignments from Clockwise. Primarily, it allows you to fetch, represent, and mark assignments as complete.
### Features
- **Infuzu Authentication**: Represents authentication credentials for Infuzu with methods for signature generation.
- **Assignment Representation**: Represents an Assignment fetched from Clockwise.
- **Complete Assignment Representation**: Represents a completed assignment in Clockwise.
- **Fetch and Complete Assignments**: Functionality to retrieve and mark assignments as complete.
## Setup Instructions
**Install the Package using pip**:

```
pip install infuzu-python-sdk
```

## Usage
### InfuzuCredentials Class
This class is used to represent authentication credentials for Infuzu.
```python
from infuzu.auth import InfuzuCredentials

credentials: InfuzuCredentials = InfuzuCredentials(secret_id="YOUR_SECRET_ID", secret_key="YOUR_SECRET_KEY")
```
Methods & Classmethods:
- `from_file(filepath: str) -> 'InfuzuCredentials'`: Create an `InfuzuCredentials` instance from a `JSON` file.
- `from_dict(data: dict[str, str]) -> 'InfuzuCredentials'`: Create an `InfuzuCredentials` instance from a dictionary.

## Important Note
Please handle your credentials securely and ensure you manage exceptions when dealing with API calls.

## Contributing
As this is an open-source project hosted on GitHub, your contributions and improvements are welcome! Follow these general steps for contributing:

1. **Fork the Repository**: 
Start by forking the main repository to your personal GitHub account.

2. **Clone the Forked Repository**: 
Clone your forked repository to your local machine.

    ```
    git clone https://github.com/Infuzu/InfuzuPythonSDK.git
    ```

3. **Create a New Branch**: 
Before making any changes, create a new branch:

    ```
    git checkout -b feature-name
    ```

4. **Make Your Changes**: 
Implement your features, enhancements, or bug fixes.

5. **Commit & Push**:

    ```
    git add .
    git commit -m "Descriptive commit message about changes"
    git push origin feature-name
    ```
   
6. **Create a Pull Request (PR)**: 
Go to your forked repository on GitHub and click the "New Pull Request" button. Make sure the base fork is the original repository, and the head fork is your repository and branch. Fill out the PR template with the necessary details.

Remember to always be respectful and kind in all interactions with the community. It's all about learning, growing, and helping each other succeed!

## Acknowledgments
Crafted with 💙 by Yidi Sprei for Infuzu. Kudos to all contributors and the expansive Infuzu and `Python` community for encouragement and motivation.

