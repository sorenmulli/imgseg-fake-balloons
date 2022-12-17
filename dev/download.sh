# This command comes from https://medium.com/geekculture/wget-large-files-from-google-drive-336ba2e1c991
echo "Downloading Fake Balloons Perlin..."
wget --load-cookies /tmp/cookies.txt\
    "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate\
    'https://docs.google.com/uc?export=download&id=1k6ikalUtzpYARzGTrxpVCvUwmP9_EJ9W' -O-\
    | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1k6ikalUtzpYARzGTrxpVCvUwmP9_EJ9W" -O perlin.zip\
    && rm -rf /tmp/cookies.txt

echo "Downloading Fake Balloons Sparce Convolution ..."
wget --load-cookies /tmp/cookies.txt\
    "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate\
    'https://docs.google.com/uc?export=download&id=1psLKuoBt9Ai_bP9zxUFJ_OeGAyxa1jm-' -O-\
    | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1psLKuoBt9Ai_bP9zxUFJ_OeGAyxa1jm-" -O sc.zip\
    && rm -rf /tmp/cookies.txt
