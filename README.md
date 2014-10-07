Viikkoharjoitus 4: MapReduce
----------------------------

MapReduce on suurten datamäärien prosessointiin tarkoitettu ohjelmointimalli.
Google App Engine tarjoaa oman MapReduce-ympäristönsä.

MapReduceen voi tutustua vaikka [tästä](https://cloud.google.com/appengine/docs/python/dataprocessing/).
[Tässä taas](https://cloud.google.com/appengine/docs/python/dataprocessing/mapreduce_library) ohjeita App Enginen mapreduce-kirjaston käyttöön.

App Enginen MapReduce-toteutuksessa on [erilaisia tapoja lukea syötettä ja kirjoittaa tuloksia](https://cloud.google.com/appengine/docs/python/dataprocessing/readers_writers).
Tässä harjoituksessa voi esimerkiksi lukea käyttäen `DatastoreInputReader`:ia ja kirjoittaa tulokset `FileOutputWriter`:illä Cloud Storageen.

## Tehtävä: laske eläinten saalistajien lukumäärä MapReducella
1. [Toisessa viikkoharjoituksessa](https://github.com/Palpo/palpo_viikkoharkka2) tallennettiin eläimiä Datastore-tietokantaan. Voit jatkaa joko omasta 2. harjoituksen toteutuksestasi tai kloonata tämän repositorion, johon on jo valmiiksi lisätty [mapreduce-kirjasto](https://cloud.google.com/appengine/docs/python/dataprocessing/mapreduce_library).
2. Laske MapReducen avulla kunkin eläimen saalistajien lukumäärä. Eli se kuinka monta kertaa kukin eläin esiintyy muiden eläinten saaliseläimenä.
3. Tulosten esittämiseen ei tässä tarvitse keskittyä. Voit katsoa ne vaikka SDK:n [kehityskonsolin]( http://localhost:8000) Blobstore Viewerillä (jos tallensit käyttäen `FileOutputWriter`:iä. Tai App Enginessä ajaessasi [sen kehityskonsolista](https://console.developers.google.com/).

(Oikeasti tietenkään näin pienten datamäärien tapauksessa ei ole mitään järkeä käyttää MapReducea; saman voisi hyvin tehdä tietokantakyselyinkin.)