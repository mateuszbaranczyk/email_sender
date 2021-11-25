import json
import smtplib
from email.message import EmailMessage

import requests


class TrashRequester:
    def __init__(self) -> None:
        self.url = (
            "https://warszawa19115.pl/harmonogramy-wywozu-odpadow?p_p_id=portalCKMjunkschedules_WAR_portalCKMjunksched"
            "ulesportlet_INSTANCE_o5AIb2mimbRJ&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=ajaxReso"
            "urceURL&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1"
        )
        self.home = {
            "_portalCKMjunkschedules_WAR_portalCKMjunkschedulesportlet_INSTANCE_o5AIb2mimbRJ_addressPointId": "95175614"
        }
        self.schedule = []
        self.short_list = []
        self.data = []

    def get_data(self) -> list:
        response = requests.post(self.url, data=self.home).text
        data = json.loads(response)
        schedule = data[0]["harmonogramy"]

        schedule = [
            (i["data"], i["frakcja"]["nazwa"])
            for i in schedule
            if i["data"] is not None
        ]

        return self._convert_confusing_type(schedule)

    def _convert_confusing_type(self, data) -> list:
        converted = []

        for date, trash_type in data:

            if trash_type == "zmieszane odpady opakowaniowe":
                trash_type = "metale i tworzywa sztuczne"
            elif trash_type in ("odpady kuchenne ulegające biodegradacji", "odpady wielkogabarytowe"):
                continue

            converted.append((date, trash_type))

        return sorted(converted, key=lambda x: x[0])

    def create_short_list(self, data) -> list:
        nearest_course = data[0][0]
        short_list = []

        for position in data:
            if position[0] == nearest_course:
                short_list.append(position)

        return short_list


class Postman:
    def __init__(self) -> None:
        self.trash_requester = TrashRequester()
        self.gmail_user = "example.user@gmail.com"
        self.gmail_password = "admin1"

        self.sent_from = "example.user@gmail.com"
        self.to = [
            "example.user2@gmail.com",
            "example.user3@gmail.com",
            "example.user4@gmail.com",
        ]

    def create_msg(self) -> str:
        calendar = self.trash_requester.get_data()
        msg = EmailMessage()
        message_content = "  ".join(f"\n{i[0]}  {i[1]}" for i in calendar)

        msg.set_content(
            f"""Harmonogram wywozu śmieci:
        {message_content}
        NIE odpowiadaj na tą wiadomość!!!
        """
        )
        msg["Subject"] = "Mmm Trash, Yeah I Love Trash"

        return msg

    def send_trash(self) -> None:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(self.gmail_user, self.gmail_password)
        server.send_message(self.create_msg(), self.sent_from, self.to)

if __name__ == "__main__":
    postman = Postman()
    postman.send_trash()