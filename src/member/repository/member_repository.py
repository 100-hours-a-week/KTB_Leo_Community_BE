import csv
import os
from typing import Optional, List

from member.schema.member_request import MemberInDB

CSV_FILE = "members.csv"
CSV_HEADERS = ["id", "email", "password", "nickname", "profile_image"]


class MemberRepository:
    def __init__(self, csv_file: str = CSV_FILE):
        self.csv_file = csv_file

    def save(self, member: MemberInDB) -> MemberInDB:
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writerow({
                'id': member.id,
                'email': member.email,
                'password': member.password,
                'nickname': member.nickname,
                'profile_image': member.profile_image or ''
            })
        return member

    def find_by_email(self, email: str) -> Optional[MemberInDB]:
        members = self.find_all()
        for member in members:
            if member.email.lower() == email.lower():
                return member
        return None

    def get_next_id(self):
        members = self.find_all()
        if not members:
            return 1
        return max(member.id for member in members) + 1

    def find_all(self) -> List[MemberInDB]:
        members = []

        if not os.path.exists(self.csv_file):
            return members
        with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                members.append(MemberInDB(
                    id=row['id'],
                    email=row['email'],
                    password=row['password'],
                    nickname=row['nickname'],
                    profile_image=row['profile_image'] if row['profile_image'] else None
                ))
        return members
