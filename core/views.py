from urllib.parse import urlencode

from django.shortcuts import redirect, render
from django.urls import reverse

from core import storage


def _base_context(**extra):
    ctx = {
        "product_name": storage.PRODUCT_NAME,
        "version": storage.VERSION,
    }
    ctx.update(extra)
    return ctx


def home(request):
    return render(
        request,
        "core/home.html",
        _base_context(description=storage.PRODUCT_DESCRIPTION),
    )


def request_list(request):
    courses = {c["id"]: c for c in storage.load_courses()}
    items = []
    for row in storage.load_requests():
        course = courses.get(row["course_id"], {})
        items.append(
            {
                **row,
                "course_name": course.get("name", "—"),
            }
        )
    return render(
        request,
        "core/request_list.html",
        _base_context(requests=items),
    )


def request_create(request):
    courses = storage.load_courses()
    if request.method == "POST":
        required = [
            "child_full_name",
            "child_age",
            "parent_full_name",
            "parent_phone",
            "parent_email",
            "course_id",
        ]
        missing = [f for f in required if not str(request.POST.get(f, "")).strip()]
        if missing:
            params = urlencode(
                {
                    "reason": "empty_fields",
                    "detail": "Заполните все обязательные поля заявки.",
                }
            )
            return redirect(f"{reverse('access_denied')}?{params}")

        try:
            child_age = int(request.POST["child_age"])
            course_id = int(request.POST["course_id"])
        except (TypeError, ValueError):
            params = urlencode(
                {
                    "reason": "invalid_data",
                    "detail": "Возраст и курс должны быть указаны числами.",
                }
            )
            return redirect(f"{reverse('access_denied')}?{params}")

        ok, message = storage.age_fits_course(child_age, course_id)
        if not ok:
            params = urlencode({"reason": "age_mismatch", "detail": message})
            return redirect(f"{reverse('access_denied')}?{params}")

        record = storage.add_request(request.POST)
        return redirect("request_detail", pk=record["id"])

    return render(
        request,
        "core/request_form.html",
        _base_context(courses=courses),
    )


def request_detail(request, pk: int):
    record = storage.get_request(pk)
    if record is None:
        params = urlencode(
            {
                "reason": "not_found",
                "detail": f"Заявка №{pk} не найдена.",
            }
        )
        return redirect(f"{reverse('access_denied')}?{params}")

    viewer_phone = (request.GET.get("parent_phone") or "").strip()
    if viewer_phone and viewer_phone != record["parent_phone"]:
        params = urlencode(
            {
                "reason": "foreign_request",
                "detail": (
                    "Родитель пытался открыть заявку с чужим номером телефона. "
                    "Просмотр контактных данных доступен только владельцу заявки."
                ),
                "attempted": record["public_number"],
            }
        )
        return redirect(f"{reverse('access_denied')}?{params}")

    course = storage.get_course(record["course_id"])
    return render(
        request,
        "core/request_detail.html",
        _base_context(
            item=record,
            course=course,
            viewer_phone=viewer_phone,
        ),
    )


def access_denied(request):
    reason = request.GET.get("reason", "unknown")
    detail = request.GET.get(
        "detail",
        "Система отклонила действие из-за ошибки или недостаточных прав.",
    )
    attempted = request.GET.get("attempted", "")

    reason_titles = {
        "empty_fields": "Пустые обязательные поля",
        "invalid_data": "Недопустимые значения",
        "age_mismatch": "Возраст не подходит к курсу",
        "foreign_request": "Чужая заявка",
        "not_found": "Заявка не найдена",
        "unknown": "Отказ",
    }

    return render(
        request,
        "core/access_denied.html",
        _base_context(
            reason_code=reason,
            reason_title=reason_titles.get(reason, "Отказ"),
            detail=detail,
            attempted=attempted,
        ),
    )
