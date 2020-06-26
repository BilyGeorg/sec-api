# Process SEC API

* The data is extracted from [SEC API](https://sec-api.io) – it has a free tier that can be used for the
purpose of this test. The API also has sandbox environment and documentation section.

* Please place your API key in `credentials.json`

* Please amend `quey.json` as required. At the moment, it is set-up for Form D and Form D/A only for the current month (June 2020). The query and the time period are adjustable. If necessary, these changes could offer room for improvement in the scripts, `api.py`in particular.

* Run `api.py`. This script takes 'filename' and 'max_calls' as arguments. The output is written to a source file.

* Run `sec.py`. This script goes to the SEC 'linkToFillingDetails' page, extracts additional data, and appends the columns 'Year of Incorporation/Organization', 'City', and 'Industry Group' to the output file. It takes 'in_filename' and 'out_filename' as arguments.

* Run `index.py`. This script applies additional filters on the data, such as:

> companies incorporated in the current year
> belonging to any type of Pooled Investment Fund (Industry Group) except Other Investment Fund.
> limited to Form D and Form D/A filings made in the current month.

The script takes 'in_filename' and 'out_filename' as arguments. It also applies the transformations necessary to prepare and save the final data in the required format.

