# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 00:15:50 2022

@author: Gortaf

https://github.com/Gortaf
"""

import requests as http
from requests.structures import CaseInsensitiveDict
import json
import datetime
import time

import smtplib

def smtp_gmail(days):
    """
    Envoie un mail pour notifier que des créneaux sont disponibles au consulat.
    Changez username & password par une adresse gmail avec permission pour les
    application moins sécurisés (utilisez une boite mail temporaire, pas votre
    mail principal). Ce sera l'adresse qui vous enverras la notification.
    Changez email_to par l'adresse mail que vous voulez notifier en cas de
    créneaux libres

    Parameters
    ----------
    days : str
        Les jours avec des créneaux disponibles.

    Returns
    -------
    None.

    """
    username = "un_mail@gmail.com"
    password = "un_mot_de_passe"
    smtp_server = "smtp.gmail.com:587"
    email_from = username
    email_to = "mail_à_notifier@domain.com"
    email_body = "".join([
        "From: %s\r\n" % email_from,
        "To: %s\r\n" % email_to,
        "Subject: Horaires dispo au consulat!\r\n",
        "\r\n",
        "Les jours suivants ont des dispos au consulat: %s\r\n" % (days)
        ]
        )

    server = smtplib.SMTP(smtp_server)
    server.starttls()
    server.login(username, password)
    server.sendmail(email_from, email_to, email_body)
    server.quit()

class Http_toolbox:
    def __init__(self):
        pass

    # Obtient un id de session depuis le site du consulat
    def get_id(self):
        url = "https://api.consulat.gouv.fr/api/team/61f924e90b0582a933ff3e7c/reservations-session"

        headers = CaseInsensitiveDict()
        headers["Connection"] = "keep-alive"
        headers["Content-Length"] = "0"
        headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
        headers["Accept"] = "application/json, text/plain, */*"
        headers["x-troov-web"] = "com.troov.web"
        headers["sec-ch-ua-mobile"] = "?0"
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        headers["sec-ch-ua-platform"] = '"Windows"'
        headers["Origin"] = "https://consulat.gouv.fr"
        headers["Sec-Fetch-Site"] = "same-site"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Referer"] = "https://consulat.gouv.fr/"
        headers["Accept-Language"] = "fr"
        resp = http.post(url, headers=headers)

        if resp.ok:
            return json.loads(resp.content)["_id"]
        else:
            raise Exception('get_id didn\'t return a 200 signal')

    # Optient la liste des "jours exclus" sur le site du consulat
    def get_days(self):
        url = "https://api.consulat.gouv.fr/api/team/61f924e90b0582a933ff3e7c/reservations/exclude-days"

        headers = CaseInsensitiveDict()
        headers["Connection"] = "keep-alive"
        headers["sec-ch-ua"] = '"Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
        headers["Accept"] = "application/json, text/plain, */*"
        headers["x-troov-web"] = "com.troov.web"
        headers["sec-ch-ua-mobile"] = "?0"
        headers["Content-Type"] = "application/json"
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        headers["sec-ch-ua-platform"] = '"Windows"'
        headers["Origin"] = "https://consulat.gouv.fr"
        headers["Sec-Fetch-Site"] = "same-site"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Referer"] = "https://consulat.gouv.fr/"
        headers["Accept-Language"] = "fr"

        today = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        then = (datetime.datetime.now() + datetime.timedelta(days=46)).strftime("%Y-%m-%dT%H:%M:%S")
        data = f'{{"start":"{today}","end":"{then}","session":{{"623e3c5319ec2e40dcf76397":1}}}}'


        resp = http.post(url, headers=headers, data=data)
        if resp.ok:
            days = resp.content[2:-1].decode("utf-8").replace('"', '').split(",")

            return days
        else:
            raise Exception('get_days didn\'t return a 200 signal')

    # Optient les heures disponibles à un jour donné. Requiert une id de session.
    def get_hours(self, sess_id, day):

        url = f"https://api.consulat.gouv.fr/api/team/61f924e90b0582a933ff3e7c/reservations/avaibility?name=Demande%20de%20passeport%2FCNI&date={day}&places=1&matching=&maxCapacity=1&sessionId={sess_id}"

        headers = CaseInsensitiveDict()
        headers["Connection"] = "keep-alive"
        headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
        headers["Accept"] = "application/json, text/plain, */*"
        headers["x-troov-web"] = "com.troov.web"
        headers["sec-ch-ua-mobile"] = "?0"
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
        headers["sec-ch-ua-platform"] = '"Windows"'
        headers["Origin"] = "https://consulat.gouv.fr"
        headers["Sec-Fetch-Site"] = "same-site"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Referer"] = "https://consulat.gouv.fr/"
        headers["Accept-Language"] = "fr"


        resp = http.get(url, headers=headers)

        if resp.ok:
            return resp.content.decode("utf-8")
        else:
            raise Exception('get_hours didn\'t return a 200 signal')

if __name__ == "__main__":
    tools = Http_toolbox()

    while True:
        time.sleep(10)  # Cooldown avant de re-scanner le site. Évite un too_many_requests.

        next_days = [(datetime.datetime.today() + datetime.timedelta(days=x)).strftime("%Y-%m-%d") for x in range(46)]
        try:
            excluded_days = tools.get_days()
        except Exception as e:
            print(e)
            continue
        available_days = list()
        for day in next_days:
            if day not in excluded_days:
                available_days.append(day)

        if len(available_days) == 0:
            print(f"{datetime.datetime.now()}: Aucun jour avec des créneaux")
            continue
        try:
            sess_id = tools.get_id()
        except Exception as e:
            print(e)
            continue

        to_send = ""
        for day in available_days:
            try:
                hours = tools.get_hours(sess_id, day)
                if len(hours) != 2:
                    to_send += f"{day}\n"
            except Exception as e:
                print(e)
                continue


        if to_send != "":
            print(f"{datetime.datetime.now()}: {to_send} sont disponibles")
            smtp_gmail(to_send)
        else:
            print(f"{datetime.datetime.now()}: Aucun jour avec des créneaux")