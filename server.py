from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__, template_folder=".")
CORS(app)


def GetBanStatus(PLAYER_UID):
    uid = PLAYER_UID

    BAN_REASON = ""

    url = "https://ff.garena.com/api/antihack/check_banned"
    params = {
        "lang": "en",
        "uid": uid
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://ff.garena.com/en/support/",
        "sec-ch-ua": '"Chromium";v="148", "Microsoft Edge";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0",
        "x-requested-with": "B6FksShzIgjfrYImLpTsadjS86sddhFH"
    }

    cookies = {
        "_ga_3LHB0DGPG8": "GS2.1.s1779623681$o1$g1$t1779623692$j49$l0$h0",
        "_ga_E2MPCS8678": "GS2.1.s1779623683$o1$g0$t1779623692$j51$l0$h0",
        "datadome": "v6j100GC4ow85TkXKp~EgE_gy~ZXEDZiQq3sJz56G4CtzQh_988mHhQR7QF5pNpNrBoOwxmVWyz_XX4MhhJhEULEfWx2_0x6BDvK5TuMHWcblAMLD22kzV7UNe5E1zDH",
        "_ga_G8QGMJPWWV": "GS2.1.s1779623727$o2$g0$t1779623729$j58$l0$h0",
        "_gid": "GA1.2.2101733196.1780026913",
        "_ga_57E30E1PMN": "GS2.2.s1780026913$o1$g1$t1780026930$j43$l0$h0",
        "_ga_KE3SY7MRSD": "GS2.1.s1780026965$o2$g1$t1780026965$j60$l0$h0",
        "_gat_gtag_UA_207309476_25": "1",
        "_ga_RF9R6YT614": "GS2.1.s1780026966$o2$g0$t1780026966$j60$l0$h0",
        "_ga": "GA1.1.1796598086.1779597274"
    }

    try:
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        response.raise_for_status()  # Raise an exception for bad status codes
        

        data = response.json()
        ban_status = data["data"]["is_banned"]

        flagged_uid = ["2149547650"]
        ignore_ids = ["7205726896"]

        if (uid in flagged_uid and ban_status == 1):
            BAN_REASON = "Player used internal Aimbot modifier. Account is Ban.\nDetected  Internal AOB Aimbot Offset Modifications"

            res = {
                "msg": BAN_REASON
            }

            return jsonify(res)
        
        elif (uid in ignore_ids and ban_status == 1):
            BAN_REASON = "The player id is banned. might be due to emulator modifications."

            res = {
                "msg": BAN_REASON
            }

            return jsonify(res)
        


        elif (ban_status == 1):
            BAN_REASON = "Player used Third Party Aimbot modifier. Account is Ban."
            res = {
                "msg": BAN_REASON
            }

            return jsonify(res)

        else:
            res = {
                "msg": "There is no proof that the player is using cheats."
            }

            return jsonify(res)


    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return jsonify({"msg": "Server is busy !"})


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/check-ban")
def checkBanStatus():
    player_uid = request.args.get("player-uid")

    if not player_uid:
        return jsonify("player uid is required !")
    
    try:
        response = GetBanStatus(player_uid)
        return response, 200
    except:
        return jsonify({"msg": "error"}), 500

    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5555", debug=True)

