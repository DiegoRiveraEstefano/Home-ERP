---
trigger: always_on
---

# Home-ERP: View Layer Rules

Views act as HTTP bridges: parse incoming requests -> delegate to services/selectors -> return responses (templates, Unpoly partials, JSON).

## 1. Prefer Class-Based Views (CBVs)
- Use Django generic views (`ListView`, `DetailView`, `CreateView`, `UpdateView`).
- Inject behavior via standard methods (`get_queryset`, `get_context_data`, `form_valid`).

## 2. Reuse via Mixins
- Extract shared logic (e.g., household resolution, Unpoly fragment handling, role validation) into mixins.
- Inherit from `HouseholdContextMixin` and `PermissionRequiredMixin`.

## 3. Function-Based Views (FBVs) - Strict Exception
- Permitted only for very small, hyper-specific actions (e.g., a tiny toggle endpoint).
- Must manually secure: use decorators (`@login_required`, `@permission_required`) and enforce `household_id` filtering.

## 4. Zero Business Logic in Views
- Controllers unpack inputs, delegate, and respond. No calculations, complex business validations, or direct DB mutations.
- **Writes -> `services/`** (e.g., `ChoreService.complete_assignment()`).
- **Complex reads -> `selectors.py`** (e.g., `FinanceSelector.get_monthly_summary()`).

## Anti-patterns vs. Correct Patterns

| Anti-pattern | Correct | Why |
|---|---|---|
| Updating account balances inside `post()` | `FinanceService.record_expense(...)` | Keeps business rules testable outside HTTP |
| `queryset.filter(household=request.user.household)` repeated across 50 views | Inherit from `HouseholdContextMixin` | Eliminates manual filtering boilerplate and prevents leaks |
| 400-line CBV overriding internal Django methods | Extract logic to service or selector layer | Maintainable, low cognitive load |
| Unprotected FBV: `Chore.objects.get(id=id).delete()` | `get_object_or_404(Chore, id=id, household_id=request.household_id)` | Prevents IDOR data access |

## Examples

### Standard CBV (Delegation)
```python
from django.views.generic import CreateView
from home_erp.apps.core.mixins import HouseholdContextMixin, PermissionRequiredMixin
from home_erp.apps.finances.models import FinancialTransaction
from home_erp.apps.finances.forms import ExpenseForm
from home_erp.apps.finances.services import FinanceService

class ExpenseCreateView(PermissionRequiredMixin, HouseholdContextMixin, CreateView):
    model = FinancialTransaction
    form_class = ExpenseForm
    permission_required = "finances.add_financialtransaction"
    template_name = "finances/expense_form.html"

    def form_valid(self, form):
        self.object = FinanceService.record_expense(
            household_id=str(self.request.household.id),
            account_id=form.cleaned_data["account"].id,
            category_id=form.cleaned_data["category"].id,
            amount=form.cleaned_data["amount"],
            description=form.cleaned_data["description"],
            user_id=str(self.request.user.id),
        )
        return super().form_valid(form)
```

### Acceptable FBV (Protected, Tiny Unpoly Toggle)
```python
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from home_erp.apps.chores.models import ChoreAssignment
from home_erp.apps.chores.services import ChoreService

@login_required
@permission_required("chores.change_choreassignment", raise_exception=True)
def toggle_chore_complete(request, assignment_id):
    assignment = ChoreService.complete_assignment(
        household_id=str(request.household.id),
        assignment_id=assignment_id,
        completed_by=request.user,
    )
    return HttpResponse(f"<span class='badge badge-success' id='chore-status-{assignment_id}'>{assignment.status}</span>")
```