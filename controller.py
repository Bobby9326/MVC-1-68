from datetime import date

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.current_student_id = None

        # เชื่อมการทำงานกับปุ่มใน view
        self.view.btn_login.config(command=self.on_login)
        self.view.btn_profile_detail.config(command=self.on_open_detail_from_profile)
        self.view.btn_profile_to_register.config(command=self.on_go_register)
        self.view.btn_logout.config(command=self.on_logout)
        self.view.btn_detail_back.config(command=self.on_back_from_detail)
        self.view.btn_reg_detail.config(command=self.on_open_detail_from_register)
        self.view.btn_reg_enroll.config(command=self.on_enroll)
        self.view.btn_reg_back.config(command=self.on_back_to_profile)

    # login 
    def on_login(self):
        user, pwd = self.view.get_login_inputs()
        st = self.model.get_student(user)
        # user เป็นรหัสนักศึกษา pass คือ 4 ตัวแรกของรหัสนักศึกษา 
        if (not st) or (pwd != user[:4]):
            self.view.error("username or password wrong"); return

        b = self.model.student_birthdate(user)

        #ตรวจสอบ อายุ
        if (not b) or self._age_years(b) < 15:
            self.view.error("ไม่ผ่านเงื่อนไขอายุ (ต้องมีอายุอย่างน้อย 15 ปี)"); return

        self.current_student_id = user
        self._show_profile()

    #เช็คอายุ
    def _age_years(self, dob):
        today = date.today()
        y = today.year - dob.year
        if (today.month, today.day) < (dob.month, dob.day):
            y -= 1
        return y

    #logout
    def on_logout(self):
        self.current_student_id = None
        self.view.show_login()

    # แสดงหน้า profile
    def _show_profile(self):
        st = self.model.get_student(self.current_student_id)
        # เตรียมข้อมูลวิชาที่ลงแล้ว
        rows = []
        for e in self.model.list_enrollments_of_student(self.current_student_id):
            sub = self.model.get_subject(e["subject_id"])
            if not sub:
                continue
            rows.append({
                "subject_id": sub["subject_id"],
                "name": sub["name"],
                "teacher": sub["teacher"],
                "credit": sub["credit"],
                "current_count": sub["current_count"],
                "max_capacity": sub["max_capacity"],
                "grade": (e.get("grade") or "None")
            })
        self.view.show_profile(st, rows)

    # แสดงรายละเอียดวิชา profile
    def on_open_detail_from_profile(self):
        sid = self.view.get_selected_subject_id_in_profile()
        if not sid:
            self.view.error("กรุณาเลือกวิชา"); return
        self.view.show_subject_detail(self.model.get_subject(sid))

    # กลับหน้า profile
    def on_back_from_detail(self):
        self._show_profile()

    # แสดงหน้าลงทะเบียน
    def on_go_register(self):
        all_subjects = self.model.list_subjects()
        enrolled_ids = set(self.model.list_enrolled_subject_ids(self.current_student_id))
        available = [s for s in all_subjects if s["subject_id"] not in enrolled_ids]
        self.view.show_registration(available)

    # แสดงรายละเอียดวิชาจากหน้าลงทะเบียน
    def on_open_detail_from_register(self):
        sid = self.view.get_selected_subject_id_in_register()
        if not sid:
            self.view.error("กรุณาเลือกวิชา"); return
        self.view.show_subject_detail(self.model.get_subject(sid))

    def on_back_to_profile(self):
        self._show_profile()

    #ลงทะเบียน
    def on_enroll(self):
        sid = self.view.get_selected_subject_id_in_register()
        if not sid:
            self.view.error("กรุณาเลือกวิชา"); return
        sub = self.model.get_subject(sid)
        if not sub:
            self.view.error("ไม่พบข้อมูลวิชา"); return

        # กันลงซ้ำ
        if sid in set(self.model.list_enrolled_subject_ids(self.current_student_id)):
            self.view.error("คุณลงทะเบียนรายวิชานี้แล้ว"); return

        # ตรวจ 'ต้องมีเกรดผ่าน' ในวิชาบังคับก่อน
        prereq_id = self.model.subject_prereq(sid)
        if prereq_id:
            passed = set(self.model.student_passed_subject_ids(self.current_student_id))
            if prereq_id not in passed:
                self.view.error("ยังไม่มีเกรด 'ผ่าน' ในวิชาบังคับก่อน จึงลงวิชานี้ไม่ได้"); return

        #  ตรวจจำนวนสูงสุด
        maxcap, current = self.model.subject_capacity_info(sid)
        if maxcap is None:
            self.view.error("ข้อมูลจำนวนสูงสุดไม่สมบูรณ์"); return
        if (maxcap != -1) and (current >= maxcap):
            self.view.error("จำนวนผู้ลงทะเบียนถึงจำนวนสูงสุดแล้ว"); return

        # ผ่านทั้งหมด → บันทึก enrollment ใหม่ (grade เริ่มต้น None)
        self.model.add_enrollment(self.current_student_id, sid, grade=None)
        self.view.info("ลงทะเบียนสำเร็จ")
        self._show_profile()
