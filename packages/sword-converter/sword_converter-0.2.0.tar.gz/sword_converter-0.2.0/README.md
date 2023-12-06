# SWORD Converter

[![Test](https://github.com/evnskc/sword-converter/actions/workflows/test.yml/badge.svg)](https://github.com/evnskc/sword-converter/actions/workflows/test.yml)
[![Publish](https://github.com/evnskc/sword-converter/actions/workflows/publish.yml/badge.svg)](https://github.com/evnskc/sword-converter/actions/workflows/publish.yml)
[![PyPI](https://img.shields.io/pypi/v/sword-converter)](https://pypi.org/project/sword-converter/)

## Generate JSON Files of Bible Texts from SWORD Modules

The [SWORD project provides modules](http://crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles) freely for common
Bible translations in different languages.

### Sample Output

#### _1. JSON_

```json
{
  "name": "King James Version (1769) with Strongs Numbers and Morphology  and CatchWords",
  "abbreviation": "KJV",
  "books": {
    "ot": [
      {
        "number": 1,
        "name": "Genesis",
        "abbreviation": "Gen",
        "chapters": [
          {
            "number": 1,
            "verses": [
              {
                "number": 1,
                "text": "In the beginning God created the heaven and the earth."
              }
            ]
          }
        ]
      }
    ],
    "nt": [
      {
        "number": 40,
        "name": "Matthew",
        "abbreviation": "Matt",
        "chapters": [
          {
            "number": 1,
            "verses": [
              {
                "number": 1,
                "text": "The book of the generation of Jesus Christ, the son of David, the son of Abraham."
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### Installation

Using `pip`

```commandline
pip install sword-converter
```

Using `poetry`

```commandline
poetry add sword-converter
```

### Usage

Output file will be saved in the same directory as the sword module.

```text
sword-converter source module
```

```commandline
sword-converter /home/user/Downloads/KJV.zip KJV
```