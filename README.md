
# SassyAI - The Sarcastic AI Assistant

## Introduction

SassyAI is a sarcastic assistant designed to answer questions with snarky and ironic remarks. This project was developed as part of the **Amazon Q Developer - Quack the Code** challenge. The goal is to demonstrate the ability to integrate Amazon Q to generate automated and sarcastic responses while providing an interactive experience via a command-line interface (CLI).

## Features

* Sarcastic responses on different themes: general, code, philosophy, food, artificial intelligence.
* Dynamic theme management via Amazon Q to enrich the response engine.
* Interactive command-line session with built-in commands to change themes, display help and exit the session.
* Reflection effect with random messages to simulate an AI in processing.
* Various output messages to keep the interaction light and fun.


# Installation


## Clone the project
```bash
git clone https://github.com/hericlibong/SassyAI.git
cd SassyAI
```

## Create virtual environment
```bash
python3.12 -m venv venv
```

## Activate environment
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

```bash
# Install dependencies
pip install -r requirements.txt
```


# Launching the Application

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

## Commandes CLI

* `:help` - Afficher l'aide.
* `:themes` - Voir les thèmes disponibles.
* `:mode <theme>` - Changer de thème.
* `:exit` - Quitter la session.

### Exemples

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

* Exit the application:

```
🗨️ [code] > :exit
```

## Tests

Unit tests are performed using Pytest. To run them, execute:

```bash
pytest --cov=sassy_ai
```

Test coverage will be displayed at the end of the run.

## Customization

You can enrich existing themes or add new ones via Amazon Q. To add a custom theme, follow these steps:

1. **Send a prompt to Amazon Q** to generate sarcastic responses.

   * Example of a prompt for a new theme "sports":

     ```
     Act as a sarcastic AI assistant who dislikes sports discussions.  
     Generate 5 different humorous responses for the question: "Who is the best football player?"  
     The tone should be mocking, as if the AI finds sports debates boring or trivial.  
     ```

2. **Integration (automatic)**:

   * Amazon Q will automatically update the `engine.py` file with the new responses.
   * The responses will be added to `self.custom_responses`, and a corresponding regex pattern will be created in `self.custom_patterns`.

3. **Manual Adjustment**:

   * Update the `THEMES` dictionary in `main_cli.py` to include the new theme, like this:

     ```python
     THEMES = {
         "general": "What's the capital of France?",
         "code": "Write a Python function to sort a list.",
         "philosophy": "What is the meaning of life?",
         "food": "What's the best pizza topping?",
         "rogue_ai": "Are you going to turn against humanity?",
         "sports": "Who is the best football player?"
     }
     ```
   * This step ensures that the new theme appears in the interactive CLI interface.


## Contribution

Contributions are welcome. If you have ideas to enhance SassyAI, feel free to submit Pull Requests or Issues.

## License

This project is licensed under the MIT License.

## Notes

* This project is designed for the Amazon Q Developer - Quack the Code challenge.
* We encourage the use of Amazon Q to enrich the assistant experience.
* The application is intentionally focused on humor and sarcasm to provide a fun user experience.
