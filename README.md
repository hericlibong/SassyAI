# SassyAI - The Judgy Assistant

## Introduction

SassyAI est un assistant sarcastique conçu pour répondre aux questions avec des remarques piquantes et ironiques. Ce projet a été développé dans le cadre du challenge **Amazon Q Developer - Quack the Code**. L'objectif est de démontrer la capacité à intégrer Amazon Q pour générer des réponses automatiques et sarcastiques tout en offrant une expérience interactive via une interface en ligne de commande (CLI).

## Fonctionnalités

* Réponses sarcastiques sur différents thèmes : général, code, philosophie, nourriture, intelligence artificielle.
* Gestion dynamique des thèmes via Amazon Q pour enrichir le moteur de réponses.
* Session interactive en ligne de commande avec commandes intégrées pour changer de thème, afficher l'aide et quitter la session.
* Effet de réflexion avec messages aléatoires pour simuler une IA en cours de traitement.
* Messages de sortie variés pour garder l'interaction légère et amusante.

## Installation

### Pré-requis

* Python 3.12
* Pipenv

### Installation

```bash
# Cloner le projet
git clone https://github.com/hericlibong/SassyAI.git
cd SassyAI

# Créer l'environnement virtuel
pipenv install

# Activer l'environnement
pipenv shell

# Installer les dépendances
pipenv install -r requirements.txt
```

## Lancement de l'application

Pour lancer l'application, exécutez la commande suivante :

```bash
python sassy_ai/main_cli.py
```

L'application démarre en mode interactif et vous pouvez poser des questions ou changer de thème en cours de session.

## Commandes CLI

* `:help` - Afficher l'aide.
* `:themes` - Voir les thèmes disponibles.
* `:mode <theme>` - Changer de thème.
* `:exit` - Quitter la session.

### Exemples

```bash
python sassy_ai/main_cli.py
```

* Tapez votre question directement :

```
🗨️ [general] > What is the meaning of life?
```

* Changer de thème :

```
🗨️ [general] > :mode code
```

* Quitter l'application :

```
🗨️ [code] > :exit
```

## Tests

Les tests unitaires sont réalisés avec Pytest. Pour les exécuter, lancez :

```bash
pytest --cov=sassy_ai
```

La couverture des tests est affichée en fin d'exécution.

## Personnalisation

Vous pouvez enrichir les thèmes existants ou en ajouter de nouveaux via Amazon Q. Pour ajouter un thème personnalisé, suivez ces étapes :

1. Envoyez un prompt à Amazon Q pour générer des réponses.
2. Intégrez les réponses dans le fichier `responses.py`.
3. Ajoutez le thème dans `main_cli.py` pour le rendre accessible.

## Contribution

Les contributions sont les bienvenues. Si vous avez des idées pour enrichir SassyAI, n'hésitez pas à proposer des Pull Requests ou des Issues.

## License

Ce projet est sous licence MIT.

## Remarques

* Ce projet est conçu pour le challenge Amazon Q Developer - Quack the Code.
* Nous encourageons l'utilisation d'Amazon Q pour enrichir l'expérience de l'assistant.
* L'application est volontairement axée sur l'humour et le sarcasme pour offrir une expérience utilisateur amusante.
