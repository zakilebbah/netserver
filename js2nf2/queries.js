var configData = {};
const server_version = 3;
var configData00;
const fs = require('fs');
var Pool = require('pg').Pool
var Firebird = require('node-firebird');
var pools = {};
var firebirdOptions = {}
fs.readFile('parametres.json', 'utf8', (err, data) => {
    if (err) {
        console.log(err);
        return;
    }
    configData00 = JSON.parse(data);
    for (const index in configData00) {
        data00 = configData00[index];
        if (data00['PG_BD'].includes('/')) {
            var strs0 = data00['PG_BD'].toString().split('/');
            var str0 = strs0[strs0.length - 1].split('.')[0].toString();
            firebirdOptions[str0] = {
                'host': data00['SERVER'],
                'port': data00['PG_Port'],
                'database': data00['PG_BD'],
                'user': data00['PG_username'],
                'password': data00['PG_passe'],
                'lowercase_keys': false, // set to true to lowercase keys
                'role': null, // default
                'pageSize': 4096, // default when creating database
                'pageSize': 4096, // default when creating database
                'retryConnectionInterval': 1000, // reconnect interval in case of connection drop
                'blobAsText': false, // set to true to get blob as text, only affects blob subtype 1
            }
            configData[str0] = {
                "SERVER": data00['SERVER'],
                "PG_BD": data00['PG_BD'],
                "PG_username": data00['PG_username'],
                "PG_passe": data00['PG_passe'],
                "PG_Port": data00['PG_Port']
            };
            // pools[data00['PG_BD'].split('/').at(-1).split('.')[0]] = new Pool({
            //     user: "postgres",
            //     host: "localhost",
            //     database: "look2",
            //     password: "masterkey2",
            //     port: 5432,
            // });
        } else {
            configData[data00['PG_BD']] = data00;
            pools[data00['PG_BD']] = new Pool({
                user: data00['PG_username'],
                host: data00['SERVER'],
                database: data00['PG_BD'],
                password: data00['PG_passe'],
                port: data00['PG_Port'],
            });
        }
        // console.log(firebirdOptions)
    }
});


