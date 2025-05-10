# SassyAI - The Sarcastic AI Assistant

## Introduction

SassyAI is a sarcastic assistant designed to answer questions with witty, snarky, and ironic remarks. This project was developed as part of the **Amazon Q Developer - Quack the Code** challenge. The goal is to demonstrate the ability to integrate Amazon Q to generate automated and sarcastic responses while providing an interactive experience via a command-line interface (CLI).

## Features

* Sarcastic responses on various themes: general, code, philosophy, food, artificial intelligence, sports, politics, nerd culture, dark humor, and TV series.
* Dynamic theme management via Amazon Q, with automatic integration of new responses and themes.
* Subcategory management for complex themes (e.g., sports, nerd culture, TV series) with accurate detection of context.
* Interactive command-line session with built-in commands to change themes, display help, view stats, and exit the session.
* Visual enhancements using the **Rich** library for colorful and immersive user experience.
* Reflection effect with random messages to simulate AI thinking.
* Various output messages to keep the interaction light and humorous.

## Installation

### Clone the project

```bash
git clone https://github.com/hericlibong/SassyAI.git
cd SassyAI
```

### Create virtual environment

```bash
python3.12 -m venv venv
```

### Activate environment

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Launching the Application

To start the application, run the following command:

```bash
python sassy_ai/main_cli.py
```

or

```bash
cd sassy_ai
python main_cli.py
```

The application will start in interactive mode, allowing you to ask questions or change the theme during the session.

### CLI Commands

* `:help` - Display help.
* `:themes` - List available themes.
* `:mode <theme>` - Change theme.
* `:random` - Switch to a random theme.
* `:stats` - Show theme usage statistics.
* `:exit` - Exit the session.

### Example Usage

```bash
python sassy_ai/main_cli.py
```

* Type your question directly:

```
🗨️ [general] > What is the meaning of life?
```

* Change the theme:

```
🗨️ [general] > :mode code
```

* View stats:

```
🗨️ [code] > :stats
```

* Exit the application:

```
🗨️ [code] > :exit
```

## Logging

### Location

Logs are stored in the following directory:

```
sassy_ai/logs/amazon_q_log.md
```

### Content

The log file contains detailed information about:

- **Prompt submissions:** Records of prompts sent to Amazon Q.
- **Integration details:** Summarizes the automatic updates made to `patterns.json`, `responses.json`, `engine.py`, and `main_cli.py`.
- **Errors:** Tracks any issues during response generation or pattern creation.

### Usage

The logs help to:

- **Track changes:** Understand how themes and responses were integrated.
- **Debug issues:** Identify errors in the automatic integration process.
- **Document updates:** Keep a trace of all improvements and new features.

### Example Log Entry

```
Date: 2025-05-10
Theme: Dark Humor
Status: Success
Details:
   - Responses added to responses.json
   - Patterns updated in patterns.json
   - Theme details integrated in main_cli.py
   - Intent mapping completed in engine.py
```



## Customization

You can enrich existing themes or add new ones via Amazon Q. To add a custom theme, follow these steps:

1. **Send a prompt to Amazon Q** to generate sarcastic responses.

   * Example of a prompt for a new theme "dark humor":

     ```
     Act as a sarcastic AI assistant who embraces dark humor. Generate 5 witty, cynical responses on mortality, existential dread, and human insignificance.
     ```

2. **Integration (automatic)**:

   * Amazon Q will automatically update the `engine.py`, `responses.json`, and `patterns.json` files with the new responses.
   * Subcategories will be dynamically created if necessary (e.g., sports, nerd culture).

3. **Manual Adjustment**:

   * Update the `THEME_DETAILS` dictionary in `main_cli.py` to include the new theme, like this:

     ```python
     THEME_DETAILS = {
         "general": {"prompt": "What's the capital of France?", "color": "cyan", "emoji": "💡"},
         "code": {"prompt": "Write a Python function to sort a list.", "color": "green", "emoji": "💻"},
         "dark_humor": {"prompt": "What happens after we die?", "color": "bright_black", "emoji": "💀"}
     }
     ```

## Tests

Unit tests are performed using Pytest. To run them, execute:

```bash
pytest --cov=sassy_ai
```

Test coverage will be displayed at the end of the run.

### Test Coverage

The current test coverage is approximately 90%. Some edge cases are still under investigation, especially those involving complex subcategory handling.

## Contribution

Contributions are welcome. If you have ideas to enhance SassyAI, feel free to submit Pull Requests or Issues.

## License

This project is licensed under the MIT License.

## Notes

* This project is designed for the Amazon Q Developer - Quack the Code challenge.
* The assistant's sarcastic and mocking responses are intentional to enhance the humorous interaction.
