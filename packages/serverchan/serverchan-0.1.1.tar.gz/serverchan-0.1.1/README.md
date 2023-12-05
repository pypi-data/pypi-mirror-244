📦 serverchan (for ftqq)
=======================

简单封装[ftqq]提供的api，仓库地址 [serverchan] 

`非官方版本，具体可以查看仓库源码`

参考具体用法官方API

目的在于方便脚本调用，减少重复代码

[Check out the example!][serverchan]

Installation
-----

```bash
pip install serverchan
```

demo
```python
from serverchan import ServerChan
from serverchan.channel import Channels

# secret = 'SCU114xxxxx'
secret = 'SCTxxxx'
serverchan = ServerChan(secret)
response = serverchan.push(title="test", desp='just for test')
print(response.text)
print(response.text.encode().decode('unicode_escape'))

response = serverchan.push(title="test1", desp='just for test1', channel='{}|{}'.format(Channels.WECHAT_SERVICE_ACCOUNT, Channels.PUSHDEER))
print(response.text)
print(response.text.encode().decode('unicode_escape'))


```

To Do
-----

-   Tests via `$ setup.py test` (if it's concise).

Pull requests are encouraged!

More Resources
--------------

-   [What is setup.py?] on Stack Overflow
-   [Official Python Packaging User Guide](https://packaging.python.org)
-   [The Hitchhiker's Guide to Packaging]
-   [Cookiecutter template for a Python package]

License
-------
agpl-3.0

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

  [ftqq]: https://sct.ftqq.com/
  [serverchan]: https://github.com/anysoft/serverchan
  [PyPi]: https://docs.python.org/3/distutils/packageindex.html
  [Twine]: https://pypi.python.org/pypi/twine
  [image]: https://farm1.staticflickr.com/628/33173824932_58add34581_k_d.jpg
  [What is setup.py?]: https://stackoverflow.com/questions/1471994/what-is-setup-py
  [The Hitchhiker's Guide to Packaging]: https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html
  [Cookiecutter template for a Python package]: https://github.com/audreyr/cookiecutter-pypackage
