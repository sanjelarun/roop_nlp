
# roop_nlp

## Description
The `roop_nlp` project aims to convert given Python code into PySpark code using an NLP model. The main workflow involves extracting loop snippets from Python code, obtaining PySpark API calls using the NLP model, and refactoring the original code with the PySpark equivalents.

## Directory Structure
```
roop_nlp/
|-- src/
|--|--data_models    # stores the data structure related to code translation like lopp information and dataset information
|   |-- extraction/      # Contains code related to extraction of loops from Python code
|   |-- nlp/             # Contains the NLP model and related code to convert loops to PySpark
|   |-- refactoring/     # Code related to refactoring the original Python code with PySpark equivalents
|   |-- testing/         # Scripts and tools to test the refactored code
|-- data/                # Sample Python codes, extracted loops, and other relevant data
|-- tests/               # Unit tests for each module
|-- docs/                # Documentation, papers, and other relevant write-ups
```

## Branching Strategy
To maintain code quality and ensure isolated development, we follow a specific branching strategy:

1. **Main Branch (`main`)**: This is the default branch. It contains the most recent version of the code which is stable and deployable.

2. **Feature Branches**: For each major task or module, a new branch is created. This allows developers to work in isolation, ensuring that the `main` branch always has stable code. Here's how the branches are organized:
   - `feature/extraction`: For the extraction module.
   - `feature/nlp`: For the NLP conversion module.
   - `feature/refactoring`: For the refactoring module.
   - `feature/testing`: For testing the refactored code.

   Once a feature is complete and tested, it's merged back into the `main` branch via a pull request.

3. **Development Branch (`dev`)**: This is an optional branch. It's useful if you want to have a branch where all features are integrated before merging them into the `main` branch.

## How to Contribute
1. Clone the repository:
   ```bash
   git clone [repository_url]
   cd roop_nlp
   ```

2. Create a new branch for the feature/module you're working on. For example, if you're working on the extraction module:
   ```bash
   git checkout -b feature/extraction
   ```

3. After you've made your changes, commit them and push them to the repository:
   ```bash
   git add .
   git commit -m "[DESCRIBE YOUR CHANGES HERE]"
   git push origin [YOUR_BRANCH_NAME]
   ```

4. Once you're ready to merge your changes into the `main` branch, create a pull request via the GitHub/GitLab interface.

5. After a code review, your changes will be merged into the `main` branch.

## Feedback & Collaboration
We encourage team members and collaborators to provide feedback, suggest improvements, and actively contribute to the project. Please ensure you frequently pull the latest changes to stay updated and avoid merge conflicts.
