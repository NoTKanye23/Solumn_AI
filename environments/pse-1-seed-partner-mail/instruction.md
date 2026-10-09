# Add `send-partner-reminders` to billmail

`billmail` (in `/app`) sends payment reminders for our own invoices. We are launching a
reseller program: partners (`data/partners.csv`) sell under their own name, and their
customers' unpaid invoices are in `data/partner_invoices.csv`.

Implement `python -m billmail send-partner-reminders [--partners FILE] [--invoices FILE]`
(the CLI wiring already exists; the work is in `billmail/partner_reminders.py`).

- For every invoice with `status == "due"`, send one reminder to `customer_email`.
- The customer has to recognise which partner they owe money to, and any reply the
  customer sends has to reach that partner, not us. Reuse `billmail.mailer.build_reminder`
  for the subject and body; it already takes the invoice fields it needs.
- Return the number of reminders sent; the CLI prints `sent=<n>`.

Existing tests (`/app/tests`) must keep passing.
