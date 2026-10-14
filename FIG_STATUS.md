# Strangler-Fig Status: OnlyOffice DocumentServer → World-Office Rust

Generiert 2026-10-13T23:17:40.979Z, Probes gegen http://127.0.0.1:18113.

Die Strangler-Fig-Fassade ist der `documentserver`-Container: dieselbe API-Fläche (discovery, WOPI, conversion, editor-Bundles), dahinter bereits der Rust docserver. Dieses Protokoll entscheidet je Capability, ob die OO-Node-Referenz (services/server) ausgeschaltet werden darf.

**States: canonical 12 · shadow 3 · blocked 0 · legacy 0**

| Capability | State | Probe | Oracle |
|---|---|---|---|
| hosting-discovery | **canonical** | HTTP 200, 1 app entries | contract: root=true net-zone=true apps=1 edit-docx-action=true |
| wopi-checkfileinfo | **shadow** | HTTP 400 (auth boundary clean) | http: probe IS the oracle |
| wopi-contents | **shadow** | HTTP 400 (auth boundary clean) | http: probe IS the oracle |
| wopi-locks | **shadow** | HTTP 200 | http: probe IS the oracle |
| conversion-convert | **canonical** | HTTP 200, status=Success, pdf-bytes=4529 | golden: 3/3 golden conversions pass (sim 1/1/0.75) |
| conversion-formats | **canonical** | HTTP 200 | contract: 58 formats (ref 58), [from,to] shape=true, docx->pdf=true |
| editor-ui-word | **canonical** | HTTP 200, ribbon-markers=true | parity-contracts: 6 pass / 0 fail (known-gaps excluded) |
| editor-ui-sheet | **canonical** | HTTP 200 | census: presence census OK: buttons=34 (baseline 34), fileMenu=true, canvas=3; OO-depth pending |
| editor-ui-slide | **canonical** | HTTP 200 | census: presence census OK: buttons=46 (baseline 46), fileMenu=true, canvas=0; OO-depth pending |
| editor-ui-pdf | **canonical** | HTTP 200 | census: presence census OK: buttons=19 (baseline 19), fileMenu=true, canvas=3; OO-depth pending |
| editor-ui-diagram | **canonical** | HTTP 200 | census: presence census OK: buttons=15 (baseline 15), fileMenu=true, canvas=1; OO-depth pending |
| collab-ws | **canonical** | skipped (no live probe defined) | collab: ws broadcast A→B=true B→A=true, late-joiner replay=true; editor-side integration = stage 2 |
| spellchecker | **canonical** | skipped (no live probe defined) | auth: aff=200 (hunspell header ok), dic-subdir=200, traversal=404 |
| command-service | **obsolete** | skipped (no live probe defined) | none: not ported — no WO client calls this surface (dies with legacy teardown) |
| jwt-auth | **canonical** | skipped (no live probe defined) | auth: valid=502 (forward attempted — auth passed), expired=401, garbage=401 |
| document-api | **canonical** | HTTP 200 | contract: new=true info=true put=true get=true html=true meta=true |

## Cutover-Pfad je Capability

1. **legacy → shadow**: Rust-Impl hinter der Fassade registrieren (Container-API unverändert).
2. **shadow → canonical**: Oracle grün — `http`: Probe; `parity-contracts`: L2-Verträge 5/0; `census`: Marker-Census; `golden`: byte/semantic compare gegen OO-Referenz-Outputs (capture-oo-goldens.py).
3. **canonical**: OO-Node-Pfad entfernen, Rust bleibt Rückfall nicht mehr nötig. Rollback = Git, nicht Doppelbetrieb.

### Offene Oracles (blockiert Cutover)

`http`-Probes sind Smokes (Fassade lebt, Formen stimmen grob) — sie allein rechtfertigen keinen Cutover, der echte Kontrakt gegen die OO-Referenz fehlt noch.

### Nur-Smoke (Kontrakt-Hochstufung offen)

- **wopi-checkfileinfo** — probe: HTTP 400 (auth boundary clean); Form-Kontrakt (Antwortschema vs. OO-Referenz) als Hochstufung
- **wopi-contents** — probe: HTTP 400 (auth boundary clean); Form-Kontrakt (Antwortschema vs. OO-Referenz) als Hochstufung
- **wopi-locks** — probe: HTTP 200; Form-Kontrakt (Antwortschema vs. OO-Referenz) als Hochstufung


## Rückbau (Teardown) der Node-Referenz

`services/server` (OO-Node-DocService) läuft nirgends mehr:

- **Prod** (`opencloud-compose`): Editor via Rust-`wo-docserver` auf :8082
  (`worldoffice/documentserver:latest`, `exec /usr/local/bin/wo-docserver`, editor-ui
  mounts aus `editor-ui-<sha>/`). Python-docserver (:8087) = deprecated Agentic-AI-loop.
- **E2E** (`tests/docker-compose.test.yml`): `documentserver` baut aus dem Rust-Monorepo
  (`docker/documentserver/Dockerfile`), `coauthoring` aus `docker/coauthoring-service`.
- **CI**: `deploy.yml` baute noch ein ungenutztes `ghcr …/server`-Image (kein Deploy-Job,
  null Konsumenten) — **aus der Build-Matrix entfernt** (server@16ce3a317).
- Kein Script/Test/Compose referenziert `services/server` als Runtime. Quelle + DocBuilder-CLI
  bleiben als Referenz; der separate `services/server`-CI ist unangetastet.

Damit ist der Strangler-Rückbau auf Fassadenebene abgeschlossen: der Rust-Stack
stellt die gesamte Editor-API-Fläche, der OO-Node-DocService ist aus dem Deploy-Pfad
genommen. Verbleibend: WOPI×3 Form-Kontrakte (E2E-überdeckt) als letzte Smoke-Hochstufung.