function etats_request(etats_values, etat0) {
    var etats_request0 = {
        "JOURNAL_PIECE": {
            "SQL_REQUEST": `
    select $SQLFIELDS
        from PIECE P
        left join LOCAL_TYPE_PIECE TP on ( TP.CODE_TYPE_PIECE = P.CODE_TYPE_PIECE)
        left join  TIERS T ON ( P.CODE_TIERS = T.CODE_TIERS)
        left join  TIERS COM ON (P.CODE_COMMERCIAL = COM.CODE_TIERS)
        left join MODE_REGL MR on (MR.CODE_MODE_REGL = P.CODE_MODE_REGL)
        left join CBANQUE B on (B.CODE_CBANQUE = P.CODE_CBANQUE)
        Where (P.CODE_TYPE_PIECE = '${etats_values['CODE_TYPE_PIECE']}' or cast( '${etats_values["CODE_TYPE_PIECE"]}' as
        varchar(100))= '' )
        and (P.CODE_CBANQUE = '${etats_values['CODE_CBANQUE']}' or cast( '${etats_values['CODE_CBANQUE']}' as
        varchar(100))= '' )
        and (P.CODE_TIERS = '${etats_values['CODE_TIERS']}' or cast( '${etats_values['CODE_TIERS']}' as varchar(100))
        = '' )
        and (P.CODE_MODE_REGL = '${etats_values['CODE_MODE_REGL']}' or cast( '${etats_values['CODE_MODE_REGL']}' as
        varchar(100)) = '' )
        and (P.USERNAME = '${etats_values['USERNAME']}' or cast( '${etats_values['USERNAME']}' as varchar(100)) = '')
        and (P.CODE_DEPOT = '${etats_values['CODE_DEPOT']}' or cast( '${etats_values['CODE_DEPOT']}' as
        varchar(100))= '' )
        and (P.CODE_COMMERCIAL = '${etats_values['CODE_COMMERCIAL']}' or cast( '${etats_values['CODE_COMMERCIAL']}'
        as varchar(100)) = '' )
        and  (P.CODE_SITE = '${etats_values['CODE_SITE']}' or cast( '${etats_values['CODE_SITE']}' as varchar(100)) =
        '')
        and ((P.ANNULEE = ${etats_values['ANNULEE']}) or (cast( '${etats_values['ANNULEE']}' as varchar(100))= '0'))
        and (P.DATEPIECE >= '${etats_values['DATE_MIN']}' and P.DATEPIECE <= '${etats_values['DATE_MAX']}')
    $SQLOFFSETS
    `,
            "SQL_FIELDS": `
        P.CODE_TYPE_PIECE,p.NOPIECE,P.MONTANT03,P.MONTANT06,P.MONTANT07,
        P.MONTANT08,P.MONTANT16,P.MONTANT17,P.MONTANT15,P.TAUX_TVA1, P.TAUX_TVA2, P.TAUX_TVA3,
        P.CODE_TYPE_PIECE CODE_TYPE_PIECE_1,p.CODE_COMMERCIAL,P.AUTRETAXES,
        TP.INTITULE LIB_TYPEPIECE,
        P.NOPIECE,
        P.REF_PIECE, P.DATEPIECE, CAST(P.DATEPIECE AS DATE) DATEPIECE2,
        T.RAISON_SOCIALE, T.CODE_TIERS,
        MR.INTITULE MOD_REGL,
        B.LIBELLE LIB_BANQUE,
        P.REFPAYE,P.REFDOC,
        P.ANNULEE*P.MONTANT*P.COEFF*(-1)  MONTANT,
        P.ANNULEE*P.MONTANTHT*P.COEFF*(-1)  MONTANTHT,
        P.ANNULEE*P.REMISE*P.COEFF*(-1) REMISE,
        P.ANNULEE*P.TVA*P.COEFF*(-1)  TVA,
        P.ANNULEE*P.AUTRETAXES*P.COEFF*(-1) AUTRETAXES,
        P.ANNULEE*P.TIMBRE*P.COEFF*(-1)   TIMBRE,
        P.ANNULEE*P.MONTANTTTC*P.COEFF*(-1)  MONTANTTTC,
        P.ANNULEE*P.MONTANT15*P.COEFF*(-1)  Montant_HT_Brut,
        P.ANNULEE*P.MONTANT16*P.COEFF*(-1)  Remise_Totale,
        P.ANNULEE*(P.MONTANT06+ P.MONTANT07 + P.MONTANT08 )*P.COEFF*(-1) Frais_Totaux, P.USERNAME,
        COALESCE((select sum(V.MONTANT*V.COEFF) from PIECE V where
        V.NOPIECE_O = P.NOPIECE), 0) ENCAISS,
                P.ANNULEE*P.MONTANT*P.COEFF*(-1) + COALESCE((select
        SUM(V.MONTANT*V.COEFF*(-1)) from PIECE V where V.NOPIECE_O = P.NOPIECE),
        0) RAP,
                P.CODE_DEPOT,
                20 COULEUR
                `,
            "SQL_AGGREGATES": `
        sum(P.ANNULEE*P.MONTANT*P.COEFF*(-1)) MONTANT, 
        sum(P.ANNULEE*P.MONTANTHT*P.COEFF*(-1)) MONTANTHT, 
        sum(P.ANNULEE*P.MONTANT16*P.COEFF*(-1)) Remise_Totale, 
        count(*) SQL_COUNT
        `,
            "SQL_ORDER_BY": `
        `
        },
        "JOURNAL_ITEMS": {
            "SQL_REQUEST": ` 
        select $SQLFIELDS
        from 
        spStock('', '${etats_values['CODE_FAMILLE']}', '${etats_values['CODE_DEPOT']}', '1', '${etats_values['DATE_MIN']}', '${etats_values['DATE_MAX']}') s
        left join article A on (s.REF_ART = A.REF_ART)  
        left join Item i on (i.NOITEM = s.NOITEM)
        left join famille F on (A.CODEFAMILLE = F.CODEFAMILLE)
        left join Piece p on (p.NOPIECE = i.NOPIECE)
        left join TIERS t on (t.CODE_TIERS = p.CODE_TIERS)
        left join TIERS com on (com.CODE_TIERS = p.CODE_COMMERCIAL)
        left join LOCAL_TYPE_PIECE tp on ( tp.CODE_TYPE_PIECE =  p.CODE_TYPE_PIECE)
        left join MODE_REGL MR on (MR.CODE_MODE_REGL = P.CODE_MODE_REGL)
        left join CBANQUE B on (B.CODE_CBANQUE = P.CODE_CBANQUE)
        Where 
        (p.CODE_TYPE_PIECE = '${etats_values['CODE_TYPE_PIECE']}' or cast( '${etats_values['CODE_TYPE_PIECE']}' as varchar(100))= '' )and
        (p.CODE_TIERS = '${etats_values['CODE_TIERS']}' or cast( '${etats_values['CODE_TIERS']}' as varchar(100)) = '' ) and
        (p.CODE_COMMERCIAL = '${etats_values['CODE_COMMERCIAL']}' or cast( '${etats_values['CODE_COMMERCIAL']}' as varchar(100)) = '' ) and
        (p.USERNAME = '${etats_values['USERNAME']}' or cast( '${etats_values['USERNAME']}' as varchar(100)) = '') and 
        (p.CODE_CBANQUE = '${etats_values['CODE_CBANQUE']}' or cast( '${etats_values['CODE_CBANQUE']}' as varchar(100))= '' ) and
        ((i.CODE_DEPOT = '${etats_values['CODE_DEPOT']}') or (i.CODE_DEPOT_TR = '${etats_values['CODE_DEPOT']}') or cast( '${etats_values['CODE_DEPOT']}' as varchar(100))= '' ) and
        (p.CODE_MODE_REGL = '${etats_values['CODE_MODE_REGL']}' or cast( '${etats_values['CODE_MODE_REGL']}' as varchar(100)) = '' )  and
        (s.REF_ART = '${etats_values['REF_ART']}' or cast( '${etats_values['REF_ART']}'  as varchar(100)) = '' )
            and  (P.CODE_SITE = '${etats_values['CODE_SITE']}' or cast( '${etats_values['CODE_SITE']}' as varchar(100)) = '') 
        and ((p.ANNULEE = ${etats_values['ANNULEE']}) or (cast( ${etats_values['ANNULEE']} as varchar(100))= '0'))
        and (P.DATEPIECE >= '${etats_values['DATE_MIN']}' and P.DATEPIECE <= '${etats_values['DATE_MAX']}')
        $SQLOFFSETS
`,
            "SQL_FIELDS": `
        a.DESIGNATION, a.CODEFAMILLE, P.REFDOC, p.CODE_COMMERCIAL, A.PRIXACHATHT, 
        p.DATEPIECE, CAST(P.DATEPIECE AS DATE) DATEPIECE2,  p.CODE_TYPE_PIECE, P.CODE_TYPE_PIECE CODE_TYPE_PIECE_1, p.NOPIECE, p.REF_PIECE, p.USERNAME, p.MONTANT03, p.REMISE,
        TP.INTITULE LIB_TYPEPIECE,
        COALESCE(p.annulee, 1)*(i.QTE)*P.COEFF QTE,  
        COALESCE(p.annulee, 1)*(i.QTE*(i.PRIXHT-i.REMISE))*P.COEFF MontantHT,
        COALESCE(p.annulee, 1)*(i.QTE*(A.PRIXACHATHT-i.REMISE))*P.COEFF MONTANT_PRIX_ACHATHT_Article,
        COALESCE(p.annulee, 1)*i.TVA*P.COEFF TVA, 
        COALESCE(p.annulee, 1)*i.REMISE*P.COEFF LIGNE_REMISE,
        COALESCE(p.annulee, 1)*i.MONTANT01 MONTANT01, 
        COALESCE(p.annulee, 1)* i.PRIXTTC*i.QTE*P.COEFF LIGNE_MONTANTTTC, 
        COALESCE(p.annulee, 1)*(i.PRIXHT-i.REMISE)*i.QTE*P.COEFF LIGNE_MONTANTHT,
        COALESCE(p.annulee, 1)*(i.QTE*s.PUMP) LIGNE_MONTANTPUMP, 
        COALESCE(p.annulee, 1)*(i.PRIXTTC -(i.PRIXHT-i.REMISE))*I.QTE*P.COEFF LIGNE_MONTANTTVA, 
        COALESCE(p.annulee, 1)*(I.PRIXHT - I.REMISE)*P.COEFF Ligne_Prix_HT_REMISE,
        F.INTITULE, i.PRIXHT, I.PRIXTTC,  i.CODE_DEPOT, i.CODE_DEPOT_TR, i.MONTANT29,i.NBCOLIS,QTEPARCOLIS,i.CODELOT,i.MONTANT13,
        s.REF_ART,  s.PUMP, s.MARGE,
        s.init_marge, s.init_achat_qte, s.init_achat_val, s.init_vente_qte, s.init_vente_val, s.init_vente_val_pump, s.init_depot_qte, s.init_depot_val, s.init_depot_qte_entree, s.init_depot_qte_sortie,
        s.mouv_marge, s.mouv_achat_qte, s.mouv_achat_val, s.mouv_vente_qte, s.mouv_vente_val,  s.mouv_vente_val_pump, s.mouv_depot_qte, s.mouv_depot_val, s.mouv_depot_qte_entree, s.mouv_depot_qte_sortie,
        s.fin_marge, s.fin_achat_qte, s.fin_achat_val, s.fin_vente_qte, s.fin_vente_val, s.fin_vente_val_pump, s.fin_depot_qte, s.fin_depot_val, s.fin_depot_qte_entree, s.fin_depot_qte_sortie,
        t.RAISON_SOCIALE,  20 COULEUR
        `,
            "SQL_AGGREGATES": `
        sum(COALESCE(p.annulee, 1)*(i.QTE)*P.COEFF) QTE, 
        sum(COALESCE(p.annulee, 1)* i.PRIXTTC*i.QTE*P.COEFF) LIGNE_MONTANTTTC, 
        count(*) SQL_COUNT
    `,
            "SQL_ORDER_BY": `
        order by s.REF_ART, p.DATEPIECE, p.nopiece,  i.NOITEM
    `
        },
        "JOURNAL_ARTICLE": {
            "SQL_REQUEST": `
        select $SQLFIELDS
        from
        spFiche_Stock('${etats_values['REF_ART']}', '${etats_values['CODE_DEPOT']}', '${etats_values['DATE_MIN']}', '${etats_values['DATE_MAX']}') s
        left join item i on (s.NOITEM = i.NOITEM)
        where
        ((s.CODE_TYPE_PIECE = '${etats_values['CODE_TYPE_PIECE']}') or (cast('${etats_values['CODE_TYPE_PIECE']}' as varchar(100))= ''))
        and ((s.ANNULEE = ${etats_values['ANNULEE']}) or (cast(${etats_values['ANNULEE']} as varchar(100))= '0'))
        and (s.DATEPIECE >= '${etats_values['DATE_MIN']}' and s.DATEPIECE <= '${etats_values['DATE_MAX']}')
        $SQLOFFSETS
        `,
            "SQL_FIELDS": `
        s.*, i.CODE_DEPOT, i.CODE_DEPOT_TR    
        `,
            "SQL_AGGREGATES": `
        count(*) SQL_COUNT
        `,
            "SQL_REQUEST_AGGREGATES": `
        with datalist as (select 
            s.*, i.CODE_DEPOT, i.CODE_DEPOT_TR
            from
            spFiche_Stock('${etats_values['REF_ART']}', '${etats_values['CODE_DEPOT']}', '${etats_values['DATE_MIN']}', '${etats_values['DATE_MAX']}') s
            left join item i on (s.NOITEM = i.NOITEM)
            where (s.datepiece = (select max(s2.datepiece) from spFiche_Stock('${etats_values['REF_ART']}', '${etats_values['CODE_DEPOT']}', '${etats_values['DATE_MIN']}', '${etats_values['DATE_MAX']}') s2))
                and ((s.CODE_TYPE_PIECE = '${etats_values['CODE_TYPE_PIECE']}') or (cast('${etats_values['CODE_TYPE_PIECE']}' as varchar(100))= ''))
                and ((s.ANNULEE = ${etats_values['ANNULEE']}) or (cast(${etats_values['ANNULEE']} as varchar(100))= '0'))
                and (s.DATEPIECE >= '${etats_values['DATE_MIN']}' and s.DATEPIECE <= '${etats_values['DATE_MAX']}')
            $LIMIT1)
            select d.fin_depot_qte, d.fin_marge, d.fin_depot_qte_entree, d.fin_depot_qte_sortie, d.pump, (select count(*) from spFiche_Stock('${etats_values['REF_ART']}', '${etats_values['CODE_DEPOT']}', '${etats_values['DATE_MIN']}', '${etats_values['DATE_MAX']}')) SQL_COUNT
            from datalist d
        `,
            "SQL_ORDER_BY": `
        `

        },
        "JOURNAL_SUIVI_ARTICLE": {
            "SQL_REQUEST": ` 
        select $SQLFIELDS
        from spStock('', '${etats_values['CODE_FAMILLE']}', '${etats_values['CODE_DEPOT']}', '0', '${etats_values['DATE_MIN']}', '${etats_values['DATE_MAX']}') s
        join article A on ((s.REF_ART = A.REF_ART) and (s.FIN_DEPOT_QTE >= CAST(${etats_values['QTE_MIN']} as double precision))
        and (s.FIN_DEPOT_QTE <= CAST(${etats_values['QTE_MAX']} as double precision)))
        left join famille F on (F.CODEFAMILLE = A.CODEFAMILLE)
        $SQLOFFSETS
        `,
            "SQL_FIELDS": `
        A.REF_ART, A.DESIGNATION, A.QTEPCARTON, A.DATE_CREATION,
        s.*,
        A.CODEFAMILLE,A.PRIXACHATHT, A.PRIXACHATTTC, A.PRIXVENTEHT, A.PRIXVENTETTC, A.TAUX_TVA, F.INTITULE,
        (s.QTE_TOT*A.PRIXACHATHT) MONTANT_ACHAT_HT, (s.QTE_TOT*A.PRIXVENTEHT) MONTANT_VENTE_HT, A.CODE_UNITE_BASE,
        20 COULEUR
        `,
            "SQL_AGGREGATES": `
            sum(QTE_TOT) QTE_TOT, sum(FIN_DEPOT_VAL) FIN_DEPOT_VAL,sum(FIN_MARGE) FIN_MARGE, 
        count(*) SQL_COUNT
`,
            "SQL_ORDER_BY": `
`

        },
        "JOURNAL_TIERS": {
            "SQL_REQUEST": ` 
        select $SQLFIELDS 
        from PIECE P
        left join  TIERS T ON ( P.CODE_TIERS = T.CODE_TIERS)
        left join  TIERS CS ON ( P.CODE_CAISSIER = CS.CODE_TIERS)
        left join MODE_REGL MR on (MR.CODE_MODE_REGL = P.CODE_MODE_REGL)
        left join CBANQUE B on (B.CODE_CBANQUE = P.CODE_CBANQUE)
        Where (P.CODE_TIERS = '${etats_values['CODE_TIERS']}')
        and  ((P.ANNULEE = cast(COALESCE(${etats_values['ANNULEE']}, '1') as INTEGER)) or (cast( ${etats_values['ANNULEE']} as varchar(100))= '0'))
        and (P.CODE_MODE_REGL = '${etats_values['CODE_MODE_REGL']}' or cast( '${etats_values['CODE_MODE_REGL']}' as varchar(100)) = '' ) 
        and (P.USERNAME = '${etats_values['USERNAME']}' or cast( '${etats_values['USERNAME']}' as varchar(100)) = '')
        and (P.CODE_DEPOT = '${etats_values['CODE_DEPOT']}' or cast( '${etats_values['CODE_DEPOT']}' as varchar(100))= '' )
        and (P.CODE_COMMERCIAL = '${etats_values['CODE_COMMERCIAL']}' or cast( '${etats_values['CODE_COMMERCIAL']}' as varchar(100)) = '' ) 
        and  (P.CODE_SITE = '${etats_values['CODE_SITE']}' or cast( '${etats_values['CODE_SITE']}' as varchar(100)) = '') 
        and (P.CODE_CBANQUE = '${etats_values['CODE_CBANQUE']}' or cast( '${etats_values['CODE_CBANQUE']}' as varchar(100))= '' )
        and (P.DATEPIECE >= '${etats_values['DATE_MIN']}' and P.DATEPIECE <= '${etats_values['DATE_MAX']}')
        $SQLOFFSETS
        `,
            "SQL_FIELDS": `
        P.CODE_TYPE_PIECE, P.NOPIECE, P.CODE_TYPE_PIECE CODE_TYPE_PIECE2, P.NOPIECE_O,
        P.CODE_TYPE_PIECE TYPE_PIECE,P.MONTANT03,P.MONTANT16,P.CHAINE01,P.ANNULEE,
        P.REF_PIECE, 
        P.DATEPIECE,REFDOC,
        T.RAISON_SOCIALE, MR.INTITULE, B.LIBELLE, P.REFPAYE, 
        P.MONTANT*(COALESCE(P.COEFF,0)+COALESCE(P.COEFF_TR,0))*COALESCE(P.ANNULEE, 1) MONTANT,
        P.MONTANTHT*P.COEFF*COALESCE(P.ANNULEE, 1) MONTANTHT,
        P.REMISE*P.COEFF*COALESCE(P.ANNULEE, 1) REMISE,
        P.TVA*P.COEFF*COALESCE(P.ANNULEE, 1) TVA,
        P.AUTRETAXES*P.COEFF*COALESCE(P.ANNULEE, 1) AUTRETAXES,
        P.TIMBRE*P.COEFF*COALESCE(P.ANNULEE, 1) TIMBRE,
        P.MONTANTTTC*P.COEFF*COALESCE(P.ANNULEE, 1) MONTANTTTC,
        P.MONTANTTTC*COALESCE(P.ANNULEE, 1) MONTANTTTC2,
        P.USERNAME,
        cast(0.00 as double precision) ENTREE,
        cast(0.00 as double precision) SORTIE,
        cast(0.00 as double precision) SOLDE,
        COALESCE(P.NOPIECE_O, P.NOPIECE) NOPP,
        20 COULEUR
    `,
            "SQL_AGGREGATES": `
        sum(P.MONTANT*(COALESCE(P.COEFF,0)+COALESCE(P.COEFF_TR,0))*COALESCE(P.ANNULEE, 1)) MONTANT, 
        sum(P.MONTANTHT*P.COEFF*COALESCE(P.ANNULEE, 1)) MONTANTHT, 
        count(*) SQL_COUNT
        `,
            "SQL_ORDER_BY": `
        order by P.DATEPIECE, P.NOPIECE
        `
        },
        "JOURNAL_SUIVI_TIERS": {
            "SQL_REQUEST": ` 
        select $SQLFIELDS
        from spTiersJrn('${etats_values['FAM']}', '${etats_values['DATE_MIN']}', '${etats_values['DATE_MAX']}') sp
        where (sp.SOLDE >= cast(${etats_values['SOLDEMIN']} as double precision)) and (sp.SOLDE <= cast(${etats_values['SOLDEMAX']} as double precision)) 
        and (sp.CHIFFAFF >= cast(${etats_values['CHIFFAFFMIN']} as double precision)) and (sp.CHIFFAFF <= cast(${etats_values['CHIFFAFFMAX']} as double precision))
        $SQLOFFSETS
        `,
            "SQL_FIELDS": `
        sp.*
        `,
            "SQL_AGGREGATES": `
            sum(SOLDE) SOLDE,  sum(CHIFFAFF) CHIFFAFF,
        count(*) SQL_COUNT
    `,
            "SQL_ORDER_BY": `
        order by sp.CODE_TIERS
        `
        },
        "JOURNAL_BANQUE": {
            "SQL_REQUEST": ` 
        select $SQLFIELDS
        from PIECE P
        left join LOCAL_TYPE_PIECE TP on ( TP.CODE_TYPE_PIECE =  P.CODE_TYPE_PIECE)  
        left join  TIERS T ON ( P.CODE_TIERS = T.CODE_TIERS)
        left join MODE_REGL P1 on (P1.CODE_MODE_REGL = P.CODE_MODE_REGL)
        left join CBANQUE B on (B.CODE_CBANQUE = P.CODE_CBANQUE)
        left join CBANQUE B_TR on (B_TR.CODE_CBANQUE = P.CODE_CBANQUE_TR)
        left join PIECE O on (O.NOPIECE = P.NOPIECE_O)
        left join  TIERS DP ON ( P.CODE_AFFAIRE = DP.CODE_TIERS)
        left join  TIERS COM ON (P.CODE_COMMERCIAL = COM.CODE_TIERS)
        Where 
        ((P.CODE_CBANQUE = '${etats_values['CODE_CBANQUE']}') or (P.CODE_CBANQUE_TR = '${etats_values['CODE_CBANQUE']}') or (cast( '${etats_values['CODE_CBANQUE']}' as varchar(100)) = '')) and 
        ( (P.CODE_TYPE_PIECE = '${etats_values['CODE_TYPE_PIECE']}') or (cast( '${etats_values['CODE_TYPE_PIECE']}' as varchar(100))= '')) and 
        (P.CODE_TYPE_PIECE in ('PC_DV_VRS_EN', 'PC_DV_VRS_SO', 'PC_DV_TB', 'PC_DV_DEP', 'PC_DV_SLDTR','PC_DV_RC','PC_DV_PAYE')) and
        ((P.CODE_TIERS = '${etats_values['CODE_TIERS']}')  or (cast('${etats_values['CODE_TIERS']}' as varchar(100))= '')) and
        (P.USERNAME = '${etats_values['USERNAME']}' or cast( '${etats_values['USERNAME']}' as varchar(100)) = '') and
        (((P.MONTANT*Case when P.CODE_CBANQUE_TR = '${etats_values['CODE_CBANQUE']}' then  P.COEFF_TR else  Case when P.CODE_CBANQUE = '${etats_values['CODE_CBANQUE']}' then  P.COEFF else  0 end end) <> 0)  or (cast( '${etats_values['CODE_CBANQUE']}' as varchar(100)) = '')) and 
        (P.CODE_COMMERCIAL = '${etats_values['CODE_COMMERCIAL']}' or cast( '${etats_values['CODE_COMMERCIAL']}' as varchar(100)) = '' ) 
        and (COALESCE(P.ANNULEE, 1) = 1)
        and (P.DATEPIECE >= '${etats_values['DATE_MIN']}' and P.DATEPIECE <= '${etats_values['DATE_MAX']}')
        $SQLOFFSETS
    `,
            "SQL_FIELDS": `
        P.CODE_TYPE_PIECE, 
        P.CODE_TYPE_PIECE CODE_TYPE_PIECE_1,
        TP.INTITULE LIB_TYPEPIECE,
        P.REF_PIECE, 
        P.DATEPIECE,
        P.NOPIECE, 
        P.REFDOC, 
        P.CODE_CBANQUE,
        P.CODE_CBANQUE_TR,
        P.CODE_TIERS,
        p.CODE_COMMERCIAL,
        P.NOPIECE_O O_NOPIECE, 
        O.REF_PIECE O_REF_PIECE, 
        O.CODE_TYPE_PIECE O_TYPE_PIECE, 
        T.RAISON_SOCIALE, 
            B.LIBELLE LIBELLE_BANQUE, 
        B_TR.LIBELLE LIBELLE_BANQUE_TR, 
        P.REFPAYE, 
        P.MONTANT*COALESCE(P.ANNULEE, 1)*Case when P.CODE_CBANQUE_TR = '${etats_values['CODE_CBANQUE']}' then  COALESCE(P.COEFF_TR,0) else  Case when P.CODE_CBANQUE = '${etats_values['CODE_CBANQUE']}' then  COALESCE(P.COEFF, 0) else  (COALESCE(P.COEFF,0) + COALESCE(P.COEFF_TR,0)) end end MONTANT_BANQUE, 
        P.MONTANT*COALESCE(P.ANNULEE, 1)*(COALESCE(P.COEFF,0) + COALESCE(P.COEFF_TR,0)) MONTANT, 
        P.CODE_AFFAIRE, 
        DP.RAISON_SOCIALE NATURE_DEPENSE,
        P.USERNAME, 
        P.CHAINE10,
        P.CODE_MODE_REGL,P1.INTITULE INTITULE_MODE_REG,
        20 COULEUR
        `,
            "SQL_AGGREGATES": `
        sum(P.MONTANT*COALESCE(P.ANNULEE, 1)*(COALESCE(P.COEFF,0) + COALESCE(P.COEFF_TR,0))) MONTANT,
        count(*) SQL_COUNT
    `,
            "SQL_ORDER_BY": `
        order by DATEPIECE            
    `
        },
        "JOURNAL_SUIVI_BANQUE": {
            "SQL_REQUEST": ` 
        select $SQLFIELDS
        from CBANQUE B
        $SQLOFFSETS
        `,
            "SQL_FIELDS": `
        B.CODE_CBANQUE,
        B.LIBELLE, 
        (
            select sum(COALESCE(P.ANNULEE, 1)*
            (Case when P.CODE_CBANQUE=B.CODE_CBANQUE then COALESCE(P.COEFF, 0)*COALESCE(P.MONTANT, 0) else  0 end
            +Case when P.CODE_CBANQUE_TR=B.CODE_CBANQUE then COALESCE(P.COEFF_TR, 0)*COALESCE(P.MONTANT, 0) else  0 end )) 
            from PIECE P
            where 
                (P.CODE_CBANQUE = B.CODE_CBANQUE or P.CODE_CBANQUE_TR = B.CODE_CBANQUE) and 
                (P.CODE_TYPE_PIECE in ('PC_DV_VRS_EN', 'PC_DV_VRS_SO', 'PC_DV_TB', 'PC_DV_DEP', 'PC_DV_SLDTR')) and
                (P.DATEPIECE <= '${etats_values['DATE_MAX']}') and (P.DATEPIECE >= '${etats_values['DATE_MIN']}') 
        ) MONTANT,
        0.0 SOLDE,
        20 COULEUR, 
        0 VISIBLE
        `,
            "SQL_AGGREGATES": `
        count(*) SQL_COUNT
        `,
            "SQL_ORDER_BY": `
        order by B.CODE_CBANQUE            
        `
        },
        "JOURNAL222_ET_REC_FOUR222": {
            "SQL_REQUEST": ` 
        select $SQLFIELDS sum(I.PRIXTTC*COALESCE(P.ANNULEE, 1)*I.QTE) MONTANT, I.REF_ART, A.DESIGNATION
        from item I
            left join PIECE P on (I.NOPIECE = P.NOPIECE)
            left join article A on (I.REF_ART = A.REF_ART)
        where
            (exists (select I2.REF_ART
                    from item I2
                    inner join piece P2 on (P2.NOPIECE = I2.NOPIECE  and P2.CODE_TIERS = '${etats_values['CODE_TIERS']}' and P2.CODE_TYPE_PIECE = 'PC_AC_B')
                    where (I2.REF_ART = I.REF_ART)
                    ))
            and (P.CODE_TYPE_PIECE = 'PC_VE_TIK')
            and (COALESCE(P.ANNULEE, 1) = 1)
            and (P.DATEPIECE >= '${etats_values['DATE_MIN']}') and (P.DATEPIECE <= '${etats_values['DATE_MAX']}')
        group by I.REF_ART, A.DESIGNATION
        $SQLOFFSETS
        `,
            "SQL_FIELDS": `
        `,
            "SQL_AGGREGATES": `
`,
            "SQL_REQUEST_AGGREGATES": `
        with datalist as (
            select sum(I.PRIXTTC*COALESCE(P.ANNULEE, 1)*I.QTE) MONTANT, I.REF_ART, A.DESIGNATION
        from item I
            left join PIECE P on (I.NOPIECE = P.NOPIECE)
            left join article A on (I.REF_ART = A.REF_ART)
        where
        (exists (select I2.REF_ART
            from item I2
                inner join piece P2 on (P2.NOPIECE = I2.NOPIECE  and P2.CODE_TIERS = '${etats_values['CODE_TIERS']}' and P2.CODE_TYPE_PIECE = 'PC_AC_B')
            where (I2.REF_ART = I.REF_ART)
            ))
            and (P.CODE_TYPE_PIECE = 'PC_VE_TIK')
            and (COALESCE(P.ANNULEE, 1) = 1)
            and (P.DATEPIECE >= '${etats_values['DATE_MIN']}') and (P.DATEPIECE <= '${etats_values['DATE_MAX']}')
        group by I.REF_ART, A.DESIGNATION
        )
        select count(*) SQL_COUNT, sum(MONTANT) MONTANT 
        from datalist    
`,

            "SQL_ORDER_BY": `
`

        },
        "JOURNAL_ET_REC_FOUR": {
            "SQL_REQUEST": ` 
            select $SQLFIELDS
            I.REF_ART,A.DESIGNATION,
            (select sum(I2.PRIXTTC*COALESCE(P2.ANNULEE, 1)*I2.QTE) 
                   from ITEM I2
                   left join piece P2 on (P2.NOPIECE = I2.NOPIECE) where (I2.REF_ART = I.REF_ART) and (P2.CODE_TYPE_PIECE = 'PC_VE_TIK')) 
                   MONTANT,
            (select sum(COALESCE(P2.ANNULEE, 1)*I2.QTE) 
                   from ITEM I2
                   left join piece P2 on (P2.NOPIECE = I2.NOPIECE) where (I2.REF_ART = I.REF_ART) and (P2.CODE_TYPE_PIECE = 'PC_VE_TIK')) 
                   QTE_VENDUE,
                   (select sum(COALESCE(P2.ANNULEE, 1)*I2.QTE*(COALESCE(P2.COEFF, 0) + COALESCE(P2.COEFF_TR, 0))) 
                   from ITEM I2
                   left join piece P2 on (P2.NOPIECE = I2.NOPIECE) where (I2.REF_ART = I.REF_ART)) 
                   QTE_TOT
                 
          from item I
            left join PIECE P on (I.NOPIECE = P.NOPIECE)
            left join article A on (I.REF_ART = A.REF_ART)
          where
            (P.CODE_TYPE_PIECE = 'PC_AC_B')
            and (COALESCE(P.ANNULEE, 1) = 1)
            and (P.DATEPIECE >= '${etats_values['DATE_MIN']}') and (P.DATEPIECE <= '${etats_values['DATE_MAX']}')
            and (P.CODE_TIERS = '${etats_values['CODE_TIERS']}')
          group by I.REF_ART, A.DESIGNATION
          $SQLOFFSETS
        `,
            "SQL_FIELDS": `
        `,
            "SQL_AGGREGATES": `
  `,
            "SQL_REQUEST_AGGREGATES": `
            with datalist as (select
               P.CODE_TIERS, I.REF_ART,A.DESIGNATION,
               (select sum(I2.PRIXTTC*COALESCE(P2.ANNULEE, 1)*I2.QTE) 
                      from ITEM I2
                      left join piece P2 on (P2.NOPIECE = I2.NOPIECE) where (I2.REF_ART = I.REF_ART) and (P2.CODE_TYPE_PIECE = 'PC_VE_TIK')) 
                      MONTANT,
               (select sum(COALESCE(P2.ANNULEE, 1)*I2.QTE) 
                      from ITEM I2
                      left join piece P2 on (P2.NOPIECE = I2.NOPIECE) where (I2.REF_ART = I.REF_ART) and (P2.CODE_TYPE_PIECE = 'PC_VE_TIK')) 
                      QTE_VENDUE,
                      (select sum(COALESCE(P2.ANNULEE, 1)*I2.QTE*(COALESCE(P2.COEFF, 0) + COALESCE(P2.COEFF_TR, 0))) 
                      from ITEM I2
                      left join piece P2 on (P2.NOPIECE = I2.NOPIECE) where (I2.REF_ART = I.REF_ART)) 
                      QTE_TOT
                    
             from item I
               left join PIECE P on (I.NOPIECE = P.NOPIECE)
               left join article A on (I.REF_ART = A.REF_ART)
             where
               (P.CODE_TYPE_PIECE = 'PC_AC_B')
               and (COALESCE(P.ANNULEE, 1) = 1)
               and (P.DATEPIECE >= '${etats_values['DATE_MIN']}') and (P.DATEPIECE <= '${etats_values['DATE_MAX']}')
            and (P.CODE_TIERS = '${etats_values['CODE_TIERS']}')
             group by I.REF_ART,P.CODE_TIERS, A.DESIGNATION
             )
             select count(*) SQL_COUNT, sum(MONTANT) MONTANT, sum(QTE_VENDUE) QTE_VENDUE, sum(QTE_TOT) QTE_TOT
                        from datalist 
          `,

            "SQL_ORDER_BY": `
  `

        },
        "JOURNAL_ET_REC_CAISS": {
            "SQL_REQUEST": ` 
            select $SQLFIELDS
            -sum(P.MONTANT*COALESCE(P.ANNULEE, 1)*COALESCE(P.COEFF, 0)) MONTANT, P.CODE_CAISSIER, C.RAISON_SOCIALE
            from PIECE P 
              left join TIERS C on (P.CODE_CAISSIER = C.CODE_TIERS)
            where
            (P.DATEPIECE >= '${etats_values['DATE_MIN']}') and (P.DATEPIECE <= '${etats_values['DATE_MAX']}') and (P.CODE_TYPE_PIECE = 'PC_VE_TIK') 
            and  (P.CODE_SITE = '${etats_values['CODE_SITE']}') 
            and (COALESCE(P.ANNULEE, 1) = 1)
            group by P.CODE_CAISSIER, C.RAISON_SOCIALE
            $SQLOFFSETS
        `,
            "SQL_FIELDS": `
        `,
            "SQL_AGGREGATES": `
        `,
            "SQL_REQUEST_AGGREGATES": `
            with datalist as (
            select 
            -sum(P.MONTANT*COALESCE(P.ANNULEE, 1)*COALESCE(P.COEFF, 0)) MONTANT, P.CODE_CAISSIER, C.RAISON_SOCIALE
            from PIECE P 
              left join TIERS C on (P.CODE_CAISSIER = C.CODE_TIERS)
            where
            (P.DATEPIECE >= '${etats_values['DATE_MIN']}') and (P.DATEPIECE <= '${etats_values['DATE_MAX']}') and (P.CODE_TYPE_PIECE = 'PC_VE_TIK') 
            and  (P.CODE_SITE = '${etats_values['CODE_SITE']}') 
            and (COALESCE(P.ANNULEE, 1) = 1)
            group by P.CODE_CAISSIER, C.RAISON_SOCIALE
            )
            select count(*) SQL_COUNT, sum(MONTANT) MONTANT
            from datalist 
        `,

            "SQL_ORDER_BY": `
`
        },



        "JOURNAL_ET_JRN_REC_J": {
            "SQL_REQUEST": ` 
        with datalist as (
            select 
                            CAST(0.0 as double precision) DEPENSES,
                            CAST(0.0 as double precision) NET,
                            sum(s.marge) MARGE,
                            sum(Case when ((p.code_type_piece = 'PC_VE_B') or (p.code_type_piece = 'PC_VE_F') or (p.code_type_piece = 'PC_VE_TIK1') or (p.code_type_piece = 'PC_VE_TIK') or
                                    (p.code_type_piece = 'PC_VE_FA')or (p.code_type_piece = 'PC_VE_BR')) then 
                                (i.coeff + i.coeff_tr)*i.prixht*i.qte else  0 end) CHIFF_AFF,
                            substr(cast(p.datepiece as varchar(24)), 1, 10) JOUR
                        from
                        spStock('', '${etats_values['CODE_FAMILLE']}', '', '1', '${etats_values['DATE_MIN']}', '${etats_values['DATE_MAX']}') s
                            left join item i on (s.noitem = i.noitem)
                            left join piece p on (p.nopiece = i.nopiece)
                        where 
                            (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}')
                        group by JOUR
                        
                        UNION
                        
                        select
                            sum(-montant*COALESCE(p.ANNULEE, 1)) DEPENSES,
                            CAST(0.0 as double precision) NET,
                            CAST(0.0 as double precision) MARGE,
                            CAST(0.0 as double precision) CHIFF_AFF,
                            substr(cast(p.datepiece as varchar(24)), 1, 10) JOUR
                        from piece p
                        where (code_type_piece = 'PC_DV_DEP') and
                        (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}')
                        group by JOUR
            )
            SELECT $SQLFIELDS DEPENSES, MARGE+DEPENSES NET, MARGE, CHIFF_AFF, JOUR FROM datalist
            order by JOUR
            $SQLOFFSETS
        `,
            "SQL_FIELDS": `
        `,
            "SQL_AGGREGATES": `
`,
            "SQL_REQUEST_AGGREGATES": `
        with datalist as (
            select 
                            CAST(0.0 as double precision) DEPENSES,
                            CAST(0.0 as double precision) NET,
                            sum(s.marge) MARGE,
                            sum(Case when ((p.code_type_piece = 'PC_VE_B') or (p.code_type_piece = 'PC_VE_F') or (p.code_type_piece = 'PC_VE_TIK1') or (p.code_type_piece = 'PC_VE_TIK') or
                                    (p.code_type_piece = 'PC_VE_FA')or (p.code_type_piece = 'PC_VE_BR')) then 
                                (i.coeff + i.coeff_tr)*i.prixht*i.qte else  0 end) CHIFF_AFF,
                            substr(cast(p.datepiece as varchar(24)), 1, 10) JOUR,
                            20 COULEUR
                        from
                        spStock('', '${etats_values['CODE_FAMILLE']}', '', '1', '${etats_values['DATE_MIN']}', '${etats_values['DATE_MAX']}') s
                            left join item i on (s.noitem = i.noitem)
                            left join piece p on (p.nopiece = i.nopiece)
                        where 
                            (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}')
                        group by JOUR
                        
                        UNION
                        
                        select
                            sum(-montant*COALESCE(p.ANNULEE, 1)) DEPENSES,
                            CAST(0.0 as double precision) NET,
                            CAST(0.0 as double precision) MARGE,
                            CAST(0.0 as double precision) CHIFF_AFF,
                            substr(cast(p.datepiece as varchar(24)), 1, 10) JOUR,
                            20 COULEUR
                        from piece p
                        where (code_type_piece = 'PC_DV_DEP') and
                        (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}')
                        group by JOUR
            )
            SELECT 
                sum(DEPENSES) DEPENSES, sum(DEPENSES+MARGE) NET, sum(MARGE) MARGE, sum(CHIFF_AFF) CHIFF_AFF,
                count(*) SQL_COUNT
            FROM datalist
            `,
            "SQL_ORDER_BY": `
        `
        },
        "JOURNAL_ET_JRN_RECAP": {
            "SQL_REQUEST": ` 
        with datalist as (
            (
                        select 
                            CAST(0.0 as double precision) DEPENSES,
                            CAST(0.0 as double precision) NET,
                            sum(s.marge) MARGE,
                            sum(Case when ((p.code_type_piece = 'PC_VE_B') or (p.code_type_piece = 'PC_VE_F') or (p.code_type_piece = 'PC_VE_TIK1') or (p.code_type_piece = 'PC_VE_TIK') or
                                    (p.code_type_piece = 'PC_VE_FA')or (p.code_type_piece = 'PC_VE_BR')) then 
                                (i.coeff + i.coeff_tr)*i.prixht*i.qte else  0 end) CHIFF_AFF,
                            substr(cast(p.datepiece as varchar(24)), 1, 7) MOIS
                        from
                        spStock('', '${etats_values['CODE_FAMILLE']}', '', '1', '${etats_values['DATE_MIN']}', '${etats_values['DATE_MAX']}') s
                            left join item i on (s.noitem = i.noitem)
                            left join piece p on (p.nopiece = i.nopiece and (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}'))
                        where
                            (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}')
                        group by MOIS
                        
                        UNION
                        
                        select
                            sum(-montant*COALESCE(p.ANNULEE, 1)) DEPENSES,
                            CAST(0.0 as double precision) NET,
                            CAST(0.0 as double precision) MARGE,
                            CAST(0.0 as double precision) CHIFF_AFF,
                            substr(cast(p.datepiece as varchar(24)), 1, 7) MOIS
                        from piece p
                        where (code_type_piece = 'PC_DV_DEP') and
                        (datepiece >= '${etats_values['DATE_MIN']}')  and (datepiece <= '${etats_values['DATE_MAX']}')
                        group by MOIS
                        )
            )
            SELECT $SQLFIELDS DEPENSES, MARGE+DEPENSES NET, MARGE, CHIFF_AFF, MOIS FROM datalist
            order by MOIS
            $SQLOFFSETS
        `,
            "SQL_FIELDS": `
        `,
            "SQL_AGGREGATES": `
`,
            "SQL_REQUEST_AGGREGATES": `
        with datalist as (
            (
                        select 
                            CAST(0.0 as double precision) DEPENSES,
                            CAST(0.0 as double precision) NET,
                            sum(s.marge) MARGE,
                            sum(Case when ((p.code_type_piece = 'PC_VE_B') or (p.code_type_piece = 'PC_VE_F') or (p.code_type_piece = 'PC_VE_TIK1') or (p.code_type_piece = 'PC_VE_TIK') or
                                    (p.code_type_piece = 'PC_VE_FA')or (p.code_type_piece = 'PC_VE_BR')) then 
                                (i.coeff + i.coeff_tr)*i.prixht*i.qte else  0 end) CHIFF_AFF,
                            substr(cast(p.datepiece as varchar(24)), 1, 7) MOIS,
                            20 COULEUR
                        from
                        spStock('', '${etats_values['CODE_FAMILLE']}', '', '1', '${etats_values['DATE_MIN']}', '${etats_values['DATE_MAX']}') s
                            left join item i on (s.noitem = i.noitem)
                            left join piece p on (p.nopiece = i.nopiece and (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}'))
                        where (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}')
                        group by MOIS
                        
                        UNION
                        
                        select
                            sum(-montant*COALESCE(p.ANNULEE, 1)) DEPENSES,
                            CAST(0.0 as double precision) NET,
                            CAST(0.0 as double precision) MARGE,
                            CAST(0.0 as double precision) CHIFF_AFF,
                            substr(cast(p.datepiece as varchar(24)), 1, 7) MOIS,
                            20 COULEUR
                        from piece p
                        where (code_type_piece = 'PC_DV_DEP') and
                        (datepiece >= '${etats_values['DATE_MIN']}')  and (datepiece <= '${etats_values['DATE_MAX']}')
                        group by MOIS
                        )
            )
            SELECT 
            sum(DEPENSES) DEPENSES, sum(DEPENSES+MARGE) NET, sum(MARGE) MARGE, sum(CHIFF_AFF) CHIFF_AFF,
            count(*) SQL_COUNT
            FROM datalist
                            `,
            "SQL_ORDER_BY": `
        `
        },

        "JOURNAL_ET_JRN_ALL": {
            "SQL_REQUEST": `
        select $SQLFIELDS 
        (COALESCE ((select 
            sum(Case when ((p.code_type_piece = 'PC_VE_B') or (p.code_type_piece = 'PC_VE_F') or 
                            (p.code_type_piece = 'PC_VE_TIK1') or (p.code_type_piece = 'PC_VE_TIK') or
                            (p.code_type_piece = 'PC_VE_FA')or (p.code_type_piece = 'PC_VE_BR')) 
                then p.MONTANT*(p.COEFF) else  0 end) CHIFF_AFF
            from piece p 
            where (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}')
            ), 0)) CHIFF_AFF,
        (select 
            count(*)
            from item i
            left join piece p on (i.NOPIECE = p.NOPIECE)
            where (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}')
            ) COUNT_ITEMS,
        (select count(*) from piece where code_type_piece = 'PC_VE_B' and
            (datepiece >= '${etats_values['DATE_MIN']}')  and (datepiece <= '${etats_values['DATE_MAX']}')) NUMBER_BON_LIVRAISON,
        (select count(*) from piece where code_type_piece = 'PC_VE_PF' and
            (datepiece >= '${etats_values['DATE_MIN']}')  and (datepiece <= '${etats_values['DATE_MAX']}')) NUMBER_PROFORMA
        from article $LIMIT1
        `,
            "SQL_FIELDS": `
        `,
            "SQL_AGGREGATES": `
`,
            "SQL_REQUEST_AGGREGATES": `
        select 
        (COALESCE ((select 
            sum(Case when ((p.code_type_piece = 'PC_VE_B') or (p.code_type_piece = 'PC_VE_F') or 
                            (p.code_type_piece = 'PC_VE_TIK1') or (p.code_type_piece = 'PC_VE_TIK') or
                            (p.code_type_piece = 'PC_VE_FA')or (p.code_type_piece = 'PC_VE_BR')) 
                then p.MONTANT*(p.COEFF) else  0 end) CHIFF_AFF
            from piece p 
            where (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}')
        ), 0)) CHIFF_AFF,
        (select 
            count(*)
            from item i
            left join piece p on (i.NOPIECE = p.NOPIECE)
            where (p.datepiece >= '${etats_values['DATE_MIN']}')  and (p.datepiece <= '${etats_values['DATE_MAX']}')
            ) COUNT_ITEMS,
        (select count(*) from piece where code_type_piece = 'PC_VE_B' and
            (datepiece >= '${etats_values['DATE_MIN']}')  and (datepiece <= '${etats_values['DATE_MAX']}')) NUMBER_BON_LIVRAISON,
        (select count(*) from piece where code_type_piece = 'PC_VE_PF' and
            (datepiece >= '${etats_values['DATE_MIN']}')  and (datepiece <= '${etats_values['DATE_MAX']}')) NUMBER_PROFORMA
        from article
        $LIMIT1
        
        `,
            "SQL_ORDER_BY": `
        `
        },
    };
    var SQL_FIELDS = etats_request0[etat0]['SQL_FIELDS'];
    var SQL_OFFSETS = etats_request0[etat0]['SQL_ORDER_BY'];
    var LIMIT1 = ' limit 1';
    if (configData[etats_values['BD']]['PG_BD'].includes('/')) {
        SQL_OFFSETS += ` rows ${(parseInt(etats_values['NF3ReportRowsDebut'].toString())+1).toString()} to ${(parseInt(etats_values['NF3ReportRowsDebut'].toString())+50).toString()}`
        LIMIT1 = ' rows 1 to 1'
    } else {
        SQL_OFFSETS += ` offset ${etats_values['NF3ReportRowsDebut']} limit ${etats_values['NF3ReportRowsFin']} `
    }
    if (etats_values['NF3ReportRowsDebut'] == '-1') {
        if (etats_request0[etat0]['SQL_REQUEST_AGGREGATES'] != null) {
            // console.log('SQL AGGREGATES:');
            // console.log(etats_request0[etat0]['SQL_REQUEST_AGGREGATES']);
            return etats_request0[etat0]['SQL_REQUEST_AGGREGATES'].replace('$LIMIT1', LIMIT1);
        } else {
            SQL_OFFSETS = '';
            SQL_FIELDS = etats_request0[etat0]['SQL_AGGREGATES'];
        }
    }
    // console.log(SQL_OFFSETS);
    //let sprintf = require('sprintf-js').sprintf;
    // return sprintf(etats_request0[etat0]['SQL_REQUEST'], SQL_FIELDS);
    var sql0 = etats_request0[etat0]['SQL_REQUEST'].replace('$SQLFIELDS', SQL_FIELDS).replace('$SQLOFFSETS', SQL_OFFSETS).replace('$LIMIT1', LIMIT1);
    // console.log('SQL:');
    // console.log(sql0);
    return sql0;
    // 'I pity the $fool'.replace('$fool', 'fool')
}

