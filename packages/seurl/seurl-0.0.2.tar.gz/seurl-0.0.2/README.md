# seurl

Retrieve domain URLs from Search Engines

## Usage

Specify one or several domains by stdin:
```
$ echo gitlab.com | seurl
https://status.gitlab.com/
https://design.gitlab.com/
https://gitlab.com/piveau
https://gitlab.com/dnsmichi
...
```

You can also combine it with other tools:
```
$ echo gitlab.com | seurl | urld -f domain
ERROR:seurl.__main__:Captcha in Duckduckgo
status.gitlab.com
design.gitlab.com
gitlab.com
gitlab.com
about.gitlab.com
...
```


## Supported Search Engines

- Bing
- Duckduckgo
- Ecosia
- Google
