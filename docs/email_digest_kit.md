# Kit Digest Setup

The scanner creates a Kit broadcast for stocks whose daily cloud count is 1 and
weekly cloud count is greater than 0. Kit manages subscriber consent,
unsubscription, and broadcast delivery. The scanner does not store subscriber
email addresses.

## Kit configuration

1. Create a Kit form or landing page for the Cloud Signal digest. Configure it
   for confirmed opt-in and apply a dedicated tag to subscribers.
2. Copy the tag ID from Kit and create an API key with permission to create
   broadcasts.
3. Set `KIT_API_KEY` and `KIT_DIGEST_TAG_ID` in the environment used to run the
   scanner. The broadcast is restricted to that tag; it will not target the
   entire Kit account.

## Run

With the repository virtual environment active in PowerShell:

```powershell
$env:KIT_API_KEY = "your-kit-api-key"
$env:KIT_DIGEST_TAG_ID = "123456"
python -m cloud_signal.runners.main
```

The full runner scans enabled markets and schedules a broadcast after the scan
finishes. To schedule from CSV results already in `output/cloud`, run:

```powershell
python -m cloud_signal.runners.send_email_digest
```

Kit's API key is private. Keep it in the scheduled task's environment or a
secret manager; never place it in a GitHub Pages JavaScript bundle or commit it
to the repository. `KIT_SEND_DELAY_MINUTES` controls the short delay before Kit
sends the broadcast and defaults to `10` minutes. `EMAIL_DIGEST_MARKETS` can
limit the scan to a comma-separated set of equity market names.

The local `instance/kit_digest_deliveries.sqlite3` database prevents scheduling
the same digest date twice. Keep this file persistent between runs. Set
`DIGEST_STATE_DB` to another persistent path if needed.

GitHub Pages can link to Kit's hosted form or embed Kit's form. It remains a
static site; Kit handles the subscription form and subscriber list.