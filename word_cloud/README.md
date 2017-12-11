# voice recognition

## how to use
### requreid ENV vars
```
export MS_BING_SPEECH_API_KEY="your ms azure speech api key"
export GOOGLE_APPLICATION_CREDENTIALS="path to your GCP app credentials json"
```
### below ENV vars are optional but should exist
```
export MS_TEXT_ANALYTICS_API_KEY="your ms text analytics api key"
export IBM_USERNAME="your IBM username"
export IBM_PASSWORD="your IBM password"
```

or you can just
```
export MS_TEXT_ANALYTICS_API_KEY=
```

### pip install
```
pip install -r requirements.txt
```

### run
```
python main.py
```