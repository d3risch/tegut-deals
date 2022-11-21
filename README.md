Running the download-action results in an artifact which holds the leaflet pdf.

Default location is Frankfurt but if you want to get your local leaflet just use a PLZ as an argument. To run locally on a basic Ubunutu version check first if your installed chrome version already works if not use:
```
sudo apt purge google-chrome-stable
sudo apt purge chromium-browser
sudo apt install -y chromium-browser
pip install -r requirements.txt
python ./headless/chromium-headless.py $LOCAL_PLZ
```

For scheduled downloading add the following to main.yml using [POSIX cron syntax](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07):
```
on:
  schedule:
    # * is a special character in YAML so you have to quote this string
    - cron:  '* * * * *'
```
