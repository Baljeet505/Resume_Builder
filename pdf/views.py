from django.shortcuts import redirect, render
from .models import Profile  # Import your Profile model
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

def accept(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        summary = request.POST.get("summary", "")
        school = request.POST.get("school", "")
        degree = request.POST.get("degree", "")
        university = request.POST.get("university", "")
        previous_work = request.POST.get("previous_work", "")
        skills = request.POST.get("skills", "")

        # Create a Profile object using the retrieved data
        profile = Profile(
            name=name,
            email=email,
            phone=phone,
            summary=summary,
            school=school,
            degree=degree,
            university=university,
            previous_work=previous_work,
            skills=skills,
        )

        # Save the Profile object to the database
        profile.save()

    return render(request, 'pdf/index.html')

def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile': user_profile})

    # Specify the path to wkhtmltopdf executable
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }

    # Use the configured path to wkhtmltopdf
    pdf = pdfkit.from_string(html, False, options, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    return response

def list(request):
    profile = Profile.objects.all()
    return render(request,'pdf/list.html',{'profile':profile})


def Delete_list(request,id):
    profile = Profile.objects.get(id=id)

    if request.method =="POST":
        profile.delete()
        return redirect('accept')
    
    return render(request,'pdf/confirm_delete.html',{'profile':profile})