import os
import requests
import urllib.request
from datetime import datetime

# -------- CONFIG ------------------
# Get your user ID from the "view as visitor link (https://www.midjourney.com/app/users/.../) on your Midjourney gallery
USER_ID = "831784424554627072"
# In your browser's dev tools, find the `__Secure-next-auth.session-token` cookie.
SESSION_TOKEN = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..iZ9VXYbzGGUEcoAf.cLzPbQbQWcb39VyIwceMYQ50q1ZfAwBVpjCj18gc6PF5OPtql4JxlOuhetc-hOdavPHgRTMk1vLKrZqfMW9eBoVZnVSW_JUpZOsdPIaQmipMDEkJ2WHNyJi-JcU72yLpx6lOioGiWHJXhXRlJOj-pFYIYleC6iDSu761MoEintIra_JQU8kd923dfTPYjKgziazHs3PBQ0ncPw3sEmqG9JjyElrpCe2VJfwC4YSkni_6zLx6MZ2236ngh7cwbn3CLJmtP8vP10nhIeWynzfsjjwHuQYGi-KeLmb8pBqLQj0Kc0RHf6qBfRwME_bsCkvnxyv-tWUcfrWmCMwzQcGiILHst3jurpe6moBs0Ah_ioth8XMPjQxvxt0ftDB_J1xEqGWR7DAXi_oebFtUiXq3UralsSl6LAeEgcMYgiW-7pQiAU-vj5G3CwlhiPsDc0FIpIG23HAIKbP6rzzDNFKylQea8_gRQBFTQ9uER7WkqVaAMYh4HAplT-S52OxiV-dGZyZ2sLetbElGsgvcCtzNsUT2AjFtL-HaGhpnCaLXAqnIBVaeYQwKrvSni4ITwjloIoUotW6S0HGjejk1iojfyggpkRQpuR_N0_ph8U8o5e6Y0etRgKnMgeQImuDWAcvBT7P125ORIKsgQZ7ARLZIuJ5xrqtb-nhKXa6WVDKax7DXVw1ESsM4o3WNiM1DbQJQ0TS6GcBHl9auD3pNz0cE38zV9_KvBX-O7U2XkHoPqd5K2ZYhpSZEQt8EKsNrqx5L4Mv3sgkslTu9ga7-fU1HlwMHiD8pA69VcuG6gDWx24CoKSfz4h2hsagRyuRccOU-ORW281TU4yCr0NU5PVbgDef3tKGHy_ZZ2PlnDAB_egj0BGP28NIeWn5F_PSm1tf4HWV1g2hWn1WZm_J2VOuCRR_YeZveTaG6iNXF6rBZn7SAgI17qzl8WHp4LlQJvxt78Be-1vIyHswYWp5LIjazC3U71Kk76X2L22J1gx9CqIIgF891hubTUCb5jSeDAlfIhD_kf08Rjs0msgnTaLQl0XJ9puOaBhYqhXStLFwb85kvluD5GzDXCM_nSwueQtCn7bgfn0xGqPKrr0QEjKlhpPGRFwZg1erfevZMoTLnOGYx_QwQcr33w31z2U4dPciMFC70ioKmqFKKe0Ydf1mol5AGzJszpi444BDY1sJP-UvvzvaeNm88oqI2ejcP2wOIr1jF3ltQZnoUO1KNr8T0HHcRImrBWDwLdU2GKlN6s_VdDgFGAJtqeeAQ5jvjpCVAdzVuCmnrN_y6Gp3WzJyB8bq-SGfmoDy6EPRSOqa618B3Zp28AIIfMFclhBKIhRe8JJJZZAIVtpe8Tfb56CJcJMMI0AZEDDp_mlAgeyA2Iy_Q-IYMuW_hQ-g-NzVMPKElOb7Fpzxr8SaQHbcUoehDUE89QsZ6ll6nkHWnrqw5lnrk5d_Gp14Yk1JIcbcVpBnqXE4jGEryNLonU_X9SepI01FGLA.NYAkjCYZIqat7WBjsPxBfw"
# ---------------------------------


# ------- OPTIONS -----------------
UPSCALES_ONLY = False
GRIDS_ONLY = True
USE_DATE_FOLDERS = True
GROUP_BY_MONTH = True
SKIP_LOW_RATED = False
# ---------------------------------

UA = 'Midjourney-image-downloader/0.0.1'
HEADERS = {'User-Agent': UA}
COOKIES = {'__Secure-next-auth.session-token': SESSION_TOKEN}
ORDER_BY_OPTIONS = ["new", "oldest", "hot", "rising", "top-today", "top-week", "top-month", "top-all", "like_count"]


