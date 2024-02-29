# Quick Start Guide

Run `make` from the top directory. This will bring up a Docker stack with an app server
listening on <http://127.0.0.1:8000>.

Click the `Admin` link, login as `admin` with password `admin`, then go to any fact model page
(like `Posts` or `Comments`) and press `IMPORT FROM JPH` button.

When the import is finished, you will see some records imported from the fake API.
After 10 minutes or so you will notice a record in the `SyncLog` model indicating that the initial sync
has completed. In case all components are functioning properly, the records will have `success` flag set
and `end date` field filled in. The count field should indicate around 600 records, because the initial sync
pushes all records to the slave system.

Now modify at least one of the `Post` or `Comment` records and save them.
Some 10 minutes later you will notice another `SyncLog`
records, with `count` field equal to the number of records you've modified.

This completes the initial smoke test of the system.