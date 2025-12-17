from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import doctor_required
from .forms import AvailabilitySlotForm
from .models import AvailabilitySlot


@doctor_required
def availability_list(request):
    slots = AvailabilitySlot.objects.filter(doctor=request.user)
    return render(request, "doctors/availability_list.html", {"slots": slots})


@doctor_required
def availability_create(request):
    if request.method == "POST":
        form = AvailabilitySlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.doctor = request.user
            slot.save()
            return redirect("doctors:availability_list")
    else:
        form = AvailabilitySlotForm()
    return render(request, "doctors/availability_form.html", {"form": form})


@doctor_required
def availability_update(request, pk):
    slot = get_object_or_404(AvailabilitySlot, pk=pk,
                             doctor=request.user, is_booked=False)
    if request.method == "POST":
        form = AvailabilitySlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            return redirect("doctors:availability_list")
    else:
        form = AvailabilitySlotForm(instance=slot)
    return render(request, "doctors/availability_form.html", {"form": form})


@doctor_required
def availability_delete(request, pk):
    slot = get_object_or_404(AvailabilitySlot, pk=pk,
                             doctor=request.user, is_booked=False)
    if request.method == "POST":
        slot.delete()
        return redirect("doctors:availability_list")
    return render(request, "doctors/availability_confirm_delete.html", {"slot": slot})