def get_api_page(order_by="new", page=1):
    api_url = "https://www.midjourney.com/api/app/recent-jobs/" \
              f"?orderBy={order_by}&jobStatus=completed&userId={USER_ID}" \
              f"&dedupe=true&refreshApi=0&amount=50&page={page}"
    if UPSCALES_ONLY:
        api_url += "&jobType=upscale"
    elif GRIDS_ONLY:
        api_url += "&jobType=grid"

    print(f"API URL = {api_url}")
    response = requests.get(api_url, cookies=COOKIES, headers=HEADERS)
    result = response.json()
    return result


def download_page(page):
    for idx, image_json in enumerate(page):
        filename = save_prompt(image_json)
        if filename:
            print(f"{idx+1}/{len(page)} Downloaded {filename}")


def ensure_path_exists(year, month, day, image_id):
    if USE_DATE_FOLDERS:
        if not os.path.isdir(f"jobs/{year}"):
            os.makedirs(f"jobs/{year}")
        if not os.path.isdir(f"jobs/{year}/{month}"):
            os.makedirs(f"jobs/{year}/{month}")
        if GROUP_BY_MONTH:
            if not os.path.isdir(f"jobs/{year}/{month}/{image_id}"):
                os.makedirs(f"jobs/{year}/{month}/{image_id}")
            return f"jobs/{year}/{month}/{image_id}"
        else:
            if not os.path.isdir(f"jobs/{year}/{month}/{day}"):
                os.makedirs(f"jobs/{year}/{month}/{day}")
            if not os.path.isdir(f"jobs/{year}/{month}/{day}/{image_id}"):
                os.makedirs(f"jobs/{year}/{month}/{day}/{image_id}")
            return f"jobs/{year}/{month}/{day}/{image_id}"
    else:
        if not os.path.isdir(f"jobs/{image_id}"):
            os.makedirs(f"jobs/{image_id}")
        return f"jobs/{image_id}"


def save_prompt(image_json):
    image_paths = image_json.get("image_paths", [])
    image_id = image_json.get("id")
    prompt = image_json.get("prompt")
    enqueue_time_str = image_json.get("enqueue_time")
    enqueue_time = datetime.strptime(enqueue_time_str, "%Y-%m-%d %H:%M:%S.%f")
    year = enqueue_time.year
    month = enqueue_time.month
    day = enqueue_time.day

    filename = prompt
    #.replace(" ", "_").replace(",", "").replace("*", "").replace("'", "").replace(":", "").replace("__", "_").replace("<", "").replace(">", "").replace("/", "").replace(".", "").lower().strip("_*")[:100]

    ranking_by_user = image_json.get("ranking_by_user")
    if SKIP_LOW_RATED and ranking_by_user and isinstance(ranking_by_user, int) and (ranking_by_user in [1, 2]):
        # print(f"Skipping low rated image {filename}")
        return
    elif os.path.isfile(f"jobs/{year}/{month}/{image_id}/done") or \
            os.path.isfile(f"jobs/{year}/{month}/{day}/{image_id}/done") or \
            os.path.isfile(f"jobs/{image_id}/done"):
        # print(f"Skipping downloaded image {filename}")
        return
    else:
        image_path = ensure_path_exists(year, month, day, image_id)
        full_path = f"{image_path}/{filename}.png"
        for idx, image_url in enumerate(image_paths):
            if idx > 0:
                filename = f"{filename[:97]}-{idx}"
                full_path = f"{image_path}/{filename}.png"
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', UA)]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(image_url, full_path)
        completed_file_path = f"{image_path}/done"
        f = open(completed_file_path, "x")
        f.close()
    return full_path


def paginated_download(order_by="new"):
    page = 1
    page_of_results = get_api_page(order_by, page)
    while page_of_results:
        if isinstance(page_of_results, list) and len(page_of_results) > 0 and "no jobs" in page_of_results[0].get("msg", "").lower():
            print("Reached end of available results")
            break

        print(f"Downloading page #{page} (order by '{order_by}')")
        download_page(page_of_results)
        page += 1
        page_of_results = get_api_page(order_by, page)


def download_all_order_by_types():
    for order_by_type in ORDER_BY_OPTIONS:
        paginated_download(order_by_type)


def main():
    if not SESSION_TOKEN or not USER_ID:
        raise Exception("Please edit SESSION_TOKEN and USER_ID")
    download_all_order_by_types()


if __name__ == "__main__":
    main()
