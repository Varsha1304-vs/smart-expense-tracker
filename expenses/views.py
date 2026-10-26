
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Expense, Budget


def home(request):
    if request.method == "POST":
        if request.POST.get("action") == "budget":
            amount = request.POST.get("amount")
            if amount:
                Budget.objects.update_or_create(
                    id=1,
                    defaults={"amount": amount}
                )
            return redirect("home")

        Expense.objects.create(
            title=request.POST.get("title"),
            amount=request.POST.get("amount"),
            category=request.POST.get("category"),
            date=request.POST.get("date")
        )
        return redirect("home")

    expenses = Expense.objects.all().order_by("-date")
    total = sum(e.amount for e in expenses)

    today = timezone.localdate()
    monthly_expenses = expenses.filter(
        date__year=today.year,
        date__month=today.month
    )
    month_spent = sum(e.amount for e in monthly_expenses)

    budget_obj = Budget.objects.filter(id=1).first()
    budget = budget_obj.amount if budget_obj else 5000
    remaining = budget - month_spent
    percent = min(float(month_spent / budget * 100), 100) if budget > 0 else 0

    return render(request, "home.html", {
        "expenses": expenses,
        "total": total,
        "budget": budget,
        "month_spent": month_spent,
        "remaining": remaining,
        "percent": percent,
    })


def delete_expense(request, id):
    if request.method == "POST":
        get_object_or_404(Expense, id=id).delete()
    return redirect("home")


def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id)

    if request.method == "POST":
        expense.title = request.POST.get("title")
        expense.amount = request.POST.get("amount")
        expense.category = request.POST.get("category")
        expense.date = request.POST.get("date")
        expense.save()
        return redirect("home")

    return render(request, "edit.html", {"expense": expense})
