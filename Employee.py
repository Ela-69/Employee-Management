"""
/****************/
Mã sinh viên: 202418930
Họ tên: Dương Tùng Lâm
/****************/
"""
import gc
import math
import weakref
from typing import List, Optional

def _require_non_empty(value, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} không được rỗng")
    return value.strip()


def _is_number(value) -> bool:
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value))


def _require_non_negative(value, field: str) -> float:
    if not _is_number(value) or value < 0:
        raise ValueError(f"{field} phải là số không âm")
    return float(value)


def _normalize_text(value) -> str:
    if not isinstance(value, str):
        raise TypeError("Giá trị phải là chuỗi")
    return value.strip()


def _money(x: float) -> str:
    return f"{x:,.0f}"

# Lớp Employee

class Employee:
    DEFAULT_ID = "UNKNOWN"
    DEFAULT_NAME = "Unnamed employee"

    def __init__(self, emp_id: str = DEFAULT_ID,
                 full_name: str = DEFAULT_NAME,
                 base_salary: float = 0):
        """Gộp 3 constructor: (), (id, name), (id, name, salary)."""
        self._id = _require_non_empty(emp_id, "Mã nhân sự")
        self._full_name = _require_non_empty(full_name, "Họ tên")
        self._base_salary = _require_non_negative(base_salary, "Lương cơ bản")

    @property
    def id(self) -> str:
        return self._id

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def base_salary(self) -> float:
        return self._base_salary

    def increase_salary(self, value: float, by_percentage: bool = False) -> None:
        """
        increase_salary(amount)                 : tăng số tiền cố định
        increase_salary(value, by_percentage)   : True -> tăng theo %,
                                                  False -> số tiền cố định
        """
        if not _is_number(value) or value <= 0:
            raise ValueError("Giá trị tăng lương phải dương")
        if by_percentage:
            self._base_salary *= 1 + value / 100.0
        else:
            self._base_salary += value

    def calculate_monthly_cost(self) -> float:
        return self._base_salary

    def display_info(self) -> None:
        print(f"[Employee] {self._id} | {self._full_name} | "
              f"lương cơ bản: {_money(self._base_salary)} | "
              f"chi phí tháng: {_money(self.calculate_monthly_cost())}")

    def __del__(self):
        print(f"   (hủy Employee {getattr(self, '_id', '?')} - "
              f"{getattr(self, '_full_name', '?')})")

# Lớp SoftwareEngineer 

class SoftwareEngineer(Employee):
    """Lớp đại diện cho một kỹ sư phần mềm."""

    def __init__(self, emp_id: str, full_name: str, *args):
        """
        SoftwareEngineer(id, name, language)
        SoftwareEngineer(id, name, salary, language, allowance)
        """
        if len(args) == 1:
            salary, language, allowance = 0, args[0], 0
        elif len(args) == 3:
            salary, language, allowance = args
        else:
            raise TypeError("SoftwareEngineer nhận (id, name, language) "
                            "hoặc (id, name, salary, language, allowance)")
        super().__init__(emp_id, full_name, salary)
        self._primary_language = _require_non_empty(language, "Ngôn ngữ chính")
        self._technical_allowance = _require_non_negative(allowance, "Phụ cấp")

    @property
    def primary_language(self) -> str:
        return self._primary_language

    @property
    def technical_allowance(self) -> float:
        return self._technical_allowance

    def calculate_monthly_cost(self) -> float:
        return self._base_salary + self._technical_allowance

    def display_info(self) -> None:
        print(f"[SoftwareEngineer] {self._id} | {self._full_name} | "
              f"ngôn ngữ: {self._primary_language} | "
              f"lương: {_money(self._base_salary)} | "
              f"phụ cấp: {_money(self._technical_allowance)} | "
              f"chi phí tháng: {_money(self.calculate_monthly_cost())}")

    def __del__(self):
        print(f"   (hủy SoftwareEngineer {getattr(self, '_id', '?')} - "
              f"{getattr(self, '_full_name', '?')})")
        super().__del__()

# Lớp ProjectTeam 

