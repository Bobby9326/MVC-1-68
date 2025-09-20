import tkinter as tk
from tkinter import ttk, messagebox

class View:
    #เตรียมหน้าต่างหลัก
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.geometry("900x560")
        self._build_frames()

    #แสดงหน้า login
    def show_login(self):
        self._raise("login")

    #แสดงหน้า profile
    def show_profile(self, student, enrolled_rows):
        self.lbl_student_info.config(
            text=f"รหัส: {student['student_id']} | {student['title']}{student['first_name']} {student['last_name']} | โรงเรียน: {student['school']}"
        )
        self._refresh_tree(self.tree_enrolled, enrolled_rows)
        self._raise("profile")

    #แสดงหน้ารายละเอียดวิชา
    def show_subject_detail(self, subject_dict):
        if not subject_dict:
            return
        values = [
            ("รหัสวิชา", subject_dict["subject_id"]),
            ("ชื่อวิชา", subject_dict["name"]),
            ("หน่วยกิต", subject_dict["credit"]),
            ("อาจารย์ผู้สอน", subject_dict["teacher"]),
            ("วิชาบังคับก่อน", subject_dict.get("prereq_subject_id") or "-"),
            ("จำนวนสูงสุด", subject_dict["max_capacity"]),
            ("จำนวนที่ลงแล้ว", subject_dict["current_count"]),
        ]
        self._refresh_tree(self.tree_detail, values)
        self._raise("detail")

    #แสดงหน้าลงทะเบียน
    def show_registration(self, available_subjects):
        self._refresh_tree(self.tree_available, available_subjects)
        self._raise("register")

    #แสดงแจ้งเตือนทั่วไป
    def info(self, msg):
        messagebox.showinfo("Info", msg)

    #แสดงแจ้งเตือน error
    def error(self, msg):
        messagebox.showerror("Error", msg)

    #สร้างเฟรมทั้งหมด
    def _build_frames(self):
        self.frames = {}

        # ---- Login ----
        f_login = ttk.Frame(self.root, padding=16)
        self.frames["login"] = f_login
        ttk.Label(f_login, text="เข้าสู่ระบบ", font=("Segoe UI", 20, "bold")).pack(pady=8)
        form = ttk.Frame(f_login); form.pack(pady=12)
        ttk.Label(form, text="รหัสนักเรียน (username):").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(form, text="รหัสผ่าน (4 ตัวแรกของรหัสนักเรียน):").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.ent_user = ttk.Entry(form, width=30)
        self.ent_pass = ttk.Entry(form, width=30, show="*")
        self.ent_user.grid(row=0, column=1, padx=6, pady=6)
        self.ent_pass.grid(row=1, column=1, padx=6, pady=6)
        self.btn_login = ttk.Button(f_login, text="เข้าสู่ระบบ")
        self.btn_login.pack(pady=12)

        # ---- Profile ----
        f_profile = ttk.Frame(self.root, padding=12)
        self.frames["profile"] = f_profile
        ttk.Label(f_profile, text="ประวัตินักเรียน", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        self.lbl_student_info = ttk.Label(f_profile, text="-")
        self.lbl_student_info.pack(anchor="w", pady=(4, 10))
        self.tree_enrolled = self._make_tree(
            f_profile,
            [
                ("subject_id","รหัสวิชา",110),
                ("name","ชื่อวิชา",320),
                ("teacher","อาจารย์",160),
                ("credit","หน่วยกิต",80),
                ("current_count","ลงแล้ว",80),
                ("max_capacity","รับสูงสุด",90),
                ("grade","เกรด",70)
            ]
        )
        self.tree_enrolled.pack(fill="both", expand=True, pady=6)

        btns = ttk.Frame(f_profile); btns.pack(anchor="e", pady=8)
        self.btn_profile_detail = ttk.Button(btns, text="ดูรายละเอียดวิชา")
        self.btn_profile_to_register = ttk.Button(btns, text="ไปลงทะเบียนเรียน")
        self.btn_logout = ttk.Button(btns, text="ออกจากระบบ")
        self.btn_profile_detail.grid(row=0, column=0, padx=6)
        self.btn_profile_to_register.grid(row=0, column=1, padx=6)
        self.btn_logout.grid(row=0, column=2, padx=6)

        # ---- Subject Detail ----
        f_detail = ttk.Frame(self.root, padding=12)
        self.frames["detail"] = f_detail
        ttk.Label(f_detail, text="รายละเอียดวิชา", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0,8))
        self.tree_detail = self._make_kv_tree(f_detail)
        self.tree_detail.pack(fill="both", expand=True)
        bar = ttk.Frame(f_detail); bar.pack(anchor="e", pady=8)
        self.btn_detail_back = ttk.Button(bar, text="กลับ")
        self.btn_detail_back.grid(row=0, column=0, padx=6)

        # ---- Registration ----
        f_reg = ttk.Frame(self.root, padding=12)
        self.frames["register"] = f_reg
        ttk.Label(f_reg, text="ลงทะเบียนเรียน", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        self.tree_available = self._make_tree(
            f_reg,
            [
                ("subject_id","รหัสวิชา",120),
                ("name","ชื่อวิชา",320),
                ("teacher","อาจารย์",180),
                ("credit","หน่วยกิต",80),
                ("current_count","ลงแล้ว",80),
                ("max_capacity","รับสูงสุด",100)
            ]
        )
        self.tree_available.pack(fill="both", expand=True, pady=6)
        btns2 = ttk.Frame(f_reg); btns2.pack(anchor="e", pady=8)
        self.btn_reg_detail = ttk.Button(btns2, text="ดูรายละเอียดวิชา")
        self.btn_reg_enroll = ttk.Button(btns2, text="ลงทะเบียน")
        self.btn_reg_back = ttk.Button(btns2, text="กลับโปรไฟล์")
        self.btn_reg_detail.grid(row=0, column=0, padx=6)
        self.btn_reg_enroll.grid(row=0, column=1, padx=6)
        self.btn_reg_back.grid(row=0, column=2, padx=6)

        self.show_login()

    #สลับหน้าแสดงผล
    def _raise(self, name):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    #สร้าง Treeview แบบตาราง
    def _make_tree(self, parent, cols):
        tree = ttk.Treeview(parent, columns=[c[0] for c in cols], show="headings", height=12)
        for key, text, width in cols:
            tree.heading(key, text=text)
            tree.column(key, width=width, anchor="center")
        return tree

    #สร้าง Treeview แบบ key-value
    def _make_kv_tree(self, parent):
        tree = ttk.Treeview(parent, columns=["k","v"], show="headings")
        tree.heading("k", text="หัวข้อ")
        tree.heading("v", text="ข้อมูล")
        tree.column("k", width=200, anchor="w")
        tree.column("v", width=600, anchor="w")
        return tree

    #เคลียร์ข้อมูลเก่าใน Treeview แล้วอัปเดต
    def _refresh_tree(self, tree, rows):
        for iid in tree.get_children():
            tree.delete(iid)
        if not rows:
            return
        if isinstance(rows[0], dict):
            cols = tree["columns"]
            for r in rows:
                tree.insert("", "end", values=[r.get(c,"") for c in cols])
        else:
            for k, v in rows:
                tree.insert("", "end", values=[k, v])

    #get input ของ  login
    def get_login_inputs(self):
        return self.ent_user.get().strip(), self.ent_pass.get().strip()

    #get วิชาที่เลือก จากหน้า profile
    def get_selected_subject_id_in_profile(self):
        sel = self.tree_enrolled.selection()
        if not sel:
            return None
        values = self.tree_enrolled.item(sel[0], "values")
        return values[0] if values else None
    #get วิชาที่เลือก จากหน้าลงทะเบียน
    def get_selected_subject_id_in_register(self):
        sel = self.tree_available.selection()
        if not sel:
            return None
        values = self.tree_available.item(sel[0], "values")
        return values[0] if values else None
