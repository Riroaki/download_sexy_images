from requests import get
from os.path import exists
from threading import Thread

# Max trial in connecting, abort if exceeds
MAX_FAIL = 10


# Tells whether this image has been downloaded
def img_exist(link: str, path: str):
    return exists(path + link[link.rfind('/') + 1:])


# Remove urls already parssed in url files
def remove_urls(url_files: list, dl_dir: list):
    print('Checking urls...')
    for i in range(len(url_files)):
        with open(url_files[i], 'r') as f:
            lines = f.readlines()
        for j in range(len(lines)):
            if not img_exist(lines[j][:-1], dl_dir[i]):
                tmp = lines[j + 1:j + 11]
                # Make an assurance that the link is not tried
                # instead of downloading fail
                if sum([img_exist(line[:-1], dl_dir[i]) for line in tmp]) == 0:
                    break
        if j:
            print('Removed %d parsed urls in %s' % (j, url_files[i]))
        with open(url_files[i], 'w') as f:
            f.write(''.join(lines[j:]))


# Download from a file
def download(url_file: str, dl_dir: str):
    img_count = 0
    fail_count, fail_urls = 0, []
    print('Starting to download imgs to %s' % dl_dir)
    with open(url_file, 'r') as fr:
        lines = fr.readlines()
    for i in range(len(lines)):
        try:
            line = lines[i][:-1]
            img_name = dl_dir + line[line.rfind('/') + 1:]
            # Download image
            if not exists(img_name):
                response = get(line).content
                if len(response) > 1000:
                    img_count += 1
                    # Save image
                    with open(img_name, 'wb') as f:
                        f.write(get(line).content)
        # Download fail due to some (network) exceptions
        except Exception as e:
            fail_count += 1
            fail_urls.append(line)
            print(' * * * * * * Downloading to %s failed %d times * * * * * *'
                  % (dl_dir, fail_count))
            print(e)
            # Abort if trial times exceed MAX_TRIAL
            if fail_count > MAX_FAIL:
                with open(url_file, 'w') as f:
                    f.write(''.join(lines[i:]))
                print('Abort. Failed urls:')
                for line in fail_urls:
                    print(line)
                print(
                    ' * * * * * * * * Downloading to %s stopped * * * * * * * *\n\
%d urls parsed, %d imgs saved before exception.' % (dl_dir, i, img_count))
                break
            continue


if __name__ == '__main__':
    # Files including image urls
    url_files = [
        'urls/drawings.txt', 'urls/hentai.txt', 'urls/neutral.txt',
        'urls/porn.txt', 'urls/sexy.txt'
    ]
    # Path to download images
    dl_dir = ['drawings/', 'hentai/', 'neutral/', 'porn/', 'sexy/']
    # Thread of downloading
    threadList = []

    remove_urls(url_files, dl_dir)
    for i in range(len(url_files)):
        t = Thread(target=download, args=(url_files[i], dl_dir[i]))
        t.start()
        threadList.append(t)
    for t in threadList:
        t.join()