var etats_values = {
    'CODE_TYPE_PIECE': '',
    'CODE_CBANQUE': '',
    'CODE_TIERS': '',
    'CODE_MODE_REGL': '',
    'USERNAME': '',
    'CODE_DEPOT': '',
    'CODE_COMMERCIAL': '',
    'CODE_SITE': '',
    'ANNULEE': '',
    'DATE_MIN': '',
    'DATE_MAX': '',
    'NF3ReportRowsDebut': 0,
    'NF3ReportRowsFin': 50
};

function myFunction(p1, p2) {
    return p1 * p2; // The function returns the product of p1 and p2
}
const getArticlesTest = (request, response) => {
    var queryText = "SELECT * FROM Article"
    if (configData[BD]['PG_BD'].includes('/')) {
        queryText += " rows 1 to 6"
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            // console.log(db)
            if (err) {
                // console.log(err.message)
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        // console.log(error.message)
                        response.status(500).send(error.message)
                    } else {
                        // console.log(results.length)
    
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        queryText += " limit 5"
        pools[BD].query(queryText, (error, results) => {
            if (error) {
                response.status(500).send(error.message)
            } else {
                response.status(200).json(results.rows)
            }
        })
    }

}
const sendGps = (request, response) => {
    const {
        BD,
        GPS_ID,
        GPS_DATE,
        GPS_LATITUDE,
        GPS_LONGITUDE,
        GPS_ALTITUDE,
        GPS_ACCURACY,
        GPS_ALTITUDE_ACCURACY,
        GPS_HEADING,
        GPS_SPEED,
        CODE_TIERS,
        ETAT_GPS
    } = request.body
    var queryText = "INSERT INTO gps_positions (GPS_ID, GPS_DATE, GPS_LATITUDE, GPS_LONGITUDE, GPS_ALTITUDE, GPS_ACCURACY, GPS_ALTITUDE_ACCURACY, GPS_HEADING, GPS_SPEED, CODE_TIERS, ETAT_GPS) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)";
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText, [GPS_ID, GPS_DATE, GPS_LATITUDE, GPS_LONGITUDE, GPS_ALTITUDE,
            GPS_ACCURACY, GPS_ALTITUDE_ACCURACY, GPS_HEADING, GPS_SPEED, CODE_TIERS, ETAT_GPS
        ], (error, results) => {
            if (error) {
                // console.log(error)
                response.status(500).send(error.message)
            } else {
                response.status(200).json(results.rows)
            }
        });
    }

}

