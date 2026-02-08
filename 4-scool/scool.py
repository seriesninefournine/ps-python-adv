from dataclasses import dataclass
from abc import ABC, abstractmethod
import random
from decimal import Decimal

class Notification(ABC):

    @abstractmethod
    def send(self, message:str) -> None: ...


class NotificationEmail(Notification):
    def send(self, message: str) -> None:
        print(f"Оповещение через Email: {message}")


class NotificatioSMS(Notification):
    def send(self, message: str) -> None:
        print(f"Оповещение через SMS: {message}")


@dataclass
class Student:
  name: str

class Monitoring(ABC):
    def __init__(self) -> None:...

    @abstractmethod
    def report(self, notification: Notification) -> None: ...


class Journal:
    def __init__(self, mon: Monitoring) -> None:
        self.grade_list = []
        self.monitoring = mon
    
    def add_record(self, student: Student, subj: str, grade: int):
        self.grade_list.append((student, subj, grade))
        mon.report(self, student)

class Statistic:
    def avg_by_student(self, journal: Journal, std: Student) -> Decimal:
        total = 0
        count = 0
        for rec in journal.grade_list:
            if rec[0] == std:
                count += 1
                total += rec[2]
        avg: Decimal = Decimal(total / count).quantize(Decimal('1.0'))
        return avg
    
    def avg_by_subject(self, journal: Journal, subj: str) -> Decimal:
        total = 0
        count = 0
        for rec in journal.grade_list:
            if rec[1] == subj:
                count += 1
                total += rec[2]
        avg: Decimal = Decimal(total / count).quantize(Decimal('1.0'))        
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


class MonitoringLowAVGGrade(Monitoring):
    def __init__(self, stat: Statistic, notification: Notification) -> None:
        self.statistic = stat
        self.notification = notification

    def report(self, jrnl: Journal, std: Student) -> None:
        if (avg := self.statistic.avg_by_student(jrnl, std)) < 3.5:
            self.notification.send(f"Студент {std.name} имеет средний балл {avg}")

subject_list = ["Математика", "Русский язык", "Физика", "Физкультура", "Физика"]
student_list = [Student("Вася"), Student("Петя"), Student("Миша"), Student("Оксана"), Student("Петя")]

mon = MonitoringLowAVGGrade(Statistic(),NotificationEmail())
jrnl = Journal(mon)

for _ in range(10):
    grade_rand = random.randint(2, 5)
    stdnt_rand = random.randint(0, 4)
    jrnl.add_record(student_list[stdnt_rand], subject_list[stdnt_rand], grade_rand)
