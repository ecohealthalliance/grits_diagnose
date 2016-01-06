This plugin serves the `/diagnose` endpoint from [grits-api](https://github.com/ecohealthalliance/grits-api)
through a [girder](https://github.com/girder/girder) plugin.  It relies on the following commit from
the grits-api repository:
[3d2b31eb3564abbac550291829478055bb58409a](https://github.com/ecohealthalliance/grits-api/commit/3d2b31eb3564abbac550291829478055bb58409a)

To use the plugin, you must include the path to your local `grits-api` install (including all dependencies)
in your python path prior to starting girder.  I.e.
```
PYTHONPATH=$HOME/grits:$HOME/grits/annie python -m girder
```

The plugin endpoint is served as: `POST /grits/diagnose`.  See the swagger api docs at
[http://localhost:8080/api/v1#!/grits](http://localhost:8080/api/v1#!/grits).

## License
Copyright 2016 EcoHealth Alliance

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