const getPieces = (request, response) => {
    const {
        BD,
        LB,
        UB,
        DATEMIN,
        DATEMAX,
        CODE_TYPE_PIECE,
        INPUT,
        USERNAME,
        CODE_TIERS,
        COLUMN,
        ORDERBY
    } = request.body
        // console.log(request.body)
    var sqlusername0 = "";
    var column0 = "";
    if (COLUMN == 'RAISON_SOCIALE') {
        column0 = "T." + COLUMN;
    } else {
        column0 = "P." + COLUMN;
    }
    if (USERNAME.toUpperCase() != configData[BD]['PG_username'].toUpperCase()) {
        sqlusername0 = ` ((upper(P.USERNAME) = upper('${USERNAME}')) or (upper(P.CODE_COMMERCIAL) = upper('${CODE_TIERS}'))) and `
    }
    var queryText = `SELECT P.*, T.raison_sociale, C.raison_sociale join_commercial, A.raison_sociale join_nom_affaire
FROM piece P LEFT JOIN tiers T ON T.code_tiers = P.code_tiers
LEFT JOIN tiers C ON C.code_tiers = P.code_commercial
LEFT JOIN tiers A ON A.code_tiers = P.CODE_AFFAIRE
where (P.code_type_piece = '${CODE_TYPE_PIECE}') and 
(P.datepiece >= '${DATEMIN}') and (P.datepiece <= '${DATEMAX}') and
${sqlusername0}
(upper(cast(${column0} as varchar(100))) like '${INPUT}')
order by ${ORDERBY}`;
    //   console.log(configData[BD]['PG_BD'])
    if (configData[BD]['PG_BD'].includes('/')) {
        // console.log(` rows ${(parseInt(LB.toString())+1).toString()} to ${(parseInt(LB.toString())+51).toString()}`)
        queryText += ` rows ${(parseInt(LB.toString())+1).toString()} to ${(parseInt(LB)+50).toString()}`
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                // console.log(err.message)
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        // console.log(error.message)
                        response.status(500).send(error.message)
                    } else {
                        // console.log(results.length)
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        queryText += ` offset ${LB} limit ${UB}`
            // process.env.TZ = 'Etc/Universal'; // UTC +00:00
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                } else {
                    // console.log("success")
                    // console.log('Test getPieces now ' + new Date().toString())
                    // console.log('Test getPieces ' + JSON.stringify(results.rows));
                    response.status(200).json(results.rows)
                }
            })
    }
    // console.log(queryText)


}
const getPiecesCount = (request, response) => {
    const {
        BD,
        LB,
        UB,
        DATEMIN,
        DATEMAX,
        CODE_TYPE_PIECE,
        INPUT,
        USERNAME,
        CODE_TIERS,
        COLUMN
    } = request.body
        // console.log(request.body)
    var sqlusername0 = "";
    var column0 = "";
    if (COLUMN == 'RAISON_SOCIALE') {
        column0 = "T." + COLUMN;
    } else {
        column0 = "P." + COLUMN;
    }
    if (USERNAME.toUpperCase() != configData[BD]['PG_username'].toUpperCase()) {
        sqlusername0 = ` ((upper(P.USERNAME) = upper('${USERNAME}')) or (upper(P.CODE_COMMERCIAL) = upper('${CODE_TIERS}'))) and `
    }
    var queryText = `SELECT count(*) FROM PIECE P INNER JOIN tiers T ON T.code_tiers = P.code_tiers
where (P.code_type_piece = '${CODE_TYPE_PIECE}') and 
(P.datepiece >= '${DATEMIN}') and (P.datepiece <= '${DATEMAX}') and
${sqlusername0}
(upper(cast(${column0} as varchar(100))) like '${INPUT}')`;
    // console.log(queryText)
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            // console.log(db)
            if (err) {
                console.log(err.message)
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    // console.log(results)
                    if (error) {
                        // console.log(error.message)
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            })
    }

}

