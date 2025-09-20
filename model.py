import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data"

class Model:
    #เตรียมไฟล์ทั้งหมด
    def __init__(self):
        self.students = self._load_json("students.json")
        self.subjects = self._load_json("subjects.json")
        self.enrollments = self._load_json("enrollments.json")
        self._students_by_id = {s["student_id"]: s for s in self.students}
        self._subjects_by_id = {sub["subject_id"]: sub for sub in self.subjects}
        self._recount_all() 

    #โหลดไฟล์ json
    def _load_json(self, name):
        fp = DATA_DIR / name
        if fp.exists():
            with open(fp, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    #เซฟไฟล์ json
    def _save_json(self, name, data):
        fp = DATA_DIR / name
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    #เซฟสถานะปัจจุบันทั้งหมดกลับไฟล์
    def persist(self):
        self._save_json("subjects.json", self.subjects)
        self._save_json("students.json", self.students)
        self._save_json("enrollments.json", self.enrollments)

    #ส่งข้อมูลนักเรียนตาม student_id
    def get_student(self, student_id: str):
        return self._students_by_id.get(student_id)

    #ส่งลิสต์รายวิชาทั้งหมด
    def list_subjects(self):
        return list(self._subjects_by_id.values())

    #ส่งรายละเอียดวิชาตาม subject_id
    def get_subject(self, subject_id: str):
        return self._subjects_by_id.get(subject_id)

    #ส่งลิสต์ subject_id ที่นักเรียนคนนั้น "ลงทะเบียนแล้ว"
    def list_enrolled_subject_ids(self, student_id: str):
        return [e["subject_id"] for e in self.enrollments if e["student_id"] == student_id]

    #ส่งรายการ enrollment  ของนักเรียนคนนั้น
    def list_enrollments_of_student(self, student_id: str):
        
        return [e for e in self.enrollments if e["student_id"] == student_id]

    # นับจำนวนนักเรียนที่ลงทะเบียนในวิชานี้ตาม subject_id
    def subject_current_count(self, subject_id: str) -> int:
        return sum(1 for e in self.enrollments if e["subject_id"] == subject_id)

    # เพิ่มแถวลงทะเบียนใหม่
    def add_enrollment(self, student_id: str, subject_id: str, grade=None):
        #บันทึกการลงทะเบียนใหม่: ใส่ grade เริ่มต้นเป็น None
        self.enrollments.append({"student_id": student_id, "subject_id": subject_id, "grade": grade})
        sub = self.get_subject(subject_id)
        if sub:
            sub["current_count"] = self.subject_current_count(subject_id)
        self.persist()

   
    #ส่งจำนวนนักเรียนสูงสุดของวิชา
    def subject_capacity_info(self, subject_id: str):
        sub = self.get_subject(subject_id)
        if not sub:
            return None, None
        return sub.get("max_capacity", -1), sub.get("current_count", 0)

    #ส่ง subject_id ของวิชาบังคับ
    def subject_prereq(self, subject_id: str):
        sub = self.get_subject(subject_id)
        if not sub:
            return None
        return sub.get("prereq_subject_id") or None

    #ส่งวันเกิดของนักเรียน
    def student_birthdate(self, student_id: str):
        st = self.get_student(student_id)
        if not st:
            return None
        try:
            return datetime.strptime(st["birthdate"], "%Y-%m-%d").date()
        except Exception:
            return None

    #เช็คว่าเกรดผ่านหรือไม่
    def is_passing_grade(self, grade) -> bool:
        #เกณฑ์ผ่าน: ต้องมีเกรด และไม่ใช่ F/none/ว่าง
        if grade is None:
            return False
        g = str(grade).strip().lower()
        return (g not in ("", "none", "f"))

    #ส่งลิสต์ subject_id ที่นักเรียนผ่านแล้ว
    def student_passed_subject_ids(self, student_id: str):
        passed = []
        for e in self.list_enrollments_of_student(student_id):
            if self.is_passing_grade(e.get("grade")):
                passed.append(e["subject_id"])
        st = self.get_student(student_id) or {}
        passed += st.get("completed_subject_ids", [])
        return list(dict.fromkeys(passed))  
    
    # sync ค่า current_count ของทุกวิชาให้เท่ากับจำนวนแถวใน enrollments
    def _recount_all(self):
        for sub in self.subjects:
            sub["current_count"] = self.subject_current_count(sub["subject_id"])