class ProjectTeam:
    def __init__(self, project_code: str, project_name: str,
                 leader: Optional[Employee] = None):
        """ProjectTeam(code, name) / ProjectTeam(code, name, leader)."""
        self._project_code = _require_non_empty(project_code, "Mã dự án")
        self._project_name = _require_non_empty(project_name, "Tên dự án")
        self._leader: Optional[Employee] = None
        self._members: List[Employee] = []
        if leader is not None:
            if not isinstance(leader, Employee):
                raise TypeError("Trưởng nhóm phải là Employee")
            self._members.append(leader)
            self._leader = leader

    @property
    def project_code(self) -> str:
        return self._project_code

    @property
    def leader(self) -> Optional[Employee]:
        return self._leader

    def _find(self, employee_id: str) -> Optional[Employee]:
        for m in self._members:
            if m.id == employee_id:
                return m
        return None

    def contains(self, employee_id: str) -> bool:
        return self._find(employee_id) is not None

    def add_member(self, employee: Employee, make_leader: bool = False) -> bool:
        """
        add_member(employee)               : thêm thành viên thường
        add_member(employee, make_leader)  : True -> thêm và làm trưởng nhóm
        Trưởng nhóm cũ vẫn là thành viên.
        """
        if not isinstance(employee, Employee):
            return False
        if self.contains(employee.id):
            return False
        self._members.append(employee)
        if make_leader:
            self._leader = employee
        return True

    def remove_member(self, employee_id: str) -> bool:
        target = self._find(employee_id)
        if target is None:
            return False
        if target is self._leader:
            return False
        self._members.remove(target)
        return True

    def change_leader(self, employee: Employee) -> bool:
        if not isinstance(employee, Employee):
            return False
        existing = self._find(employee.id)
        if existing is None:
            self._members.append(employee)
        elif existing is not employee:
            return False
        self._leader = employee
        return True

    def calculate_total_monthly_cost(self) -> float:
        return sum(m.calculate_monthly_cost() for m in self._members)

    def display_team(self) -> None:
        print(f"=== Dự án {self._project_code}: {self._project_name} ===")
        leader = self._leader.full_name if self._leader else "(chưa có)"
        print(f"Trưởng nhóm: {leader} | Số thành viên: {len(self._members)}")
        for m in self._members:
            print("  * (trưởng nhóm)" if m is self._leader else "  *", end=" ")
            m.display_info()
        print(f"Tổng chi phí tháng: {_money(self.calculate_total_monthly_cost())}")

    def __del__(self):
        print(f"   (hủy ProjectTeam {getattr(self, '_project_code', '?')}; ")
        getattr(self, '_members', []).clear()
        self._leader = None


def check(label: str, condition: bool) -> None:
    print(f"   [{'OK' if condition else 'FAIL'}] {label}")
    assert condition, label


def second_team_scope(shared: Employee, engineer: SoftwareEngineer):
    """tạo nhóm thứ hai trong phạm vi cục bộ; ra khỏi hàm = nhóm bị hủy."""
    team_b = ProjectTeam("PRJ-B", "Mobile App", engineer)
    check("Nhóm B tự đưa trưởng nhóm vào danh sách", team_b.contains(engineer.id))
    check("Thêm nhân sự đã có ở nhóm A vào nhóm B", team_b.add_member(shared))
    team_b.display_team()
    print("   -> kết thúc khối lệnh, nhóm B sắp bị hủy...")
    return weakref.ref(team_b)


def _ask(prompt: str) -> str:
    return input(prompt).strip()


def _ask_required(prompt: str, field: str) -> str:
    value = _ask(prompt)
    if not value:
        raise ValueError(f"{field} không được rỗng")
    return value


def _ask_float(prompt: str) -> float:
    raw = _ask_required(prompt, "Giá trị")
    try:
        return float(raw.replace(",", "").replace("_", ""))
    except ValueError:
        raise ValueError(f"'{raw}' không phải số hợp lệ")


def _ask_optional_float(prompt: str, default: float = 0.0) -> float:
    raw = _ask(prompt)
    if not raw:
        return default
    try:
        return float(raw.replace(",", "").replace("_", ""))
    except ValueError:
        raise ValueError(f"'{raw}' không phải số hợp lệ")

# Chương trình chính 

