# DB
Not included in the repository. TODO: add creation steps here.

Dates are stored in the format 2023-08-12 (ISO 8601) which can be obtained via ``str(datetime.datetime.today().date())`` or ``new Date().toISOString().split('T')[0]``.
Times are stored in the format which can be obtained via ``str(datetime.datetime.today())``.

# Tables
## journalentries
``CREATE TABLE `journalentries` (`date` date not null primary key default CURRENT_DATE, `body` text not null);``
- date date not null primary key default CURRENT_DATE
- body text not null
In the body, stores an entry for a daily mood evaluation. Sometimes referred to as mood description.

## taskclasses
## taskinstances