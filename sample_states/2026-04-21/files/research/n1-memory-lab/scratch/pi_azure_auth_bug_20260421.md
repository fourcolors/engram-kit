# Pi Azure-Anthropic-Foundry Auth Bug — 2026-04-21

## Symptom

During blind-packet rerun (v0.2.4 → v0.2.5), every Opus-judge cell failed with 401
from Azure:

```
401 {"error":{"code":"401","message":"Access denied due to invalid subscription key
     or wrong API endpoint..."}}
```

GPT-5.4 judge arms (provider `openai-codex`) worked fine. Only the Azure-routed
Opus arms failed.

## Root cause — corrected

The original suspicion pointed at the OS sandbox stripping env vars. **That was
wrong.** The actual cause is in syke's own Pi-launch code.

Commit `dc83d39` (Apr 21 15:29 PDT) replaced Pi's wildcard env-forwarding logic:

```python
# pre-dc83d39 (broad wildcard, worked for Apr 20 Opus runs)
if key.endswith("_API_KEY") or key.endswith("_TOKEN") or ...:
    env[key] = value

# post-dc83d39 (explicit per-provider allowlist, introduced today)
for key in _host_env_passthrough_keys(provider):  # per-provider allowlist
    ...
```

The new allowlist:

```python
_PROVIDER_HOST_ENV_ALLOWLIST = {
    "anthropic": {"ANTHROPIC_API_KEY", ...},
    "openai": {"OPENAI_API_KEY", ...},
    "openai-codex": {"OPENAI_API_KEY", ...},
    "openrouter": {"OPENROUTER_API_KEY", ...},
    "azure-openai-responses": {"AZURE_OPENAI_API_KEY", ...},   # has Azure OpenAI
    "kimi-coding": {"KIMI_API_KEY", ...},
    "zai": {"ZAI_API_KEY", ...},
    # BUT: "azure-anthropic-foundry" was missing from this list.
}
```

The user's `models.json` registers only one provider: `azure-anthropic-foundry`.
So today — for the first time since the hardening commit — judge runs through
that provider had no `AZURE_OPENAI_API_KEY` in Pi's subprocess env.

Pi's resolver (`pi-coding-agent/dist/core/resolve-config-value.js` line 14):

```js
const envValue = process.env[config];
return envValue || config;   // ← silent literal fallback
```

Since `process.env.AZURE_OPENAI_API_KEY` was empty in Pi, the resolver returned
the literal string `"AZURE_OPENAI_API_KEY"` as the key. Azure Foundry replied
with `401 "invalid subscription key"` — technically correct, since the string is
not a valid key.

## Diagnosis steps that led to the finding

1. Direct `curl -H "x-api-key: $AZURE_OPENAI_API_KEY" https://azure-lunar.openai.
   azure.com/anthropic/v1/messages` returned HTTP 200 with real Opus response.
   → Key and endpoint are fine.
2. Python `os.environ.get("AZURE_OPENAI_API_KEY")` inside benchmark_runner shows
   the key (84 chars, last-4 `vJ79`).
3. `subprocess.run(['env'])` from Python shows the var present. → Env propagation
   to direct children works.
4. Read Pi's model-registry.js (line 478) — confirms `authStorage.getApiKey` is
   tried first, and FAILS OVER to `resolveConfigValue(providerConfig.apiKey)`.
5. Read resolve-config-value.js line 14 — confirms fallback-to-literal behavior.
6. Added `azure-anthropic-foundry` entry to `~/.syke/pi-agent/auth.json` with
   `{"type": "api_key", "key": "<actual key>"}` matching the existing `anthropic`
   entry's shape. Smoke on R01 with Opus judge through `azure-anthropic-foundry`
   → 3/3 cells judged cleanly (verdicts: fail/pass/pass).

## The fix — applied in the syke repo at commit 119ca43

Added `azure-anthropic-foundry` to the allowlist in
`syke/llm/pi_client.py::_PROVIDER_HOST_ENV_ALLOWLIST`:

```python
"azure-anthropic-foundry": frozenset(
    {
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_BASE_URL",
    }
),
```

Verified three ways:

1. Direct `curl` with the same key against the Foundry endpoint → 200 OK.
   (Confirmed key + endpoint are fine; only the Pi passthrough was broken.)
2. Smoke with `SYKE_PI_PASSTHROUGH_ENV=AZURE_OPENAI_API_KEY` (the escape-hatch
   env var that dc83d39 also introduced, no code change) → 3/3 Opus cells
   judged cleanly. Proves the env-var-flow hypothesis before we touched code.
3. Smoke with the committed code fix only (no escape hatch, auth.json reverted
   to original) → 1/3 cells judged cleanly mid-run, no 401.

## Earlier workaround (reverted)

Initial suspicion pointed at Pi's credential store as the right place to fix.
The auth.json modification was applied and then reverted once the real upstream
cause was identified. The original `auth.json.bak` was restored cleanly.

## Durable fixes worth considering

1. **Fix Pi's resolver** to throw (or log loudly) when env-var lookup fails,
   instead of silently falling back to the literal string. The silent fallback
   is the real foot-gun — the 401 we saw is *only* informative because Azure
   happened to return a recognizable error body.

2. **Investigate the sandbox env-strip.** `sandbox-exec -f <profile>` on macOS
   typically inherits the parent's env by default; if Syke's profile is doing
   something explicit to restrict env vars, that's where to look. See
   `syke/runtime/sandbox.py::write_sandbox_profile`.

3. **Standardize auth storage on auth.json** for all providers, not env vars.
   The `anthropic` direct provider uses auth.json already; doing the same for
   `azure-anthropic-foundry` (and any other provider that reads from env) would
   eliminate this class of bug entirely.

## Why Apr 20 Opus runs worked

Unknown without deeper inspection. Most likely: either the sandbox profile was
different then, or the env var was already in auth.json for that run, or the Pi
invocation path didn't go through the sandbox for the Apr 20 lane. Worth
checking git history on `syke/runtime/sandbox.py` between Apr 20 and Apr 21.
