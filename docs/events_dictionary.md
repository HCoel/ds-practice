# Events Dictionary — `events_28d.parquet`

One row per user-facing browser event, last 28 days, staff accounts removed.

## Columns

| Name | Type | PostHog source | Meaning | Nulls when |
|---|---|---|---|---|
| `event_id` | `String` | `uuid` | Unique PostHog event ID | Never |
| `ts` | `Datetime[us, UTC]` | `timestamp` | When the event fired, stored in UTC | Never |
| `person_id` | `String` | `person_id` | PostHog person UUID (stitched across sessions) | Never |
| `event` | `String` | `event` | Event name — `$pageview` or `billing.<action>` | Never |
| `org_id` | `Int64` | `properties.org_id` | BuiltGrid organisation ID | Anonymous / unauthenticated visitors |
| `plan` | `String` | `properties.plan` | Subscription plan at time of event | Almost always — only set on certain billing events |
| `host` | `String` | `properties['$host']` | Hostname the event came from | Never (filtered in SQL) |
| `pathname` | `String` | `properties['$pathname']` | URL path at time of event | Never |

## Filters and why

| Filter | SQL clause | Reason |
|---|---|---|
| 28-day window | `timestamp >= now() - toIntervalDay(28)` | Keeps dataset small; rolling window for weekly analysis |
| Browser events only | `properties['$lib'] = 'web'` | Excludes server-side and mobile SDK events that lack page context |
| Staff removed | `person.properties.email NOT ILIKE '%@builtgrid.com%'` | Prevents internal usage inflating product metrics |
| Known hosts only | `properties['$host'] IN ('app.builtgrid.com', 'builtgrid.com')` | Removes bot traffic and GTM preview hits (e.g. `gtm-msr.appspot.com`) that pass the lib filter |
| User-facing events only | `event = '$pageview' OR event LIKE 'billing.%'` | Excludes internal instrumentation events not relevant to product analysis |