def test() -> None:
    employees = {}
    teams = {}

    def register(e: Employee) -> None:
        if e.id in employees:
            raise ValueError(f"Mã '{e.id}' đã tồn tại trong danh sách nhân sự")
        employees[e.id] = e
        e.display_info()

    def pick_employee(prompt: str = "Mã nhân sự: ") -> Employee:
        emp_id = _ask_required(prompt, "Mã nhân sự")
        if emp_id not in employees:
            raise ValueError(f"Không có nhân sự mã '{emp_id}'")
        return employees[emp_id]

    def pick_team() -> ProjectTeam:
        code = _ask_required("Mã dự án: ", "Mã dự án")
        if code not in teams:
            raise ValueError(f"Không có nhóm mã '{code}'")
        return teams[code]

    def create_employee() -> None:
        print("1) Employee()  2) Employee(id, name)  3) Employee(id, name, salary)")
        c = _ask("Chọn: ")
        if c == "1":
            register(Employee())
        elif c == "2":
            register(Employee(_ask_required("Mã: ", "Mã nhân sự"),
                              _ask_required("Họ tên: ", "Họ tên nhân sự")))
        elif c == "3":
            register(Employee(_ask_required("Mã: ", "Mã nhân sự"),
                              _ask_required("Họ tên: ", "Họ tên nhân sự"),
                              _ask_float("Lương cơ bản: ")))
        else:
            raise ValueError("Lựa chọn không hợp lệ")

    def create_engineer() -> None:
        print("1) SoftwareEngineer(id, name, language)")
        print("2) SoftwareEngineer(id, name, salary, language, allowance)")
        c = _ask("Chọn: ")
        if c == "1":
            register(SoftwareEngineer(_ask_required("Mã: ", "Mã nhân sự"),
                                      _ask_required("Họ tên: ", "Họ tên nhân sự"),
                                      _ask_required("Ngôn ngữ chính: ", "Ngôn ngữ chính")))
        elif c == "2":
            emp_id = _ask_required("Mã: ", "Mã nhân sự")
            name = _ask_required("Họ tên: ", "Họ tên nhân sự")
            salary = _ask_float("Lương cơ bản: ")
            lang = _ask_required("Ngôn ngữ chính: ", "Ngôn ngữ chính")
            allowance = _ask_optional_float("Phụ cấp kỹ thuật (để trống = 0): ")
            if allowance < 0:
                raise ValueError("Phụ cấp phải là số không âm")
            register(SoftwareEngineer(emp_id, name, salary, lang, allowance))
        else:
            raise ValueError("Lựa chọn không hợp lệ")

    def raise_salary() -> None:
        e = pick_employee()
        print("1) increase_salary(amount)")
        print("  2) increase_salary(value, byPercentage)")
        c = _ask("Chọn: ")
        if c not in ("1", "2"):
            raise ValueError("Lựa chọn không hợp lệ")
        value = _ask_float("Giá trị tăng: ")
        before = e.base_salary
        if c == "1":
            e.increase_salary(value)
        else:
            by_percentage = _ask("byPercentage (true/false): ").lower()
            if by_percentage not in ("true", "false"):
                raise ValueError("byPercentage phải là true hoặc false")
            e.increase_salary(value, by_percentage == "true")
        print(f"{_money(before)} -> {_money(e.base_salary)}")

    def list_employees() -> None:
        if not employees:
            print("(trống)")
        for e in employees.values():
            e.display_info()

    def total_monthly_cost() -> None:
        total = sum(e.calculate_monthly_cost() for e in employees.values())
        print(_money(total))

    def create_team() -> None:
        code = _ask_required("Mã dự án: ", "Mã dự án")
        name = _ask_required("Tên dự án: ", "Tên dự án")
        if code in teams:
            raise ValueError(f"Mã dự án '{code}' đã tồn tại")
        print("1) Không có trưởng nhóm  2) Có trưởng nhóm")
        c = _ask("Chọn: ")
        if c == "1":
            teams[code] = ProjectTeam(code, name)
        elif c == "2":
            teams[code] = ProjectTeam(code, name,
                                      pick_employee("Mã trưởng nhóm: "))
        else:
            raise ValueError("Lựa chọn không hợp lệ")
        print("Đã tạo")

    def add_member() -> None:
        t, e = pick_team(), pick_employee()
        print("1) Thêm nhân sự  2) Thêm nhân sự và làm trưởng nhóm")
        c = _ask("Chọn: ")
        if c not in ("1", "2"):
            raise ValueError("Lựa chọn không hợp lệ")
        ok = t.add_member(e) if c == "1" else t.add_member(e, True)
        print("OK" if ok else "Từ chối")

    def remove_member() -> None:
        t = pick_team()
        ok = t.remove_member(_ask("Mã nhân sự cần xóa: "))
        print("OK" if ok else "Từ chối")

    def change_leader() -> None:
        t, e = pick_team(), pick_employee("Mã trưởng nhóm mới: ")
        ok = t.change_leader(e)
        print("OK" if ok else "Từ chối")

    def check_contains() -> None:
        t = pick_team()
        print("Có" if t.contains(_ask("Mã nhân sự: ")) else "Không")

    def show_team() -> None:
        pick_team().display_team()

    def destroy_team() -> None:
        code = _ask("Mã dự án cần hủy: ")
        if code not in teams:
            raise ValueError(f"Không có nhóm mã '{code}'")
        ref = weakref.ref(teams[code])
        del teams[code]
        gc.collect()
        print("Bị hủy." if ref() is None else "Chưa hủy.")
        print(f"Nhân sự: {len(employees)}")
        list_employees()

    actions = {
        "1": ("Tạo Employee", create_employee),
        "2": ("Tạo SoftwareEngineer", create_engineer),
        "3": ("Tăng lương", raise_salary),
        "4": ("Danh sách nhân sự", list_employees),
        "5": ("Tạo nhóm", create_team),
        "6": ("Thêm thành viên", add_member),
        "7": ("Xóa thành viên", remove_member),
        "8": ("Đổi trưởng nhóm", change_leader),
        "9": ("Kiểm tra trong nhóm", check_contains),
        "10": ("Hiển thị nhóm", show_team),
        "11": ("Hủy nhóm", destroy_team),
        "12": ("Tổng chi phí tháng", total_monthly_cost),
    }

    while True:
        print("\n========== MENU ==========")
        for key, (label, _) in actions.items():
            print(f"{key:>3}. {label}")
        print("  0. Thoát")
        try:
            choice = _ask("Chọn: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if choice == "0":
            break
        if choice not in actions:
            print("Sai")
            continue
        try:
            actions[choice][1]()
        except (ValueError, TypeError) as ex:
            print(f"LỖI: {ex}")
        except (EOFError, KeyboardInterrupt):
            print()
            break


if __name__ == "__main__":
    test()
