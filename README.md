# google-csv-to-abx-converter [![Flattr this][flatter_png]][flatter]

Convert Google contact export to ABX format.

## Usage

1. Install `python`, and `make`, if needed.

2. Clone the repo:
	````bash
	git clone git@github.com:rasa/google-csv-to-abx-converter
	````

3. Visit https://takeout.google.com/

4. Click [Deselect All]

5. Check [Contacts]

6. Click [vCard Format]

7. Select [CSV]

8. Click [OK]

9. Scroll down and click [Next Step]

10. Click [Create archive]

11. Unzip the archive into the google-csv-to-abx-converter folder

12. Run:
	````bash
	$ cd google-csv-to-abx-converter
	$ python google-contacts-to-abx.py takeout-20190328T195144Z-001
	````

13. The file `takeout-20190328T195144Z-001/Takeout/Contacts/All Contacts/All Contacts.abx` will be generated containing all contacts that have an address

## Contributing

To contribute to this project, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Bugs

To view existing bugs, or report a new bug, please see [issues](../../issues).

## Changelog

To view the version history for this project, please see [CHANGELOG.md](CHANGELOG.md).

## License

This project is [MIT licensed](LICENSE).

## Contact

This project was created and is maintained by [Ross Smith II][] [![endorse][endorse_png]][endorse]

Feedback, suggestions, and enhancements are welcome.

[Ross Smith II]: mailto:ross@smithii.com "ross@smithii.com"
[flatter]: https://flattr.com/submit/auto?user_id=rasa&url=https%3A%2F%2Fgithub.com%2Frasa%2Fgoogle-csv-to-abx-converter
[flatter_png]: http://button.flattr.com/flattr-badge-large.png "Flattr this"
[endorse]: https://coderwall.com/rasa
[endorse_png]: https://api.coderwall.com/rasa/endorsecount.png "endorse"

