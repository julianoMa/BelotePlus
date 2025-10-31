# BelotePlus

# Language

- 🇫🇷 [Français](#-français)
    * [Aperçu](#aperçu)
    * [Fonctionnalités](#fonctionnalités)
    * [Installation](#installation)
    * [Conditions d'utilisation](#conditions-dutilisation)
- 🇺🇸 [English](#-english)
    * [Overview](#overview)
    * [Features](#features)
    * [Installation](#installation-1)
    * [Terms of Use](#terms-of-use)

# 🇫🇷 Français

## Aperçu

BelotePlus est une application web locale OpenSource développée avec Flask, conçue pour simplifier l'organisation de concours de belote. Elle permet de créer, gérer et suivre des concours facilement, sans connexion internet ou compétences techniques.
Elle a été conçue à la base pour l'association "Un Ange pour Juliano".

## Fonctionnalités
- Création de tournois (le nombre de tables disponibles et de parties est changeable).
- Enregistrement des joueurs en équipe, numérotation automatique.
- Répartition automatique des équipes sur les tables, pour qu'elles ne jouent jamais deux fois ensemble.
- Calcul des scores et classement.
- Page à vidéo-projeter pour les joueurs, afin de suivre leurs scores en détail et où ils jouent.
- (A VENIR) Modification des scores avant classement en cas d'erreur de frappe

## Installation

### Débutant
Pour les utilisateurs débutants et pas à l'aise avec le développement, vous pouvez télécharger le fichier d'installation `beloteplus-setup.exe` dans la [dernière Release](https://github.com/julianoMa/BelotePlus/releases) et ainsi installer BelotePlus !

### Avancé 
Pour les utilisateurs avancés uniquement, ouvrez un terminal de commande et entrez la suite de commandes ci-dessous pour lancer BelotePlus :
```shell
git clone https://github.com/julianoMa/BelotePlus.git
cd BelotePlus

pip install -r requirements.txt
py app.py
```

## Conditions d'utilisation
Ce projet est distribué sous la license **GNU GPL v3**.
Vous êtes libre de modifier, redistribuer ou utiliser le code, tant que les versions dérivéees restent open source.
Voir le [fichier LICENSE](https://github.com/julianoMa/BelotePlus/blob/main/LICENSE) pour plus d'informations.

# 🇺🇸 English

## Overview

BelotePlus is a local open-source web application built with Flask, designed to simplify the organization of Belote tournaments. It allows you to easily create, manage, and track tournaments — no internet connection or technical skills required.
The project was originally created for the association "Un Ange pour Juliano".

## Features

- Create tournaments (number of tables and rounds can be adjusted)
- Register players in teams with automatic numbering
- Automatically distribute teams across tables so they never play together twice
- Calculate scores and rankings
- A projector-friendly page for players to follow detailed scores and table assignments
- (WIP) Ability to edit scores before ranking in case of typing errors

## Installation

### Beginner
For beginner users who are not familiar with development, you can simply download the installation file `beloteplus-setup.exe` from the [latest Release](https://github.com/julianoMa/BelotePlus/releases) to install BelotePlus easily!

### Advanced
For advanced users, open a command terminal and run the following commands to start BelotePlus :
```shell
git clone https://github.com/julianoMa/BelotePlus.git
cd BelotePlus

pip install -r requirements.txt
py app.py
```

## Terms of Use
This project is distributed under the **GNU GPL v3 license**.
You are free to modify, redistribute, or use the code, as long as derivative versions remain open source.
See the [LICENSE file](https://github.com/julianoMa/BelotePlus/blob/main/LICENSE) for more information.