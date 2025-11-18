# Contributing to PackaStack

First off, thank you for considering contributing to PackaStack! It's people like you that make open source software such a great community.

## How Can I Contribute?

There are many ways to contribute, from writing tutorials or blog posts, improving the documentation, submitting bug reports and feature requests or writing code which can be incorporated into PackaStack itself.

### Reporting Bugs

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/your-username/packastack/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/your-username/packastack/issues/new). Be sure to include a **title and clear description**, as much relevant information as possible, and a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.

### Suggesting Enhancements

- Open a new issue and describe the enhancement you have in mind.
- Include as much detail as you can, including the steps that you imagine you would take if the feature you're requesting existed.

### Pull Requests

- Fork the repository and create your branch from `main`.
- Make sure your code lints and test coverage isn't reduced.
- Issue that pull request!

## Development Setup

To get started with development, you'll need to set up a virtual environment and install the project dependencies. This project uses `uv` for managing the virtual environment and dependencies.

1.  **Install `uv`**

    If you don't have `uv` installed, you can install it with:

    ```bash
    pip install uv
    ```

2.  **Create a virtual environment**

    ```bash
    uv venv
    ```

3.  **Activate the virtual environment**

    ```bash
    source .venv/bin/activate
    ```

4.  **Install dependencies**

    ```bash
    uv pip install -e .[dev]
    ```
    The `[dev]` extra will install development dependencies like `pytest`.

5.  **Run the tests**

    To make sure everything is set up correctly, run the test suite:

    ```bash
    pytest
    ```

## Contribution Workflow
Contributions are welcome! If you'd like to help improve PackaStack, please follow these steps:

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally (`git clone https://github.com/your-username/packastack.git`).
3.  **Create a new branch** for your feature or bug fix (`git checkout -b my-new-feature`).
4.  **Make your changes** and commit them with a clear message.
5.  **Run the tests** to ensure everything is working (`pytest`).
6.  **Push your branch** to your fork (`git push origin my-new-feature`).
7.  **Open a pull request** on the main repository.

We're looking forward to your contributions!