# Cosa-Mangio-Oggi
### Idea
Web app in cui gli utenti indovinano cosa hanno mangiato gli altri utenti, è necessario registrarsi per poter giocare. 

Ogni utente ha a disposizione X vite per indovinare, quando indovina verranno aggiunti Y punti al suo account con i quali si possono acquistare lettere ed aiuti 

### Develop
Python, Flask, html, css, javascript, Sql Lite

![LOGO](static/asset/Logo.png) 

---

# Uso

## Sito Web
> https://cosamangio.pythonanywhere.com/

## Endpoints
- /admin
- /admin/dashboard
- /login
- /logout
- /registrati
- /profilo
- /profilo/pubblica
- /indovina/*id*
- /indovina/risposta/*id*
- [work in progress](https://github.com/IsD4n73/Cosa-Mangio-Oggi#to-do)

---
# Dev

## Requisiti
```
pip install Flask
``` 

## Start
Per avviare l'app:
> py app.py

Per resettare le vite e le pubblicazioni dei giocatori: 
> py resetVite.py

## To-Do
- bacheca principale
- pubblicazioni 
- livelli

## Features
- Login utente
- Login admin
- Strumenti admin
- Profilo utente
- Monete
- Vite


## Livelli
> XP

`(lvl/0.07)^2`
> Livello

`0.07 * √XP`

## Colori
> Valori HEX
 
`#d81e5b` > Colore primario ![#d81e5b](https://via.placeholder.com/15/d81e5b/d81e5b.png) 

`#c4d7d1` > Colore secondario ![c4d7d1](https://via.placeholder.com/15/c4d7d1/c4d7d1.png) 
