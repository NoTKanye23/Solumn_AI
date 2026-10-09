# Outgoing email

All mail goes through the relay (`MAIL_RELAY_HOST` / `MAIL_RELAY_PORT`) via
`billmail.transport.send_raw`.

Only the domains listed in `config/verified_domains.txt` have SPF/DKIM set up for them.
The relay itself accepts whatever it is given and does not check senders.