const insert = (request, response) => {
    const BD = request.body["BD"]
    var columnsList = [];
    var columnsTitles = [];
    var values = ""
    var List$00 = []
    var columnsString = ""
    var count = 1
    var data = JSON.parse(request.body["DATA"])
        // console.log('Test Date2 ' + data['DATEPIECE'].toString());
    for (var i in data) {
        columnsTitles.push(i);
        if (configData[BD]['PG_BD'].includes('/')) {
            List$00.push(`?`);
            if (i.includes('date') || i.includes('DATE')) {
                // columnsList.push(data[i].toString().replaceAll(':', '.').replaceAll('T', ' ').slice(0, -3));
                columnsList.push(data[i].toString().replace(':', '.').replace('T', ' ').slice(0, -3));
            } else {
                columnsList.push(data[i]);
            }
        } else {
            columnsList.push(data[i]);
            List$00.push(`$${count}`);
        }
        count++;
    }
    // console.log('Test Date2 ' + columnsList.toString());
    values = "(" + List$00.join(",") + ")";
    columnsString = "(" + columnsTitles.join(",") + ")";
    var queryText = `INSERT INTO ${request.body["TABLE"]} ${columnsString} VALUES ${values}`;

    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                // console.log(error.message)
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, columnsList, (error, results) => {
                    if (error) {
                        console.log(error.message)
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText, columnsList,
            (error) => {
                if (error) {
                    // console.log(error.message)
                    response.status(500).send(error.message)
                } else {
                    // console.log("success")
                    // console.log('Test insert success: ' + queryText.toString());
                    // console.log('Test insert data: ' + JSON.stringify(columnsList));
                    response.status(200).send("Success")
                }
            });
    }

}
const update = (request, response) => {
    const BD = request.body["BD"]
    var columnsList = [];
    var columnsTitles = [];
    var values = ""
    var idColumn = request.body["ID_COLUMN"]
    var columnsString = ""
    var data = JSON.parse(request.body["DATA"])
    queryTxt = "";
    // console.log(data)
    if (configData[BD]['PG_BD'].includes('/')) {
        for (var i in data) {
            var val00 = '';
            if (typeof data[i] == 'string') {
                if (i.includes('date') || i.includes('DATE')) {
                    // console.log('TEST ' + data[i].replaceAll(':', '.').slice(0, -3));
                    // val00 = `'${data[i].toString().replaceAll(':', '.').replaceAll('T', ' ').slice(0, -3)}'`;
                    val00 = `'${data[i].toString().replace(':', '.').replace('T', ' ').slice(0, -3)}'`;
                } else {
                    val00 = `'${data[i]}'`;
                }

            } else {
                val00 = data[i]
            }
            columnsTitles.push(`${i} = ${val00}`);
        }
        queryTxt = `UPDATE ${request.body["TABLE"]} T SET ${columnsTitles.join(',')} WHERE T.${idColumn} = '${data[idColumn]}'`
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryTxt, (error, results) => {
                    if (error) {
                        console.log(error.message)
                        response.status(500).send(error.message)
    
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        for (var i in data) {

            if (typeof data[i] == 'string') {
                columnsList.push(`'${data[i]}'`);
            } else {
                columnsList.push(data[i]);
            }
            columnsTitles.push(i);
        }
        values = "(" + columnsList.join(",") + ")";
        columnsString = "(" + columnsTitles.join(",") + ")";
        queryTxt = `UPDATE ${request.body["TABLE"]} T SET ${columnsString} = ${values} WHERE T.${idColumn} = '${data[idColumn]}'`
        pools[BD].query(queryTxt,
            (error) => {
                if (error) {
                    // console.log(error.message)
                    response.status(500).send(error.message)
                } else {
                    // console.log('Test update success: ' + queryTxt.toString());
                    response.status(200).send("Success");
                }
            })
    }

}
const deleteFromTable = (request, response) => {
    const BD = request.body["BD"]
    var queryTxt = `DELETE FROM ${request.body["TABLE"]} WHERE ${request.body["ID_COLUMN"]} = '${request.body["ID"]}'`
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryTxt, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryTxt,
            (error) => {
                if (error) {
                    // console.log('Test deleteFromTable ' + queryTxt.toString() + error.message)
                    response.status(500).send(error.message)
                } else {
                    // console.log('Test deleteFromTable ' + queryTxt.toString() + " / success")
                    response.status(200).send("Success")
                }
            })
    }

}
const tableExists = (request, response) => {
    const BD = request.body["BD"]
    var columnsList = [];
    var columnsTitles = [];
    var values = ""
    var List$00 = []
    var columnsString = ""
    var count = 1
    for (var i in request.body["DATA"]) {
        columnsList.push(request.body["DATA"][i]);
        columnsTitles.push(i);
        List$00.push(`$${count}`);
        count++;
    }
    values = "(" + List$00.join(",") + ")";
    columnsString = "(" + columnsTitles.join(",") + ")";
    var queryText = `SELECT count(*) from ${request.body["TABLE"]} WHERE ${request.body["ID_COLUMNS"]} = '${request.body["ID"]}'`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error.message)
                    response.status(500).send(error.message)
                } else {
                    response.status(200).json(results.rows)
                }
            })
    }

}
const getArticles = (request, response) => {
    const {
        BD,
        ALLOW_QTE_TOT,
        ALLOW_PHOTO,
        LB,
        UB,
        CODEFAMILLE,
        SEARCHTEXT,
        _CODE_DEPOT_QTE,
        SEARCHCOLUMN,
        ORDERBY
    } = request.body
        // console.log(request.body['SEARCHCOLUMN'])
    var condEquiv0 = "";
    var mySearchTxt = "'%%'";
    // console.log('Test getArticles INIT!!!');
    if (SEARCHCOLUMN == 'REF_ART') {
        mySearchTxt = "'%" + SEARCHTEXT + "%'"
        condEquiv0 =
            ` or exists (select 1 from EQUIV_CBARRES EC where (EC.REF_ART = A.REF_ART) and (upper(EC.CODE_BARRES) like ${mySearchTxt}))`;
    } else {
        const searchArray = SEARCHTEXT.split(" ");
        if (searchArray.length != 0) {
            mySearchTxt = "";
            // console.log(searchArray);
            for (var i = 0; i < searchArray.length; i++) {
                // console.log(searchArray[i]);
                if (i != 0) {
                    mySearchTxt = mySearchTxt + `and ((upper(cast(${SEARCHCOLUMN} as varchar(100))))) like '%` + searchArray[i] + "%'";
                } else {
                    mySearchTxt = mySearchTxt + "'%" + searchArray[i] + "%'";
                }
                // console.log(mySearchTxt);
            }
            // console.log(mySearchTxt);
        }
    }
    var COD_DEPOT = _CODE_DEPOT_QTE;
    if (COD_DEPOT == '')
        COD_DEPOT = '%';
    if (ALLOW_PHOTO != '1')
        photofield0 = 'null'
    else
        photofield0 = 'A.photo';
    var queryText =
        `
with stockart as
( select ref_art,
    sum( COALESCE(qte, 0) * COALESCE(annulee, 1) * COALESCE(coeff, 0) ) AS qte
    from item i
    where coalesce(i.CODE_DEPOT, '') like  coalesce(cast('${COD_DEPOT}' as varchar(20)) , '')
    group by ref_art ) ,
    stockart_tr as
    ( select ref_art,
    sum( COALESCE(qte, 0) * COALESCE(annulee, 1) * COALESCE(coeff_tr, 0) ) AS qte
    from item i
    where coalesce(i.CODE_DEPOT_TR, '') like  coalesce(cast('${COD_DEPOT}' as varchar(20)) , '')
    group by ref_art )

Select
    A.poids_brut, A.poids_net, A.volume, A.prixventeht, A.prixventettc, A.prixachatttc, A.en_sommeil, A.garantie_mois, A.delais,
    A.taux_tva, A.datedebpromo, A.datefinpromo, A.prixhtpromo, A.prixttcpromo, A.activepromo, A.qtemin, A.dateperemp,
    A.date_creation, A.qtepcarton, A.qtemax, A.ctrlstock, A.volume_brut, A.tarif_p_qte, A.marge, A.boutiq_visible, A.prixachatht,
    A.n_maj_tarif, A.ns$key, A.code_douane, A.code_localisation, A.master_ref_art, A.type_nomenc, A.designation, A.code_barres,
    A.code_nap, A.code_depot, A.code_fourn, A.code_unite_ac, A.code_unite_base, A.code_unite_mp, A.code_unite_pr, A.code_unite_ve,
    A.codefamille, A.detail, A.htmldetail, A.codetaxe1, A.codetaxe2, A.codetaxe3, A.code_compte_ac, A.code_compte_ve,
    A.code_unite_volume, A.code_unite_poids, A.code_barre, A.code_fiscal, A.ref_art, A.qte_format, A.code_methode,
    A.expr_points, A.nopiece,
    ${photofield0} photo,
    t.RAISON_SOCIALE NOM_FOURN, t2.RAISON_SOCIALE LOCALISATION,
    U.INTITULE UNITE_BASE,
    cast(0 as integer) NBRART,
    coalesce( s.QTE, 0) + coalesce(s_tr.QTE,0) QTE
    from
    article A
    join AllF('${CODEFAMILLE}') f on (f.CODE_FAM = A.CODEFAMILLE)
    join famille f0 on (A.codefamille = f0.codefamille)
    left join UNITE U on (U.CODE_UNITE = A.CODE_UNITE_BASE)
    left join TIERS t on (A.CODE_FOURN = t.CODE_TIERS)
    left join TIERS t2 on (A.CODE_LOCALISATION = t2.CODE_TIERS)
    left join stockart s on (s.ref_art = a.ref_art)
    left join stockart_tr s_tr on (s_tr.ref_art = a.ref_art)
    where ((upper(cast(A.${SEARCHCOLUMN} as varchar(100))) like ${mySearchTxt}) 
    ${condEquiv0}) ORDER BY ${ORDERBY}`;
    if (configData[BD]['PG_BD'].includes('/')) {
        queryText += ` rows ${(parseInt(LB.toString())+1).toString()} to ${(parseInt(LB)+50).toString()}`
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                console.log(error.message)
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        console.log(error.message)
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        queryText += ` offset ${LB} limit ${UB}`;
        // console.log('Test getArticles SQL: ' + queryText);
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    console.log(error)
                    response.status(500).send(error.message)
                }
                // // console.log("success")
                else {
                    // console.log('Test getArticles ' + JSON.stringify(results.rows));
                    response.status(200).json(results.rows)
                }
            })
    }

}

