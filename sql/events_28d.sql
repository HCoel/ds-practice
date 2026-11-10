-- One row per user-facing event, last 28 days, staff accounts removed
SELECT
    uuid AS event_id,
    timestamp AS ts,
    person_id,
    event,
    properties.org_id AS org_id,
    properties.plan AS plan,
    properties['$host'] AS host,
    properties['$pathname'] AS pathname
FROM
    events
WHERE
    timestamp >= now() - toIntervalDay (28)
    AND timestamp < now()
    AND properties['$lib'] = 'web' -- browser events only
    AND properties['$host'] IN ('app.builtgrid.com', 'builtgrid.com')
    AND (
        event = '$pageview'
        OR event LIKE 'billing.%'
    )
    AND coalesce(person.properties.email, '') NOT ILIKE '%@builtgrid.com%'
ORDER BY
    ts
LIMIT
    50000