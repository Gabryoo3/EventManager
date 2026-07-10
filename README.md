# EventsforIndies
## Obbiettivo
Questo progetto punta a creare una piattaforma per gestire eventi dedicati agli artisti indipendenti, di qualunque genere e categoria.
## Caratteristiche principali
- Registrazione e gestione degli artisti partecipanti (tramite admin)
- Creazione e gestione di eventi
- Gestione delle prenotazioni e dei biglietti per gli eventi
- Registrazione e login degli utenti
- Gestione degli utenti e dei loro profili
- Possibilità di visualizzare gli eventi di un certo organizzatore
- Possibilità di filtrare gli eventi per organizzatore, categoria e città di svolgimento
## Esecuzione locale
### Scaricando il progetto
Lanciare i seguenti comandi:
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

Il database sarà prepopolato di default.


## Ruoli utente
- **Admin**: può creare nuovi artisti, eventi e utenti dalla interfaccia di amministrazione. Attenzione, è l'unico a poter creare gli artisti.
- **Organizzatore**: può gestire i propri eventi, crearne di nuovi e gestire le informazioni del proprio profilo, 
modificando tutti i suoi campi più comuni o la password, ma anche il suo nome da palcoscenico e la categoria principale (non vincolante 
al genere di spettacolo che andrà a tenere). ATTENZIONE: per semplicità, l'organizzatore dell'evento è anche l'artista che terrà lo spettacolo, quindi non è possibile creare eventi con artisti diversi dall'organizzatore stesso.
- **Utente**: può visualizzare gli eventi, prenotare biglietti, gestirli e gestire il proprio profilo. Può cambiare i campi più comuni e il suo indirizzo di casa.
## Elenco utenti divisi per ruolo
 -**Admin**:
    - Username: admin
    - Password: Admin25!
 -**Organizzatore**:
    - Username: organiz1
    - Password: Organizzatore1!
    - Username: organiz2
    - Password: Organizzatore2!
    - Username: organiz3
    - Password: Organizzatore3!
    -**Utente**:
    -Username: user1
    -Password: User1!
    -Username: user2
    -Password: User2!
    -Username: user3
    -Password: User3!

## Piccola Demo
### Home page
- Entrando nella pagina, si vedrà subito un carosello di eventi, gli eventi a posto quasi finito assieme a una piccola storia del sito,
la mission e come diventare organizzatore (mail casuale non collegata a nulla).
- La pagina mostra la navbar, con il tasto lista eventi che elenca tutti gli eventi registrati in ordine cronologico di svolgimento. 
Se entri come organizzatore, quel tasto diventa un dropdown che permette di creare eventi, gestire gli eventi creati da tale organizzatore, 
e comunque visualizzare gli eventi
- Sulla navbar si ha la barra di ricerca, che filtra gli eventi per nome. Nella lista degli eventi si avrà poi un filtro più dettagliato,
per categoria, organizzatore e città di svolgimento. Il filtro è cumulativo, quindi si possono filtrare gli eventi per più campi contemporaneamente.
- Infine, sulla navbar si ha il form per un contatto, che non è collegato a nulla, ma che mostra un messaggio di conferma se compilato correttamente.
E accanto al tasto contatti, si ha il login, che permette di accedere al proprio profilo, o di registrarsi se non si ha un account. La registrazione 
conta solo per gli utenti; gli organizzatori sono creati dall'admin.
- Se si è fatto l'accesso, il tasto login permette agli utenti di gestire il profilo e i biglietti, mentre gli organizzatori solo il profilo, poiché gli
eventi sono gestiti dal primo dropdown incontrato.

### Registrazione e login
- La registrazione è possibile solo per gli utenti, mentre gli organizzatori sono creati dall'admin. La registrazione richiede nome, cognome, username, email, numero di telefono e l'indirizzo di residenza.
- Il login richiede solo username e password
- In caso di errori in registrazione o login, viene mostrato un messaggio di errore in rosso.

### Gestione profilo
- Una volta loggati, si può accedere al proprio profilo e visualizzare le informazioni principali e modificarle attraverso il tasto apposito.
Si può anche cambiare la password di accesso, o tornare all'home page.
- Si può anche caricare un immagine profilo. Se non viene caricata, verrà mostrata la prima lettera del nome utente, un po'come un account google.

### Ricerca eventi
- Gli eventi possono essere filtrati per categoria, organizzatore e città di svolgimento. Si può vedere la lista completa cliccando su Lista eventi nella navbar.

### Dettagli evento
- Cliccando su un evento, si accede alla pagina dei dettagli dell'evento, che mostra tutte le informazioni principali, come titolo, categoria, organizzatore, 
data e ora, luogo, costo del biglietto e una descrizione.
- Solo gli utenti loggati possono prenotare i biglietti, e solo se l'evento non è già esaurito. Se l'evento è esaurito, viene mostrato un messaggio di avviso.
- Un avviso viene mostrato agli organizzatori riguardo l'impossibilità di comprare i biglietti, come agli utenti non loggati, 
che vengono invitati a fare il login per poter prenotare i biglietti.
- L'organizzatore è in grado di modificare i dettagli dell'evento o eliminarlo in toto tramite gli appositi tasti. I biglietti acquistati vengono eliminati automaticamente.

### Organizzatore: gestione eventi
- Cliccando 'I tuoi eventi' nella navbar, l'organizzatore può visualizzare tutti gli eventi che ha creato, modificarli o eliminarli.
- Cliccando 'Crea evento', l'organizzatore può creare un nuovo evento, inserendo tutte le informazioni richieste. Se l'evento viene creato correttamente, viene mostrato un messaggio di conferma.

### Gestione biglietti
- Gli utenti loggati possono visualizzare i biglietti acquistati, raggruppati per evento per una migliore visualizzazione. Il biglietto riporta le stesse info dell'evento, e permette l'eliminazione del biglietto con l'apposito tasto.
- Oltre all'id del db, il biglietto ha anche un codice univoco casuale. Utile per una futura implementazione tramite QR.
- I biglietti sono creati al momento dell'acquisto, e conteggiati dinamicamente all'evento: se un biglietto viene eliminato, il numero di biglietti disponibili per quell'evento aumenta di conseguenza. 








