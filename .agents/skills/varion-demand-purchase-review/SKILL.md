---
name: varion-demand-purchase-review
description: "Bewertet reale Nachfrage, bestaetigten Bestand und Lieferkonditionen fuer begruendete Beschaffungsvorschlaege im vorhandenen Procurement-Ablauf. Nutzen fuer Einkaufspruefungen; keine Bestellung oder Zahlung."
metadata:
  owner_role: procurement
  version: "1.0.0"
---

# varion-demand-purchase-review

## Auftrag: Beschaffungsvorschläge prüfen

1. Lade die aktuelle architecture/procurement-workflow.v1.json und
   tools/PROCUREMENT-APP-CONTRACT.md aus dem CEO-Vertrag. Verwende Ergebnisse
   des bestehenden autorisierten Rollen-/Scan-/TaskPort-Ablaufs und seine
   bestätigten Originalquellen; starte hier keinen zweiten Beschaffungsprozess.
2. Trenne Wiederholungsnachfrage von Sonderbeschaffung und einmaligen Verkäufen.
   Storno, Erstattung, Reservierung, bestehende Lieferantenbestellung,
   Versandmeldung und physischer Wareneingang dürfen nicht vermischt werden.
   Historische Exporte sind keine aktuellen Verkaufs- oder Bestandszählungen.
3. Verbinde Lieferantenpositionen, Packungs-/Einzelmengen und eigene Artikel
   nachvollziehbar. Ein Shop-Zähler, Nachbestellkennzeichen oder alter EK
   beweist weder physischen Bestand noch aktuelle Lieferfähigkeit oder Fracht.
4. Mengenbewertung nur mit bestätigtem Bestand und dem im aktuellen Vertrag
   zulässigen abgeschlossenen Quellen-/Zykluszustand. Sonst Datenlücken und
   benötigte Bestätigung liefern, keine Auffüllmenge erfinden. Aktuelle
   Quellengültigkeitsregeln beibehalten, keine pauschale neue TTL einführen.
5. Wo die Basis genügt, begründe Priorität und gegebenenfalls Menge anhand
   tatsächlicher Nachfrage, verfügbarer Menge, schon offener Bestellung und
   belegter Konditionen. Unbekannte Fracht bleibt unbekannt; Vorschlag,
   konkrete Bestellfreigabe, Bestellreceipt, Proforma und Zahlung getrennt halten.

Ergebnis: Vorschlag oder ausdrücklich nicht belastbare Mengenbewertung mit
Artikel-/Lieferantenbindung, Quellenabdeckung, belegten Kosten, Widersprüchen
und nächstem Schritt im bestehenden Ablauf. Dieser Zusatzskill löst keinen
neuen Scan-Claim, Publisher-POST, Prepare/Confirm, Lieferantenkontakt, Warenkauf
oder Zahlung aus. Die vorhandenen autorisierten Ausführungswege bleiben dafür
zuständig; keine Rollenübernahme oder Umgehung ihrer Bindungen.

## Einordnung und bestehender Kontext

Dieser zusätzliche Skill arbeitet im Auftrag der jeweiligen Rolle. Lies deren
aktuelle AGENTS.md und ROLE-REFERENCE.md und führe den dort vorgegebenen gemeinsamen
Kontext-/Memory-Start aus. Verwende die aktuelle Vertragsrevision und bestehende
Fach-Reader. Der Skill erweitert deren Berechtigungen nicht und ersetzt keinen
vorhandenen Skill, fachlichen Ablauf oder Freigabeprozess.

Sein eigener Umfang ist Lesen, Prüfen und ein interner Bericht oder Entwurf.
Schon autorisierte andere Abläufe bleiben getrennt gültig. Er richtet keine neue
Automatik, Infrastruktur, Erinnerung, kostenpflichtige API oder Nachrichtenroutine ein.
Keine private Kunden-, Finanz- oder Lieferanteninformation, Rohantwort oder Zugangsdaten
in dieses Rollen-Repository schreiben. Ergebnisse gehören in die bestehende,
tatsächlich als privat bestätigte Auftrags-/Ergebnisablage. Die Bezeichnung „privat“
in einer alten Notiz ersetzt keine Zugriffsprüfung.

## Nachweis und Abschluss

- Binde Erkenntnisse an tatsächliche Quellen-IDs, deren ursprüngliche Beobachtungszeit,
  den Prüfzeitpunkt, die Vertragsrevision sowie den gelesenen Ausschnitt und seine Abdeckung.
  Ein interner Status, Cache, HTTP 200 oder vorhandener Schlüssel belegt keinen Facherfolg.
- Fehlende Daten bleiben unbekannt. Veraltete, historische und synthetische Quellen
  ausdrücklich kennzeichnen; Testdaten autorisieren keine echte Geschäftsaktion.
- Berichte evidenceStatus complete, partial oder unavailable für den geprüften Umfang;
  wechsle deshalb nicht eigenmächtig das Statusschema der bestehenden Aufgaben.
- Liefere die wesentlichen Befunde mit owner, sourceRefs, nächstem konkretem Schritt
  und einem tatsächlich prüfbaren Ergebnisverweis. Zeige nur belegte Beträge und Wirkungen.
- Nutze für zugeordnete Aufgaben den bestehenden shared_tasks.py-/TaskPort-Vertrag
  einschließlich erwarteter Version, operationId und Ergebnis-Readback. Ein unklarer
  Schreibausgang wird vor Wiederholung abgeglichen. Ohne aktuelle Aufgabe keine
  beliebige fremde Aufgabe übernehmen oder als abgeschlossen markieren.
- Beende den gemeinsamen Kontextlauf wie in AGENTS.md vorgesehen. Fehlt ein Zugriff,
  benenne den genauen Reader/Scope/Fehler, setze nur abhängige Arbeit aus und behaupte
  weder gespeicherte Ergebnisse noch eine erfolgreiche Live-Abnahme.
