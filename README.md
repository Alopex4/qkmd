# [qkmd](#qkmd)

Quick markdown what you need, just via a link.

## [Getting Started](#Getting-Started)

Have you ever try to stored the link(URL) in `.txt` to browse it one day later or few months after? But when you open the file again, muttering to yourself 'What do I store for this?'

Have you learn `markdown` syntax, but get bored to use it to record the link(URL) by press the `[]` and `()` ?

The `qkmd` is for you, you can just give it a link(URL) then the webpage title will be extract, format to a `[title](http://example.com)` pattern. Also you can customize the title what you like, append timestamp, append code snip ...

## [Prerequisites](#Prerequisites)

If you live in the [resource blocked area](https://www.wikiwand.com/en/Great_Firewall) or [Internet censorship area](https://www.wikiwand.com/en/Internet_censorship) , please consider setting a proxy first.

1. Install the porxy software, assure you can use browser to open the webpage

2. Install `polipo`

    ```bash
    $ ## Ubuntu / Debian
    $ sudo apt-get update
    $ sudo apt-get install polipo
    ```

    ```bash
    $ ## redhat / CentOS
    ```
    >[Polipo installation instructions](https://www.irif.fr/~jch/software/polipo/INSTALL.text)
3. Export the proxy
    ```bash
    export https_proxy=http://127.0.0.1:8123
    export http_proxy=http://127.0.0.1:8123
    ```

The `qkmd` default proxy port number is 8123.

## [Installing](#Installing)

Assure you python version is >= 3.4
```bash
$ pip install qkmd
```
or

```bash
$ python3 setup.py install
```
or

```bash
$ python setup.py install
```

## [Usage](#Usage)
```
usage: qkmd.py [-h] [-d] [-v] [-c [comment [comment ...]]] [-l language]
               [-s source-code-file] [-C] [-t [title [title ...]]]
               [-o output-file] [-P]
               [link]

Quickly formatting markdown `link`, convenient your daily life/work.

positional arguments:
  link                  generate the markdown format link

optional arguments:
  -h, --help            show this help message and exit
  -d, --date            append `RFC 2822` date format
  -v, --version         display current version of `qkmd`
  -c [comment [comment ...]], --comment [comment [comment ...]]
                        give the link a simple comment
  -l language, --language language
                        specific the code language
  -s source-code-file, --source source-code-file
                        give the source code snip file
  -C, --color           source code syntax hightline
  -t [title [title ...]], --title [title [title ...]]
                        add title manually
  -o output-file, --save output-file
                        save the markdown to a file
  -P, --print           turn off print the markdown format in screen
```

Here is a simple way to reduce your time and simplify your operation.  
Assure you always want to store the file to `$HOME/mark.md` and highlight the code

```bash
alias mark='function mark(){ qkmd $* -o ~/mark.md -C;}; mark'
```

## [Authors](#Authors)

* **alopex cheung** [@alopex](mailto:alopex4@163.com)

## [License](#License)

* This project is licensed under the MIT License - see the [LICENSE](https://github.com/Alopex4/qkmd/blob/master/LICENSE) file for details
