# Juntagrico for Gartenberg

This repository sets up a project to be used with juntagrico.science as hosting.

## Setting up locally to test setup

Install Python 3, and add it to your path (tested with python 3.10, supported by Django 4.0)

## Vorgenommene Anpassungen/Konfigurationen

* Assignment Request und Billing Plugin installiert
* Name, Adresse, Bankverbindungsdaten
* Preis pro Anteilschein
* Link zu Betriebsreglement und Statuten
* Logo

Angepasste Emails
* share_created.txt -> Hinweis das ignorieren mit Probekorb
* depot_changed.txt -> Hinweis das der Änderungswunsch auch per Mail gesendet werden soll

Angepasste Seiten
* signup.html -> Hinweis auf Probekorb
* createsubscription -> select_shares.html -> Hinweis auf Probekorb
* createsubscription -> select_start_date.html -> Hinweis auf Probekorb
* createsubscription -> summary -> Hinweis auf Probekorb
* messages -> unpaid_shares.html -> Hinweis auf Probeabo
* info -> unpaid_shares.html -> Hinweis auf Probeabo

## Linux

### Set your environment variables

The following environment variables can be defined:
| Key | Description | Default Value |
| --------------- | --------------- | --------------- |
| JUNTAGRICO_SECRET_KEY | Used by Django for cryptographic signing | - |
| JUNTAGRICO_DEBUG | Enables the debug mode of the instance (should not be used in production) | False |
| JUNTAGRICO_DATABASE_ENGINE | The database engine to be used | django.db.backends.sqlite3 |
| JUNTAGRICO_DATABASE_NAME | The name of the database | 'gartenberg.db' |
| JUNTAGRICO_DATABASE_USER | The user to connect to the database | - |
| JUNTAGRICO_DATABASE_PASSWORD | The password for the database user | - |
| JUNTAGRICO_DATABASE_HOST | The host where the database is running | - |
| JUNTAGRICO_DATABASE_PORT | The port of the database | False |
| JUNTAGRICO_EMAIL_HOST | The hostname of the mailserver | - |
| JUNTAGRICO_EMAIL_USER | The user to connect to the mailserver | - |
| JUNTAGRICO_EMAIL_PASSWORD | The password of the email user | - |
| JUNTAGRICO_EMAIL_PORT | The port of the mailserver | 25 |
| JUNTAGRICO_EMAIL_TLS | Use a TLS connection to the mailserver | False |
| JUNTAGRICO_EMAIL_SSL | Use a SSL connection to the mailserver | False |

Note: 
 * JUNTAGRICO_EMAIL_TLS and JUNTAGRICO_EMAIL_SSL are mutually exclusive, you can only set one of them to true at any given time.
 * To startup an environment, you only need to define JUNTAGRICO_SECRET_KEY. you can do this as follows under linux `export JUNTAGRICO_SECRET_KEY="password"`

### Run Juntagrico locally

This requires a docker installation.

Execute
```
run.sh
```

It is started on port 8000. A mailtrap is started on port 8025

### Test Cases

* Login with existing user: test/test
* Arbeitseinsatz melden (E-Mail)
* Neuen Einsatz erstellen
* Für Einsatz eintragen (E-Mail)
* Register a new member (2 E-Mails)
* 
