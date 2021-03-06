# Out-of-stock parser
Small Parser with a bit config for checking if an item at https://www.carlroth.com is out of stock

The parser simply fetches the html code from a desired url and checks if it includes a desired substring that indicates that the item is out of stock. If the substring is not contained within the html code, a mail is send to a set of predefined mailadresses.

Sender, receivers, mailserver and the observed url can be configured in a ```config.json``` with the following format:

```
{
  # username for logging into the mail account for sending a mail
  "mailuser": "parser@example.com",
  # password for the mail account
  "password": "secret",
  # mail that is put in the 'From:' field of the mail
  "sender": "parser@example.com",
  # list of receivers that the mail will be sent to 
  "receivers": ["user1@example.com", "admin@nsa.gov"],
  # url (or IP) of the smtp endpoint of the mail server. without "smtp." prefix!
  "smtphost": "example.com",
  # port of the smtp server. Usually 465 or 587
  "port": "465",
  # desired url of an item that is currently out of stock 
  "targetUrl": "https://www.example.com"
}
```

## Requirements
Python3 and access to a mail account

## Usage
setup the config.json as described above. Then simply execute the ```out-of-stock-parser.py```
