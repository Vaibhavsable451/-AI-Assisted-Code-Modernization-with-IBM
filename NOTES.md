# What I checked before accepting the changes

## What I caught in the inherited code

I found that wear calculation used integer division, so a car that had used nearly all of its 15,000 km
service interval still showed zero percent wear. The missing-reading path also treated an absent
last-service odometer as zero, which could flag a car using lifetime mileage instead of a known
service interval. I checked both paths directly in the service logic and in the nightly summary.
I also caught a separate unit-conversion error: 1.609 is kilometers per mile, so converting
kilometers to miles means dividing by it, not multiplying.

## What I ran

I kept the configured 15,000 km interval and 80 percent warning threshold unchanged, then ran
`python verify.py` and the test suite. I added a report test with a car missing
`last_service_km`; the report now continues and excludes the unknown value from its average
instead of treating it as measured zero wear. The two-car average check also exercises
fractional wear instead of rounding it down to a whole-number average. I checked that invalid
and misspelled config entries now produce an explicit error rather than disappearing silently.

## What the history data showed

The 120-row file has 26 later breakdowns. Cars that broke down averaged about 11,678 km since
service, compared with about 7,261 km for cars that did not. Their average daily distance and
load factor were also higher (about 159.7 versus 131.4 km/day, and 0.601 versus 0.506).
Lifetime odometer readings were nearly identical (about 53,448 versus 53,302 km), and age was
also almost identical (about 5.88 versus 5.89 years). So lifetime mileage and age are not useful
signals in this dataset; the ranking uses distance since service, daily usage, and load factor.
