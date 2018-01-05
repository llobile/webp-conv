# webp-conv

This simple Python 2.6 script converts any `png`, `jpg` or `jpeg` image to a `webp` image, using Google's [cwebp](https://developers.google.com/speed/webp/) tool.

### Usage

```shell
$ webp-conv -s /path/to/desired/directory -q 80 --remove
```

`-s` denotes the source directory and points to the current working directory by default.
`-q` denotes the compression factor for RGB channels, 80 by default.
`--remove` removes the original file, once successfully converted. If not provided, the original will **not** be removed.

### License

    Copyright 2017 llobile

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
