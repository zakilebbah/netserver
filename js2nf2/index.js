const express = require('express')
const bytenode = require('bytenode');
const bodyParser = require('body-parser')
const app = express()
const cors = require("cors");
const port = 3000
app.use(bodyParser.json())
app.use(
    bodyParser.urlencoded({
        extended: true,
    })
)
app.use(cors());

// import setTZ from 'set-tz';
// setTZ('Africa/Algiers');

process.env.TZ = "Africa/Algiers";
// process.env.TZ = "Etc/Universal";

app.get('/', (request, response) => {
    response.json({ info: 'Node.js, Express, and Postgres API' })
})
const db = require('./queries.js')
app.get('/articles', db.getArticlesTest)
app.post('/gps', db.sendGps)
app.post('/insert', db.insert)
app.post('/search_pieces', db.getPieces)
app.post('/count_pieces', db.getPiecesCount)
app.post('/search_articles', db.getArticles)
app.post('/count_articles', db.getArticlesCount)
app.post('/search_tiers', db.getTiers)
app.post('/count_tiers', db.getArticleTiersCount)
app.post('/update', db.update)
app.post('/table_exists', db.tableExists)
app.post('/api-famille', db.getFamilles)
app.post('/api-famille-tiers', db.getFamillesTiers)
app.post('/api-tiers', db.getTiersFromFam)
app.post('/api-all-table', db.getAllTable)
app.post('/api-nbrows', db.getAllTableRows)
app.post('/api-etat-livraison', db.getEtatLivraison)
app.post('/api-item', db.getPieceItems)
app.post('/api-citem', db.getCItems)
app.post('/api-articleItem', db.getArticleItem)
app.post('/api-pieceVersements', db.getPieceVersements)
app.post('/api-tarifsArticle', db.getTarifsArticle)
app.post('/delete', db.deleteFromTable)
app.post('/api-etats', db.getEtats)
app.post('/api-try-connect', db.tryConnect)
app.post('/api-connect', db.connect)
app.post('/api-secure-user', db.getSecureAllofUser1)
app.post('/api-user-exists', db.ifUserExit)
app.post('/api-piece-count', db.getPieceCountLocal)
app.post('/api-piece', db.getOnePiece)
app.post('/api-tiers-place', db.getTiersPlaces)
app.post('/api-specificFamille', db.getSpecificFamilles)
app.post('/api-gen-ref_art', db.generRefArt)
app.post('/api-gen-codeTiers', db.generCodeTiers)
app.post('/api-utilisateur-search', db.getUtilisateur)
app.post('/api-disribution-pieces', db.getDistributionPieces)
app.post('/api-article-ref_art', db.getArticleRefArt)
app.post('/api-contacts', db.getContacts)
app.post('/api-tiers-code', db.getTiersFromCode)
app.post('/api-gps', db.getGps)
app.post('/api-codeFamille', db.getFamilleCode)
app.post('/api-codeFamTiers', db.getFamilleTiersCode)
app.post('/api-article', db.getArticlesSync)
app.post('/api-tiers-sync', db.getArticlesSync)
app.post('/api-famille-refArt', db.getFamilleRefArt)
app.post('/api-parametre', db.getParametre)
app.post('/api-code-site', db.getCodeSite)
app.post('/api-reqselect', db.reqSelect)
app.post('/api-pos-printer', db.printPos)



app.listen(port, () => {
    // console.log(`App running on port ${port}.`)
})