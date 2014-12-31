## wkhtmltopdf as a webservice

This app create pdf from html source uses wkhtmltopdf cli tool

First of all you need to cli tool with dependencies. follow the commands,


Install Xvfd:
```
sudo apt-get install xvfb
```

Install Fonts:
```
sudo apt-get install xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic
```

Install wkhtmltopdf
```
sudo apt-get install wkhtmltopdf
```

Python Flask
```
pip install -r requirements.pip
```

__run :__
python pdfservice.py

## Usage
Send your html content to yourip:port/makepdf end point in raw_body

## Tip
You can change ip/port in pdfservice.py on line 6

## P.S.
Osx doesn't support yet