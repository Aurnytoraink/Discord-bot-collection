# Coiffeur

Un bot trop rigolo qui répond `"feur"` lorsque quelqu'un demande `"quoi"` 😂😂🤣🤣🤣🤣

## Comment l'utiliser ?

Rendez vous sur la [page de développeur Discord](https://discord.com/developers/applications). Ensuite créer une application, puis sélectionner le type `bot`, et copier la **clé privé**

Après il vous suffit rendre dans l'onglet `"OAuth2"` et de générer un lien d'invitation avec pour **seule** permission : **écrire un message**

Voilà ! Maintenant il reste plus qu'à héberger le bot sur un serveur Linux de préférence (tmtc c'est le 💯)

Il faudra cependant créer un fichier `config.json` à la racine du dossier, ayant cette gueule:

```json
{
    "token" : "votre clé du bot discord"
}
```