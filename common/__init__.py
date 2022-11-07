def bytes_to_image_tag(img_bytes,format):
    import base64
    b64content = base64.b64encode(img_bytes).decode('utf-8')
    return f"<img src='data:image/{format};base64,{b64content}'/>"

def alert_new_release():
    import os, sys, requests, json, time
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    try:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../VERSION'), 'r') as f:
            version_current = json.load(f)
            tag_ref = version_current['tag_ref']
            tag_current = version_current['tag_val']
            upgrade_url = version_current['upgrade_url']
            response = requests.get(tag_ref)
            tag_latest = response.json()["tag_name"]

            if tag_latest != tag_current and tag_latest != 'placeholder':
                print(f"{WARNING}IMPORTANT:{ENDC}{BOLD}A newer version of this project is available! The latest version is {tag_latest}.{ENDC}", file=sys.stderr)
                print(f"{BOLD}Visit {upgrade_url} to upgrade.{ENDC}", file=sys.stderr)
                time.sleep(5)
    except KeyboardInterrupt:
        sys.exit()
        pass
    except Exception as e:
        print(f"{BOLD}Error occured checking for upgrades{ENDC}", file=sys.stderr)