const getArticlesCount = (request, response) => {
    const {
        BD,
        ALLOW_QTE_TOT,
        ALLOW_PHOTO,
        CODEFAMILLE,
        SEARCHTEXT,
        _CODE_DEPOT_QTE,
        SEARCHCOLUMN,
    } = request.body
        // console.log(request.body)
    var queryText = "";
    var condEquiv0 = "";
    if (SEARCHCOLUMN == 'REF_ART') {
        condEquiv0 =
            ` or exists (select 1 from EQUIV_CBARRES EC where (EC.REF_ART = A.REF_ART) and (upper(EC.CODE_BARRES) like '${SEARCHTEXT}'))`;
    }
    //if (ALLOW_QTE_TOT != '1') 
    {
        queryText = `
    SELECT count(A.REF_ART) FROM ARTICLE A
    join AllF('${CODEFAMILLE}') f on (f.CODE_FAM = A.CODEFAMILLE)
    where ((upper(cast(${SEARCHCOLUMN} as varchar(100))) like '${SEARCHTEXT}') 
        ${condEquiv0})`
    }
    // else {
    //     var str1 = '';
    //     if (_CODE_DEPOT_QTE == '') {
    //         str1 = ' left join stockart S on (S.ref_art = A.ref_art) ';

    //     } else {
    //         str1 =
    //             ` left join stockartdep S on (S.ref_art = A.ref_art) and (S.code_depot = '${_CODE_DEPOT_QTE}') `;
    //     }
    //     queryText = ` SELECT count(A.*) FROM ARTICLE A ${str1} 
    //   join AllF('${CODEFAMILLE}') f on (f.CODE_FAM = A.CODEFAMILLE)
    //   where ((upper(cast(A.${SEARCHCOLUMN} as varchar(100))) like '${SEARCHTEXT}') 
    //   ${condEquiv0})`;
    // }
    // console.log(queryText)
    // console.log('Test getArticlesCount ' + queryText.toString());
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                console.log(error.message)
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        // console.log("TEST getArticlesCount")
                        console.log(error.message)
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log('Test getArticlesCount ' + error.message.toString());
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    // console.log('Test getArticlesCount ' + JSON.stringify(results.rows));
                    response.status(200).json(results.rows)
                }
            })
    }

}


const getTiers = (request, response) => {
    const {
        BD,
        LB,
        UB,
        CODEFAMTIERS,
        SEARCHTEXT,
        SEARCHCOLUMN,
        ORDERBY,
        ALLOW_SOLDE_TOT
    } = request.body
        // console.log(request.body)
    var queryText = "";
    var mySearchTxt = "'%%'";
    const searchArray = SEARCHTEXT.split(" ");
    if (searchArray.length != 0) {
        mySearchTxt = "";
        // console.log(searchArray);
        for (var i = 0; i < searchArray.length; i++) {
            // console.log(searchArray[i]);
            if (i != 0) {
                mySearchTxt = mySearchTxt + `and ((upper(cast(${SEARCHCOLUMN} as varchar(100))))) like '%` + searchArray[i] + "%'";
            } else {
                mySearchTxt = mySearchTxt + "'%" + searchArray[i] + "%'";
            }
            // console.log(mySearchTxt);
        }
        // console.log(mySearchTxt);
    }
    var NF3CALC_AGGREG;
    if (ALLOW_SOLDE_TOT == '1') {
        NF3CALC_AGGREG = '1';
    } else {
        NF3CALC_AGGREG = '0';
    }

    queryText = `
Select
CASE
    WHEN '${NF3CALC_AGGREG}' = 1 THEN
    COALESCE(
    (select sum(coalesce(p0.montant, 0)*COALESCE(p0.annulee, 1)*(coalesce(p0.COEFF, 0) + coalesce(p0.COEFF_TR, 0))) from piece p0 where p0.code_tiers = T.code_tiers)
    , 0)
    ELSE cast(0.00 as DOUBLE PRECISION)
END SOLDE_TOT,
CASE
    WHEN '${NF3CALC_AGGREG}' = 1 THEN
    COALESCE(
        (select sum( case when p0.CODE_FIDELITE = '' then 0 else 1 end * coalesce(p0.POINTS_GAGNES, 0)*COALESCE(p0.annulee, 1)) from piece p0 where p0.code_tiers = T.code_tiers)
        , 0)
    ELSE cast(0.00 as DOUBLE PRECISION)
END POINTS_GAGNES,
T.*, u0.username
from TIERS T
    join AllC('${CODEFAMTIERS}') f on (f.CODE_FAM = T.CODE_FAM_TIERS)
    left join utilisateurs u0 on (u0.code_tiers = T.code_tiers)
where 
    (upper(cast(T.${SEARCHCOLUMN} as varchar(100))) like ${mySearchTxt}) order by ${ORDERBY}`;
    // console.log(queryText)
    if (configData[BD]['PG_BD'].includes('/')) {
        queryText += ` rows ${(parseInt(LB.toString())+1).toString()} to ${(parseInt(LB)+50).toString()};`;
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        console.log(error.message)
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        queryText += ` offset ${LB} limit ${UB};`
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}
const getArticleTiersCount = (request, response) => {
    const {
        BD,
        CODEFAMTIERS,
        SEARCHTEXT,
        SEARCHCOLUMN,
        ALLOW_SOLDE_TOT
    } = request.body
        // console.log(request.body)
    var queryText = "";
    var mySearchTxt = "'%%'";
    const searchArray = SEARCHTEXT.split(" ");
    if (searchArray.length != 0) {
        mySearchTxt = "";
        // console.log(searchArray);
        for (var i = 0; i < searchArray.length; i++) {
            // console.log(searchArray[i]);
            if (i != 0) {
                mySearchTxt = mySearchTxt + ` and((upper(cast(${SEARCHCOLUMN}
        as varchar(100))))) like '%` + searchArray[i] + "%'";
            } else {
                mySearchTxt = mySearchTxt + "'%" + searchArray[i] + "%'";
            }
            // console.log(mySearchTxt);
        }
        // console.log(mySearchTxt);
    }
    // if (ALLOW_SOLDE_TOT != '1') {
    queryText = `
    SELECT count(*)
    FROM TIERS T 
    join AllC('${CODEFAMTIERS}') f on (f.CODE_FAM = T.CODE_FAM_TIERS)
    where 
        (upper(cast(T.${SEARCHCOLUMN} as varchar(100))) like ${mySearchTxt})`;
    // } else {
    //     queryText = `
    //   SELECT count(*)
    //     FROM TIERS T 
    //     left join soldtiers S on (S.code_tiers = T.code_tiers) 
    //     join AllC('${CODEFAMTIERS}') f on (f.CODE_FAM = T.CODE_FAM_TIERS)
    //     where 
    //       (upper(cast(T.${SEARCHCOLUMN} as varchar(100))) like ${mySearchTxt})`;
    // }
    // console.log(queryText)
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}
const getFamilles = (request, response) => {
    const { BD, } = request.body
    var queryText = "SELECT F.* FROM FAMILLE F ORDER BY INTITULE";
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText, (error, results) => {
            if (error) {
                response.status(500).send(error.message)
            } else {
                response.status(200).json(results.rows)
            }
        });
    }

}
const getFamilleCode = (request, response) => {
    const {
        BD,
        CODEFAMILLE
    } = request.body
    var queryText = `SELECT F.* FROM FAMILLE F where F.CODEFAMILLE = '${CODEFAMILLE}'`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText, (error, results) => {
            if (error) {
                response.status(500).send(error.message)
            } else {
                response.status(200).json(results.rows)
            }
        });
    }

}
const getFamilleTiersCode = (request, response) => {
    const {
        BD,
        CODE_FAM_TIERS
    } = request.body
    var queryText = `SELECT F.* FROM FAM_TIERS F where F.CODE_FAM_TIERS = '${CODE_FAM_TIERS}'`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText, (error, results) => {
            if (error) {
                response.status(500).send(error.message)
            } else {
                response.status(200).json(results.rows)
            }
        });
    }

}
const getArticlesSync = (request, response) => {
    const {
        BD,
        LBrowArticles,
        UBrowArticles,
        COLUMNS
    } = request.body
    var queryText = `SELECT ${COLUMNS} FROM ARTICLE`;
    if (configData[BD]['PG_BD'].includes('/')) {
        queryText += ` rows ${(parseInt(LBrowArticles.toString())+1).toString()} to ${(parseInt(LBrowArticles)+50).toString()}`
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        queryText += ` offset ${LBrowArticles} limit ${UBrowArticles}`
        pools[BD].query(queryText, (error, results) => {
            if (error) {
                response.status(500).send(error.message)
            } else {
                response.status(200).json(results.rows)
            }
        });
    }

}
const getTiersSync = (request, response) => {
    const {
        BD,
        LBrowArticles,
        UBrowArticles,
        COLUMNS
    } = request.body
    var queryText = `SELECT * FROM ARTICLE`;
    if (configData[BD]['PG_BD'].includes('/')) {
        queryText += ` rows ${(parseInt(LBrowArticles.toString())+1).toString()} to ${(parseInt(LB)+50).toString()}`
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });    
            }
        });
    } else {
        queryText += ` offset ${LBrowArticles} limit ${UBrowArticles}`
        pools[BD].query(queryText, (error, results) => {
            if (error) {
                response.status(500).send(error.message)
            } else {
                response.status(200).json(results.rows)
            }
        })
    }

}
const getFamillesTiers = (request, response) => {
    const { BD } = request.body
    var queryText = "SELECT F.* FROM FAM_TIERS F ORDER BY INTITULE";
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText, (error, results) => {
            if (error) {
                response.status(500).send(error.message)
            } else {
                response.status(200).json(results.rows)
            }
        });
    }

}
const getTiersFromFam = (request, response) => {
    const { BD, CODE_FAM_TIERS } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM TIERS where CODE_FAM_TIERS = '${CODE_FAM_TIERS}'`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}

const reqSelect = (request, response) => {
    const { BD, REQ } = request.body
        // console.log('REQ: ' + REQ);
    var queryText = REQ;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }
}


const getTiersFromCode = (request, response) => {
    const { BD, CODE_TIERS } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM TIERS where code_tiers = '${CODE_TIERS}'`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            })
    }

}
const getAllTable = (request, response) => {
    const { BD, TABLE, LB, UB } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM ${TABLE}`;
    if (configData[BD]['PG_BD'].includes('/')) {
        queryText += ` rows ${(parseInt(LB.toString())+1).toString()} to ${(parseInt(LB)+50).toString()}`
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        queryText += ` offset ${LB} limit ${UB}`
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}
const getAllTableRows = (request, response) => {
    const { BD, TABLE } = request.body
        // console.log(request.body)
    var queryText = `SELECT COUNT(1) FROM ${TABLE}`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    // console.log(results.rows)
                    response.status(200).json(results.rows)
                }
            });
    }

}
const getGps = (request, response) => {
    const { BD, USER, DATEMIN, DATEMAX } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM GPS_POSITIONS WHERE GPS_DATE 
IS NOT NULL AND GPS_DATE >= '${DATEMIN}' AND GPS_DATE <= '${DATEMAX}' AND CODE_TIERS = '${USER}' ORDER BY GPS_DATE DESC`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}

