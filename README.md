<p align="center">
   <img width="512" height="239" alt="logo" src="https://github.com/user-attachments/assets/0e419cf5-c0a2-4858-bf06-010db1bc0cb8"/>
</p>

<p align="center">
   <img src="https://img.shields.io/github/license/julianoMa/BelotePlus">
   <img src="https://img.shields.io/github/v/release/julianoMa/BelotePlus?color=blue">
   <img src="https://img.shields.io/github/commit-activity/t/julianoMa/BelotePlus">
   <img src="https://img.shields.io/github/issues-closed/julianoMa/BelotePlus">
</p>

## Language

- 🇫🇷 [Français](#-français)
    * [Aperçu](#aperçu)
    * [Fonctionnalités](#fonctionnalités)
    * [Installation](#installation)
    * [Conditions d'utilisation](#conditions-dutilisation)
    * [Remerciements](#remerciements)
- 🇺🇸 [English](#-english)
    * [Overview](#overview)
    * [Features](#features)
    * [Installation](#installation-1)
    * [Terms of Use](#terms-of-use)
    * [Thanks](#thanks)

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
- Modification des scores avant classement en cas d'erreur de frappe

## Installation

### Débutant
Pour les utilisateurs débutants et pas à l'aise avec le développement, vous pouvez télécharger le fichier d'installation `beloteplus-setup.exe` dans la [dernière Release](https://github.com/julianoMa/BelotePlus/releases) et ainsi installer BelotePlus !

### Avancé 
Pour les utilisateurs avancés uniquement, ouvrez un terminal de commande et entrez la suite de commandes ci-dessous pour lancer BelotePlus :
```shell
git clone -b stable https://github.com/julianoMa/BelotePlus.git # Pour la dernière version stable, devrait fonctionner normalement
# OU
git clone -b dev https://github.com/julianoMa/BelotePlus.git # Pour la dernière version, des bugs peuvent être présents !
cd BelotePlus

pip install -r requirements.txt
py app.py
```

## Conditions d'utilisation
Ce projet est distribué sous la license **GNU GPL v3**.
Vous êtes libre de modifier, redistribuer ou utiliser le code, tant que les versions dérivéees restent open source.
Voir le [fichier LICENSE](https://github.com/julianoMa/BelotePlus/blob/main/LICENSE) pour plus d'informations.

## Remerciements
Merci à @Tarkhubal et @OmegaStator pour leurs contributions.

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
- Ability to edit scores before ranking in case of typing errors

## Installation

### Beginner
For beginner users who are not familiar with development, you can simply download the installation file `beloteplus-setup.exe` from the [latest Release](https://github.com/julianoMa/BelotePlus/releases) to install BelotePlus easily!

### Advanced
For advanced users, open a command terminal and run the following commands to start BelotePlus :
```shell
git clone -b stable https://github.com/julianoMa/BelotePlus.git # For latest STABLE release, should work properly
# OR
git clone -b dev https://github.com/julianoMa/BelotePlus.git # For the latest release, bugs can take place
cd BelotePlus

pip install -r requirements.txt
py app.py
```

## Terms of Use
This project is distributed under the **GNU GPL v3 license**.
You are free to modify, redistribute, or use the code, as long as derivative versions remain open source.
See the [LICENSE file](https://github.com/julianoMa/BelotePlus/blob/main/LICENSE) for more information.

## Thanks
Thanks to @Tarkhubal and @OmegaStator for their contributions.