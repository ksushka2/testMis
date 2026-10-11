import json
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
COURSES_FILE = DATA_DIR / "courses.json"
REQUESTS_FILE = DATA_DIR / "requests.json"

PRODUCT_NAME = "IT-Школа"
PRODUCT_DESCRIPTION = (
    "Информационная система детской IT-школы: приём заявок на курсы, "
    "просмотр статусов и работа с учебными группами."
)
VERSION = "0.0.2"


def _read_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_courses():
    return _read_json(COURSES_FILE)


def get_course(course_id: int):
    for course in load_courses():
        if course["id"] == course_id:
            return course
    return None


def load_requests():
    return _read_json(REQUESTS_FILE)


def get_request(pk: int):
    for item in load_requests():
        if item["id"] == pk:
            return item
    return None


def age_fits_course(child_age: int, course_id: int):
    course = get_course(course_id)
    if course is None:
        return False, "Выбран несуществующий курс."
    if child_age < course["min_age"] or child_age > course["max_age"]:
        return (
            False,
            f"Возраст ребёнка ({child_age}) не подходит для курса «{course['name']}» "
            f"(допустимо {course['min_age']}–{course['max_age']} лет).",
        )
    return True, None


def add_request(data: dict) -> dict:
    requests = load_requests()
    next_id = max((r["id"] for r in requests), default=0) + 1
    public_number = f"IT-2026-{next_id:03d}"
    record = {
        "id": next_id,
        "public_number": public_number,
        "child_full_name": data["child_full_name"].strip(),
        "child_age": int(data["child_age"]),
        "parent_full_name": data["parent_full_name"].strip(),
        "parent_phone": data["parent_phone"].strip(),
        "parent_email": data["parent_email"].strip(),
        "course_id": int(data["course_id"]),
        "preferred_time": data.get("preferred_time", "").strip(),
        "comment": data.get("comment", "").strip(),
        "status": "Новая",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
    }
    requests.append(record)
    _write_json(REQUESTS_FILE, requests)
    return record
