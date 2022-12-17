# This command comes from https://medium.com/geekculture/wget-large-files-from-google-drive-336ba2e1c991
echo "Downloading Fake Balloons Perlin..."
wget --load-cookies /tmp/cookies.txt\
    "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate\
    'https://docs.google.com/uc?export=download&id=FILEID' -O-\
    | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O perlin.zip\
    && rm -rf /tmp/cookies.txt

echo "Downloading Fake Balloons Sparce Convolution ..."
wget --load-cookies /tmp/cookies.txt\
    "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate\
    'https://docs.google.com/uc?export=download&id=FILEID' -O-\
    | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O sc.zip\
    && rm -rf /tmp/cookies.txt
