# Uni.lu plugins

Marketplace des plugins Claude de l'AI Dev Factory (Université du Luxembourg × Dotika).

| Plugin | Version | Rôle |
|---|---|---|
| ai-dev-factory-spec | 1.4.0 | Étape Spec : existant (`/elicitation`) ou nouvelle application (`/scope-map`, `/scope-challenge`, `/prd-draft`), puis `/opportunity-mapping`, skill `diagram`, agent `prd-griller` |

## Installer

Dans Claude (organisation) : Organization settings > Plugins, ajouter `Dotika-ai/unilu-plugins`.

Dans Claude Code :

```
/plugin marketplace add Dotika-ai/unilu-plugins
/plugin install ai-dev-factory-spec@dotika-unilu
```
