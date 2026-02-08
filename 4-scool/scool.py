from dataclasses import dataclass
from abc import ABC, abstractmethod
import random
from decimal import Decimal

class Notification(ABC):

    @abstractmethod
    def send(self, message:str) -> None: ...

class NotifivcationEmail(Notification):
    def send(self, message: str) -> None:
        print(f"Оповещение через Email: {message}")

class NotifivcatioSMS(Notification):
    def send(self, message: str) -> None:
        print(f"Оповещение через SMS: {message}")


@dataclass
class Student:
  name: str


class Journal:
    def __init__(self) -> None:
        self.grade_list = []
    
    def add_record(self, student: Student, subj: str, grade: int):
        self.grade_list.append((student, subj, grade))
        Statistic(NotifivcationEmail()).avg_by_student(self, student)

class Statistic:
    def __init__(self, notification_type: Notification) -> None:
        self.notification = notification_type

    def avg_by_student(self, journal: Journal, std: Student, send_notification: bool = True) -> Decimal:
        total = 0
        count = 0
        for rec in journal.grade_list:
            if rec[0] == std:
                count += 1
                total += rec[2]
        avg: Decimal = Decimal(total / count).quantize(Decimal('1.0'))
        if send_notification and avg < 3.5:
            self.notification.send(f"Студент {rec[0].name} имеет средний балл {avg}")
        
        return avg
    
    def avg_by_all(self, journal: Journal) -> list:
        std_list: list[Student] = []
        #grade_list[index] = [count, total]
        grade_list: list[list] = []
        for rec in journal.grade_list:
            if rec[0] in std_list:
                grade_list[std_list.index(rec[0])][0] += 1
                grade_list[std_list.index(rec[0])][1] += rec[2]
            else:
                std_list.append(rec[0])
                grade_list.append([1, rec[2]])
        result = []
        for index, rec in enumerate(std_list):
            avg = Decimal(grade_list[index][1] / grade_list[index][0]).quantize(Decimal('1.0'))
            result.append([rec, avg])
        return result


subject_list = ["Математика", "Русский язык", "Физика", "Физкультура", "Физика"]
student_list = [Student("Вася"), Student("Петя"), Student("Миша"), Student("Оксана"), Student("Петя")]

jrnl = Journal()

for _ in range(10):
    grade_rand = random.randint(2, 5)
    stdnt_rand = random.randint(0, 4)
    jrnl.add_record(student_list[stdnt_rand], subject_list[stdnt_rand], grade_rand)

stat = Statistic(NotifivcationEmail())

print(stat.avg_by_all(jrnl))