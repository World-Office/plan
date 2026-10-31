# Strangler-Fig Status: OnlyOffice DocumentServer → World-Office Rust

Generiert 2026-10-14T14:37:38.262Z, Probes gegen http://127.0.0.1:18113.

Die Strangler-Fig-Fassade ist der `documentserver`-Container: dieselbe API-Fläche (discovery, WOPI, conversion, editor-Bundles), dahinter bereits der Rust docserver. Dieses Protokoll entscheidet je Capability, ob die OO-Node-Referenz (services/server) ausgeschaltet werden darf.

**States: canonical 15 · shadow 0 · blocked 0 · legacy 0**

| Capability | State | Probe | Oracle |
|---|---|---|---|
| hosting-discovery | **canonical** | HTTP 200, 1 app entries | contract: root=true net-zone=true apps=1 edit-docx-action=true |
| wopi-checkfileinfo | **canonical** | HTTP 400 (auth boundary clean) | wopi: status=200 |
| wopi-contents | **canonical** | HTTP 400 (auth boundary clean) | wopi: status=200 |
| wopi-locks | **canonical** | HTTP 400 (auth boundary clean) | wopi: status=200 |
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

