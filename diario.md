# Diario

## 2 novembre 2021

Penso che connexion sia in grado di gestire autonomamente:

- 401: errore di autenticazione
- 400: bad request (SE specifichi benele regole di parsing)
- 500: errore del server

## Domande

## TODO

- **DONE** uniformare gli errori restituiti dal server: fai in modo che Connexion restituisca errori di tipo
  server.model.Error invece di
  connexion.problem https://stackoverflow.com/questions/55053657/how-to-change-error-format-of-all-errors-using-connexion-tornado
- fai in modo che Status rispetti gli standard delle API, quando restituito
- scrivere i casi di test per le API
- si può fare in modo che il server, una volta avviato, indichi il giusto link all'URL di base?
- "KMEs shall provide Web API server functionality to deliver keys to SAEs via HTTPS protocols."
- "Each KME shall have a unique ID (KME ID). A KME ID shall be unique in a QKD network."
- "Each SAE shall have a unique ID (SAE ID). A SAE ID shall be unique in a QKD network."
- "KMEs shall authenticate each request and identify the unique SAE ID of the calling SAE."
- **DONE** "Data in the message body of HTTPS requests from SAE to KME and HTTPS responses from KME to SAE shall be
  encoded in JSON format as per IETF RFC 8259 [6]."
- utilizzare gli slots
- aggiungi una descrizione a ogni classe del Model

## Appunti

- "The SAE making an initial "Get key" request is referred to as the Master SAE for the key(s) returned. An SAE making a
  subsequent "Get key with key IDs" request is called the Slave SAE for the key(s) returned."

## Proposte di miglioramento

- API: bisognerebbe eliminare ripetizioni e ambiguità riferite all'oggeto KeyID. L'ideale sarebbe creare un oggetto
  KeyID con queste due proprietà: key_id, key_id_extension