# Strangler-Fig Status: OnlyOffice DocumentServer → World-Office Rust

Generiert 2026-10-13T18:26:45.008Z, Probes gegen http://127.0.0.1:18113.

Die Strangler-Fig-Fassade ist der `documentserver`-Container: dieselbe API-Fläche (discovery, WOPI, conversion, editor-Bundles), dahinter bereits der Rust docserver. Dieses Protokoll entscheidet je Capability, ob die OO-Node-Referenz (services/server) ausgeschaltet werden darf.

**States: canonical 5 · shadow 10 · blocked 0 · legacy 1**

| Capability | State | Probe | Oracle |
|---|---|---|---|
| hosting-discovery | **shadow** | HTTP 200, 1 app entries | http: probe IS the oracle |
| wopi-checkfileinfo | **shadow** | HTTP 400 (auth boundary clean) | http: probe IS the oracle |
| wopi-contents | **shadow** | HTTP 400 (auth boundary clean) | http: probe IS the oracle |
| wopi-locks | **shadow** | HTTP 200 | http: probe IS the oracle |
| conversion-convert | **shadow** | HTTP 200, status=Success, pdf-bytes=4529 | golden: golden capture pipeline not yet wired (capture-oo-goldens.py exists) |
| conversion-formats | **shadow** | HTTP 200 | http: probe IS the oracle |
| editor-ui-word | **canonical** | HTTP 200, ribbon-markers=true | parity-contracts: 6 pass / 0 fail (known-gaps excluded) |
| editor-ui-sheet | **canonical** | HTTP 200 | census: presence census OK: buttons=34 (baseline 34), fileMenu=true, canvas=3; OO-depth pending |
| editor-ui-slide | **canonical** | HTTP 200 | census: presence census OK: buttons=46 (baseline 46), fileMenu=true, canvas=0; OO-depth pending |
| editor-ui-pdf | **canonical** | HTTP 200 | census: presence census OK: buttons=19 (baseline 19), fileMenu=true, canvas=3; OO-depth pending |
| editor-ui-diagram | **canonical** | HTTP 200 | census: presence census OK: buttons=15 (baseline 15), fileMenu=true, canvas=1; OO-depth pending |
| collab-ws | **shadow** | skipped (no live probe defined) | none: oracle to be defined |
| spellchecker | **shadow** | skipped (no live probe defined) | none: oracle to be defined |
| command-service | **legacy** | skipped (no live probe defined) | none: oracle to be defined |
| jwt-auth | **shadow** | skipped (no live probe defined) | none: oracle to be defined |
| document-api | **shadow** | HTTP 200 | http: probe IS the oracle |

## Cutover-Pfad je Capability

1. **legacy → shadow**: Rust-Impl hinter der Fassade registrieren (Container-API unverändert).
2. **shadow → canonical**: Oracle grün — `http`: Probe; `parity-contracts`: L2-Verträge 5/0; `census`: Marker-Census; `golden`: byte/semantic compare gegen OO-Referenz-Outputs (capture-oo-goldens.py).
3. **canonical**: OO-Node-Pfad entfernen, Rust bleibt Rückfall nicht mehr nötig. Rollback = Git, nicht Doppelbetrieb.

### Offene Oracles (blockiert Cutover)

`http`-Probes sind Smokes (Fassade lebt, Formen stimmen grob) — sie allein rechtfertigen keinen Cutover, der echte Kontrakt gegen die OO-Referenz fehlt noch.
- **conversion-convert** — oracle `golden`: golden capture pipeline not yet wired (capture-oo-goldens.py exists)
- **collab-ws** — oracle `none`: oracle to be defined
- **spellchecker** — oracle `none`: oracle to be defined
- **jwt-auth** — oracle `none`: oracle to be defined