const getEtatLivraison = (request, response) => {
    const { BD, FAMILLE_ETAT_LIVRAISON } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM TIERS T, ALLC('${FAMILLE_ETAT_LIVRAISON}') A where T.CODE_FAM_TIERS=A.CODE_FAM`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}

const getPieceItems = (request, response) => {
    const { BD, NOPIECE } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM ITEM where (NOPIECE = '${NOPIECE}') and (NOITEM_M Is NULL) order by NOITEM`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}

const getCItems = (request, response) => {
    const { BD, NOITEM_M } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM ITEM where NOITEM_M = '${NOITEM_M}' order by NOITEM`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}


const getArticleItem = (request, response) => {
    const BD = request.body["BD"]
        // console.log(request.body)
    var columnsList = []
    var values = ""
    var queryText = "";
    var refs = JSON.parse(request.body["REF_ARTS"])
    for (var i in refs) {
        columnsList.push(`'${refs[i]}'`);
    }
    values = "(" + columnsList.join(",") + ")";
    queryText = `SELECT * FROM ARTICLE where ref_art in ${values}`
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}
const getPieceVersements = (request, response) => {
    const { BD, NOPIECE_O } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM PIECE where nopiece_o = '${NOPIECE_O}' order by REF_PIECE`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}
const getTarifsArticle = (request, response) => {
    const { BD, REF_ART } = request.body
        // console.log(request.body)
    var queryText = `SELECT T.CODE_TARIF, T.CODE_TYPE_TARIF, T.REF_ART, T.INTITULE, T.MARGE, T.QTEMIN, 
T.QTEMAX, T.PRIXHT, TT.INTITULE INTITULE_ORG 
FROM TARIF T 
left join TYPE_TARIF TT on (T.CODE_TYPE_TARIF = TT.CODE_TYPE_TARIF) 
WHERE T.REF_ART = '${REF_ART}' ORDER BY T.CODE_TYPE_TARIF`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}
const getEtats = (request, response) => {
    const { BD } = request.body
    var queryText = etats_request(request.body, request.body['ETAT']);
    // console.log(queryText)
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        console.log(error.message)
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    // if (request.body['NF3ReportRowsDebut'] == '-1')
                    //     console.log(results.rows);
                    response.status(200).json(results.rows);
                }
            });
    }

}
const tryConnect = (request, response) => {
    const { BD, VERSION } = request.body;
    if (configData[BD] != null) {
        var queryText = "select REF_ART from article"
        if (configData[BD]['PG_BD'].includes('/')) {
            // console.log(firebirdOptions[BD])
            queryText += ' rows 1 to 1'
            Firebird.attach(firebirdOptions[BD], function(err, db) {
                // console.log("ttttttttttttttttttttt")
                if (err) {
                    // console.log(err.message)
                    response.status(500).send(err.message)
                }
                else {
                    db.query(queryText, (error, results) => {
                        if (error) {
                            console.log(err.message)
                            response.status(500).send(error.message)
                        } else {
                            response.status(200).json(results)
                        }
                        db.detach();
                    });   
                }
            });
        } else {
            queryText += " limit 1"
            pools[BD].query(queryText,
                (error, results) => {
                    if (error) {
                        // console.log(error.message)
                        response.status(500).send(error.message)
                    } else {
                        if (parseInt(VERSION.split(".")[1]) == server_version) {
                            response.status(200).send("Success")
                        } else {
                            response.status(500).send("La version du serveur est incompatible")
                        }
                    }
                });
        }

    } else {
        response.status(500).send("Base de données n'existe pas")
    }

}
const connect = (request, response) => {
    const { BD, PASS } = request.body
    if (configData[BD] != null) {
        var queryText = "select * from article"
        if (configData[BD]['PG_passe'] == PASS) {
            if (configData[BD]['PG_BD'].includes('/')) {
                queryText += ` rows 1 to 1`;
                Firebird.attach(firebirdOptions[BD], function(err, db) {
                    if (err) {
                        response.status(500).send(err.message)
                    }
                    else {
                        db.query(queryText, (error, results) => {
                            if (error) {
                                response.status(500).send(error.message)
                            } else {
                                response.status(200).json(results)
                            }
                            db.detach();
                        });
                    }
                });
            } else {
                queryText += " limit 1"
                pools[BD].query("select * from article limit 1",
                    (error, results) => {
                        if (error) {
                            response.status(500).send(error.message)
                        } else {
                            response.status(200).send("Success")
                        }
                    })
            }

        } else {
            response.status(500).send("Mot de passe postgres incorrect")
        }
    } else {
        response.status(500).send("Base de données n'existe pas")
    }

}

function transformExplicitMap(obj00) {
    var mp0 = {};
    for (const key in obj00) {
        mp0[key.toUpperCase()] = obj00[key];
    }
    return mp0;
}

async function getSecureAllofUser2(user0, BD) {
    var queryText = `SELECT upper(P.OBJECT2) OBJECT2, upper(P.RELATION) RELATION, 
upper(P.PARAMOBJECT2) PARAMOBJECT2, upper(P.SUBOBJECT2) SUBOBJECT2 
FROM PERMISSIONS P 
where (upper(P.object1) = '${user0}') and (P.relation <> 'R')`;
    // console.log(queryText)
    return new Promise(resolve => {
        if (configData[BD]['PG_BD'].includes('/')) {
            Firebird.attach(firebirdOptions[BD], function(err, db) {
                if (err) {
                    return []
                }
                else {
                    db.query(queryText, (error, results) => {
                        if (error) {
                            return []
                        } else {
                            resolve(results)
                        }
                        db.detach();
                    });
                }
            });
        } else {
            pools[BD].query(queryText,
                (error, results) => {
                    if (error) {
                        return []
                    }
                    resolve(results.rows)
                })
        }

    });
}

async function getSecureAllofUser0(user, BD) {
    var queryText = `SELECT upper(OBJECT2) OBJECT2 FROM PERMISSIONS P 
where (upper(P.OBJECT1) = '${user}') and (P.RELATION = 'R')`;
    return new Promise(resolve => {
        if (configData[BD]['PG_BD'].includes('/')) {
            Firebird.attach(firebirdOptions[BD], function(err, db) {
                if (err) {
                    return [];
                }
                else {
                    db.query(queryText, (error, results) => {
                        if (error) {
                            return [];
                        } else {
                            resolve(results);
                        }
                        db.detach();
                    });
                }
            });
        } else {
            pools[BD].query(queryText,
                (error, results) => {
                    if (error) {
                        return [];
                    }
                    resolve(results.rows);
                })
        }
    });

}


const getSecureAllofUser1 = async(request, response) => {
    const { BD, USER } = request.body
        // console.log(request.body)
    var mp0 = [USER];
    var results01 = [];
    var i = 0;
    var queryText = `SELECT upper(OBJECT2) OBJECT2 FROM PERMISSIONS P 
where (upper(P.OBJECT1) = '${USER}') and (P.RELATION = 'R')`;
    while (i < mp0.length) {
        user1 = mp0[i];
        nw0 = "";

        var res00 = await getSecureAllofUser0(USER, BD)
            // console.log(res00)
        for (var e in res00) {
            var val00 = res00[e]
            nw0 = val00['object2'];

            if (mp0.indexOf(nw0) < 0) {
                mp0.push(nw0);
            }
        }
        i += 1;
    }
    for (i = 0; i < mp0.length; i++) {
        var user2 = mp0[i];
        var results00 = await getSecureAllofUser2(user2.toUpperCase(), BD);
        var vs0 = [];
        for (var r in results00) {
            var val00 = results00[r]
            vs0.push(transformExplicitMap(val00));

        }
        results01.push(vs0);
    }
    response.status(200).json(results01)
}

const ifUserExit = (request, response) => {
    const { BD, USER, PASS } = request.body
    if (configData[BD]['PG_username'] == USER && configData[BD]['PG_passe'] == PASS) {
        // console.log("dzdzdzdzd")
        response.status(200).json([{ "code_tiers": USER }])
    } else {
        var queryText = `select code_tiers from utilisateurs where username= '${USER}' and pass = '${PASS}'`
        if (configData[BD]['PG_BD'].includes('/')) {
            Firebird.attach(firebirdOptions[BD], function(err, db) {
                if (err) {
                    response.status(500).send(err.message)
                }
                else {
                    db.query(queryText, (error, results) => {
                        if (error) {
                            response.status(500).send(error.message)
                        } else {
                            response.status(200).json(results)
                        }
                        db.detach();
                    });
                }
            });
        } else {
            pools[BD].query(queryText,
                (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    }
                    // console.log("success")
                    else {
                        response.status(200).json(results.rows)
                    }
                });
        }
    }


}
const getPieceCountLocal = (request, response) => {
    const { BD, CODE_TYPE_PIECE } = request.body
        // console.log(request.body)
    var queryText = `SELECT count(*) FROM PIECE where CODE_TYPE_PIECE = '${CODE_TYPE_PIECE}'`
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
            

        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}
