*Domain Finder*

Domain Finder is a command line tool that finds available domain names that match a given pattern and TLD. It uses regular expressions to match domain names and can output the results to a file.

*Usage:*

To use Domain Finder, run the following command:
```
domainfinder <pattern> <tld> <output_file>
or
domainfinder '^[a-z-]{2}$' ma  output_file.txt 
```
Where `<pattern>` is the regular expression pattern for domain names, `<tld>` is the domain extension name (e.g., `.com`), and `<output_file>` is the name of the output file.

*Options:*
Domain Finder supports the following options:

- `-h, --help`: Show the help message and exit.

*Contributing:*
Contributions to Domain Finder are welcome! If you want to add a feature, fix a bug, or improve the documentation, please submit a pull request.

*License:*
Domain Finder is licensed under the MIT license. See the LICENSE file for details.

