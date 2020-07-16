# `rosreestr_loader`

This is script to load data (addresses, coordinates, cadastre IDs, etc) from [Federal service of state registration cadastre and cartography](https://rosreestr.ru/) using API.

## Installation

Script dependencies can be installed using [Poetry](https://python-poetry.org):

```sh
poetry install --no-dev
```

## Usage

### Getting help

```sh
poetry run python ./rosreestr_loader/rosreestr_loader.py --help
```

### Loading addresses

```sh
poetry run python ./rosreestr_loader/rosreestr_loader.py START_ID OUTPUT_DIRECTORY
```

Where `START_ID` is first digits of IDs to begin loading with, `OUTPUT_DIRECTORY` is directory to save result files.

On each request, if there are less entries returned then maximum API limit (200), those entries will be saved to separate file in JSON format. If count of entries is equal to or more than maximum API limit, more narrow requests will be performed. When all data for given subregion is loaded, program quits (subregion is defined by first 4 digits of IDs, for example `50:12` means: Moscow Region, [Mytischi city district](https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%BE%D0%B9_%D0%BE%D0%BA%D1%80%D1%83%D0%B3_%D0%9C%D1%8B%D1%82%D0%B8%D1%89%D0%B8)).

Example (not program output, just description of program execution):

```
Command: python ./rosreestr_loader/rosreestr_loader.py 501200503 ../geodata/rosreestr/data

Loading https://rosreestr.ru/api/online/fir_objects/50:12:00503
Returned 200 entries, using more narrow requests
Loading https://rosreestr.ru/api/online/fir_objects/50:12:005030
Returned 200 entries, using more narrow requests
Loading https://rosreestr.ru/api/online/fir_objects/50:12:0050300
Returned 194 entries, saving to ../geodata/rosreestr/data/addresses-50120050300.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:0050301
Returned 107 entries, saving to ../geodata/rosreestr/data/addresses-50120050301.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:0050302
Returned  14 entries, saving to ../geodata/rosreestr/data/addresses-50120050302.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:0050303
Returned  17 entries, saving to ../geodata/rosreestr/data/addresses-50120050303.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:0050304
Returned  20 entries, saving to ../geodata/rosreestr/data/addresses-50120050304.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:0050305
Returned  20 entries, saving to ../geodata/rosreestr/data/addresses-50120050305.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:0050306
Returned  20 entries, saving to ../geodata/rosreestr/data/addresses-50120050306.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:0050307
Returned  20 entries, saving to ../geodata/rosreestr/data/addresses-50120050307.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:0050308
Returned  20 entries, saving to ../geodata/rosreestr/data/addresses-50120050308.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:0050309
Returned  20 entries, saving to ../geodata/rosreestr/data/addresses-50120050309.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:005031
Returned  54 entries, saving to ../geodata/rosreestr/data/addresses-5012005031.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:005032
Returned  54 entries, saving to ../geodata/rosreestr/data/addresses-5012005032.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:005033
Returned  99 entries, saving to ../geodata/rosreestr/data/addresses-5012005033.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:005034
Returned  54 entries, saving to ../geodata/rosreestr/data/addresses-5012005034.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:005035
Returned  54 entries, saving to ../geodata/rosreestr/data/addresses-5012005035.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:005036
Returned  10 entries, saving to ../geodata/rosreestr/data/addresses-5012005036.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:005037
Returned  54 entries, saving to ../geodata/rosreestr/data/addresses-5012005037.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:005038
Returned  54 entries, saving to ../geodata/rosreestr/data/addresses-5012005038.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:005039
Returned  54 entries, saving to ../geodata/rosreestr/data/addresses-5012005039.json
Loading https://rosreestr.ru/api/online/fir_objects/50:12:00504
Returned  78 entries, saving to ../geodata/rosreestr/data/addresses-501200504.json

...


Loading https://rosreestr.ru/api/online/fir_objects/50:12:9
Returned  175 entries, saving to ../geodata/rosreestr/data/addresses-50129.json

Finished
```

If program crashes, for example, due to network issues, user can copy ID from last loaded file name and pass it as `START_ID` parameter when starting script again to continue from last file.