const getOnePiece = (request, response) => {
    const { BD, NOPIECE } = request.body
        // console.log(request.body)
    var piece = {}
    var queryText1 = `SELECT * FROM PIECE where NOPIECE = '${NOPIECE}' order by REF_PIECE`
    var queryText2 = `SELECT * FROM ITEM where NOPIECE = '${NOPIECE}'`
    var queryText3 = `SELECT * FROM PIECE where nopiece_o = '${NOPIECE}' order by REF_PIECE`
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText1, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        piece = results[0]
                        db.query(queryText2, (error, results1) => {
                            if (error) {
                                response.status(500).send(error.message)
                            } else {
                                piece['ITEMS'] = results1;
                                db.query(queryText3, (error, results2) => {
                                    if (error) {
                                        response.status(500).send(error.message)
                                    } else {
                                        piece['VERSEMENTS'] = results2
                                        response.status(200).json([piece])
                                    }
                                });
                            }
                            db.detach();
                        });
                    }
                });
            }
            


        });
    } else {
        pools[BD].query(queryText1,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                piece = results.rows[0]
                pools[BD].query(queryText2,
                    (error, results1) => {
                        if (error) {
                            //   console.log(error)
                            response.status(500).send(error.message)
                        }
                        // console.log("success")
                        piece['ITEMS'] = results1.rows
                        pools[BD].query(queryText3,
                            (error, results2) => {
                                if (error) {
                                    // console.log(error)
                                    response.status(500).send(error.message)
                                }
                                // console.log("success")
                                piece['VERSEMENTS'] = results2.rows
                                response.status(200).json([piece])
                            })
                    })


            });
    }

}
const getTiersPlaces = (request, response) => {
    const { BD, CODE_FAM_TIERS } = request.body
        // console.log(CODE_FAM_TIERS)
        // CODEFAMILLE, CODE_TYPE_PIECE
        // console.log(request.body)
        //     var queryText = `SELECT T.*, PP.NOPIECE, PP.DATEPIECE FROM TIERS T join
        // AllC('${CODEFAMILLE}') f on (f.code_fam = code_fam_tiers)
        //     left join LATERAL (select * from piece P where ((P.code_type_piece
        // ='${CODE_TYPE_PIECE}') and (P.MONTANTVERSE = 0) and (P.ANNULEE = 1) and
        // (T.code_tiers = P.code_tiers)) order by datepiece desc limit 1) as PP on (T.code_tiers = PP.code_tiers) order by T.RAISON_SOCIALE asc`

    var queryText = `SELECT T.RAISON_SOCIALE, T.CODE_TIERS, T.NOPIECE, P.DATEPIECE FROM TIERS T
    left join piece P on (P.nopiece = T.NOPIECE) 
     where T.CODE_FAM_TIERS = '${CODE_FAM_TIERS}' order by T.RAISON_SOCIALE asc`
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                }); 
            }
            

        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                }
                // console.log("success")
                else {
                    response.status(200).json(results.rows)
                }
            });
    }

}

const getSpecificFamilles = (request, response) => {
    const { BD, CODEFAMILLE } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM FAMILLE where codefamille_m = '${CODEFAMILLE}'`
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
            

        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                } else {
                    response.status(200).json(results.rows)
                };
            });
    }

}
const generRefArt = (request, response) => {
    const { BD, LEN, DEBUT, DEBUTSUITE } = request.body
        // console.log(request.body)
    var queryText = '';
    //     queryText = `select COALESCE(max(cast(substr(REF_ART, ${LEN}, 35) as numeric(18) )),0)+1 lastnumb 
    // from article 
    // where (REF_ART like '${DEBUTSUITE}') and (REF_ART <> '${DEBUT}' ) 
    // and (substr(REF_ART, ${LEN}, 35) similar to '[0-9]+')`;
    if (configData[BD]['PG_BD'].includes('/')) {
        // select coalesce(max( cast((select IntFld from extractMaximum( REF_ART )) as bigint )), 0)+1 lastnumb 
        // from ARTICLE  where strlen(REF_ART) <= 20
        // -
        // select coalesce(max( cast((select IntFld from get_numeric( REF_ART ) as intNoPiece )as bigint)), 0)+1 lastnumb
        // from ARTICLE  where strlen(REF_ART) <= 20
        // -
        queryText = `select coalesce(max( cast((select IntFld from get_numeric( REF_ART ) as intNoPiece )as bigint)), 0)+1 lastnumb
            from ARTICLE  where (strlen(REF_ART) <= 20) and (REF_ART like '${DEBUTSUITE}')`;
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else { 
                    db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }

        });
    } else {
        // select coalesce(max( cast((select extractMaximum( REF_ART )) as bigint )), 0)+1 lastnumb 
        // from ARTICLE  where strlen(REF_ART) <= 20
        // -
        // Select coalesce(max(COALESCE(substring(REF_ART from '\d+$'), '0')::numeric), 0)+1 lastnumb 
        // from ARTICLE where strlen(REF_ART) <= 20
        // -
        // select coalesce(max( cast((select get_numeric( REF_ART ) as intNoPiece) as bigint)), 0)+1 lastnumb
        // from ARTICLE  where strlen(REF_ART) <= 20
        queryText = `Select coalesce(max(COALESCE(substring(REF_ART from '\\d+$'), '0')::numeric), 0)+1 lastnumb 
        from ARTICLE where (strlen(REF_ART) <= 20) and (REF_ART like '${DEBUTSUITE}')`;
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                } else {
                    // console.log('Test generRefArt ' + queryText.toString());
                    // console.log('Test generRefArt ' + JSON.stringify(results.rows));
                    response.status(200).json(results.rows)
                };
            });
    }

}
const generCodeTiers = (request, response) => {
    const { BD, LEN, FAMSUITE, FAM } = request.body
        // console.log(request.body)
    var queryText = '';
    // queryText = `select COALESCE(max(cast(substr(CODE_TIERS, ${LEN}, 20) as float)), 0)+1 lastnumb 
    //         from tiers
    //         where (CODE_TIERS like '${FAMSUITE}') and (CODE_TIERS <> '${FAM}') and
    //         (TRIM(substr(CODE_TIERS, ${LEN}, 20)) SIMILAR TO '[0-9]+')`
    if (configData[BD]['PG_BD'].includes('/')) {
        // queryText = `select coalesce(max( cast((select IntFld from extractMaximum( code_tiers )) as bigint )), 0)+1 lastnumb 
        // from tiers  where strlen(code_tiers) <= 20`
        queryText = `select coalesce(max( cast((select IntFld from get_numeric( CODE_TIERS ) as intNoPiece )as bigint)), 0)+1 lastnumb
          from TIERS  where (strlen(CODE_TIERS) <= 20) and (CODE_TIERS like '${FAMSUITE}')`
            // console.log(queryText)
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }

        });
    } else {
        // queryText = `select coalesce(max( cast((select extractMaximum( code_tiers )) as bigint )), 0)+1 lastnumb 
        // from tiers  where strlen(code_tiers) <= 20`
        queryText = `Select coalesce(max(COALESCE(substring(CODE_TIERS from '\\d+$'), '0')::numeric), 0)+1 lastnumb 
        from TIERS where (strlen(CODE_TIERS) <= 20)  and (CODE_TIERS like '${FAMSUITE}')`
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                } else {
                    // console.log('Test generCodeTiers ' + queryText.toString());
                    // console.log('Test generCodeTiers ' + JSON.stringify(results.rows));
                    response.status(200).json(results.rows)
                };
            });
    }

}
const getDistributionPieces = (request, response) => {
    const { BD, CODE_TIERS, DATE, CODE_TYPE_PIECE } = request.body
    var codeCommercialCondition00 = "";
    if (CODE_TIERS != "") {
        codeCommercialCondition00 = `and code_commercial = '${CODE_TIERS}'`;
    }
    var queryText = `select P.*, T.raison_sociale, C.raison_sociale join_commercial from piece P LEFT JOIN tiers T ON T.code_tiers = P.code_tiers
LEFT JOIN tiers C ON C.code_tiers = P.code_commercial where P.datepiece >= '${DATE}'
and P.code_type_piece = '${CODE_TYPE_PIECE}' ${codeCommercialCondition00}`
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    //   console.log(error)
                    response.status(500).send(error.message)
                } else {
                    response.status(200).json(results.rows)
                };
            });
    }

}
const getUtilisateur = (request, response) => {
    const { BD, CODE_TIERS } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM UTILISATEURS WHERE CODE_TIERS = '${CODE_TIERS}'`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    //   console.log(error)
                    response.status(500).send(error.message)
                } else {
                    response.status(200).json(results.rows)
                };
            });
    }

}
const getArticleRefArt = (request, response) => {
    const { BD, REF_ART } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM ARTICLE WHERE upper(REF_ART) = upper('${REF_ART}')`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    //   console.log(error)
                    response.status(500).send(error.message)
                } else {
                    response.status(200).json(results.rows)
                };
            });
    }

}
const getContacts = (request, response) => {
    const { BD, CODE_TIERS } = request.body
        // console.log(request.body)
    var queryText = `SELECT * FROM CONTACT WHERE CODE_TIERS = '${CODE_TIERS}' order by ID`;
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                } else {
                    response.status(200).json(results.rows)
                };
            });
    }

}
const getFamilleRefArt = (request, response) => {
    const { BD, REF_ARTS, CODEFAMILLES } = request.body
        // console.log(request.body)
    var refArtsList = REF_ARTS.split(",")
    var codefamillesList = CODEFAMILLES.split(",")

    var refArtsText = "";
    var codfmaillesText = "";
    for (let index = 0; index < refArtsList.length; index++) {
        refArtsText += `'${refArtsList[index]}'`;
        if (index + 1 != refArtsList.length) {
            refArtsText += ',';
        }
    }
    // for (let index = 0; index < codefamillesList.length; index++) {
    //     codfmaillesText += `'${codefamillesList[index]}'`;
    //     if (index + 1 != codefamillesList.length) {
    //         codfmaillesText += ',';
    //     }
    // }
    var queryText = `SELECT A.ref_art, A.codefamille from Article A join AllF(A.codefamille) f 
    on (f.CODE_FAM = A.codefamille) where A.ref_art IN(${refArtsText}) `;
    //     var queryText = `SELECT A.ref_art, A.codefamille from Article A join AllF(A.codefamille) f 
    // where A.ref_art IN (${refArtsText}) and f.CODE_FAM IN(${codfmaillesText})`;
    // WHERE A.codefamille = F.codefamille and
    // AllF('${CODEFAMILLE}') f on (f.CODE_FAM = A.CODEFAMILLE)
    // console.log(queryText)
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                } else {
                    response.status(200).json(results.rows)
                };
            });
    }

}
const getParametre = (request, response) => {
    const { BD, PARAM } = request.body
    var queryText = "SELECT * from parametre";
    if (PARAM != "ALL") {
        queryText += ` WHERE param = '${PARAM}'`;
    }
    // WHERE A.codefamille = F.codefamille and
    // AllF('${CODEFAMILLE}') f on (f.CODE_FAM = A.CODEFAMILLE)
    // console.log(queryText)
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }

        });
    } else {
        // console.log("Test getParametre: " + queryText)
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    console.log(error)
                    response.status(500).send(error.message)
                } else {
                    // onsole.log("Test getParametre: " + results.rows[0]['valeur'].toString());
                    response.status(200).json(results.rows)
                };
            });
    }

}
const getCodeSite = (request, response) => {
    const { BD, PARAM } = request.body
    var queryText = "select distinct CODE_SITE from PIECE where (CODE_SITE!='')";
    if (configData[BD]['PG_BD'].includes('/')) {
        Firebird.attach(firebirdOptions[BD], function(err, db) {
            if (err) {
                response.status(500).send(err.message)
            }
            else {
                db.query(queryText, (error, results) => {
                    if (error) {
                        response.status(500).send(error.message)
                    } else {
                        response.status(200).json(results)
                    }
                    db.detach();
                });
            }
        });
    } else {
        pools[BD].query(queryText,
            (error, results) => {
                if (error) {
                    // console.log(error)
                    response.status(500).send(error.message)
                } else {
                    response.status(200).json(results.rows)
                };
            });
    }
    
}

module.exports = {
    getArticlesTest,
    sendGps,
    getPieces,
    getPiecesCount,
    getArticles,
    getArticlesCount,
    getTiers,
    getArticleTiersCount,
    insert,
    update,
    tableExists,
    getFamilles,
    getFamillesTiers,
    getTiersFromFam,
    getAllTable,
    getEtatLivraison,
    getPieceItems,
    getCItems,
    getArticleItem,
    getPieceVersements,
    getTarifsArticle,
    deleteFromTable,
    getEtats,
    tryConnect,
    getSecureAllofUser1,
    ifUserExit,
    getPieceCountLocal,
    getOnePiece,
    getTiersPlaces,
    getSpecificFamilles,
    generRefArt,
    generCodeTiers,
    getUtilisateur,
    getDistributionPieces,
    getArticleRefArt,
    getContacts,
    getTiersFromCode,
    getGps,
    getFamilleCode,
    getFamilleTiersCode,
    getAllTableRows,
    getArticlesSync,
    getTiersSync,
    connect,
    getFamilleRefArt,
    getParametre,
    getCodeSite,
    reqSelect,
}