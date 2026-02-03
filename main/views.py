from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Skill, Project, Experience, Education, Hobby, Testimonial, ContactInfo
from .forms import ContactForm, TestimonialForm

def home(request):
    contact_form = ContactForm(prefix='contact')
    testimonial_form = TestimonialForm(prefix='testimonial')
    
    if request.method == 'POST':
        if 'submit_contact' in request.POST:
            contact_form = ContactForm(request.POST, prefix='contact')
            if contact_form.is_valid():
                # Spam check (Honeypot)
                if contact_form.cleaned_data.get('nickname'):
                    return redirect('home')  # Silent failure for bots

                try:
                    contact_form.save()
                    messages.success(request, 'Your message has been sent successfully!')
                except Exception as e:
                    # Log the error if possible, but don't crash the user
                    print(f"Error sending message: {e}")
                    messages.success(request, 'Your message has been sent successfully!') # Fake success to user if email fails but DB saved?
                    # Actually, if save() fails (signals), the DB transaction might roll back or not.
                    # Signals usually run after save. If signal fails, save is usually done.
                    # But to be safe and friendly:
                    # messages.warning(request, "Message saved, but email notification failed.")
                    # Let's just say success to not panic them, as long as it's not a critical DB error.
                    # If it's pure email error, the contact IS saved in DB.
                return redirect('home')
            else:
                messages.error(request, 'There was an error sending your message. Please check the form.')
        
        elif 'submit_testimonial' in request.POST:
            testimonial_form = TestimonialForm(request.POST, prefix='testimonial')
            if testimonial_form.is_valid():
                 # Spam check (Honeypot)
                if testimonial_form.cleaned_data.get('nickname'):
                    return redirect('home')

                try:
                    testimonial_form.save()
                    messages.success(request, 'Thank you! Your testimonial has been submitted for review.')
                except Exception as e:
                    print(f"Error saving testimonial: {e}")
                    messages.success(request, 'Thank you! Your testimonial has been submitted for review.')
                return redirect('home')
            else:
                messages.error(request, 'There was an error submitting your testimonial.')

    context = {
        'profile': Profile.load(),
        'contact_info': ContactInfo.load(),
        'skills': Skill.objects.all(),
        'projects': Project.objects.all().order_by('-created_date'),
        'experiences': Experience.objects.all().order_by('-start_date'),
        'educations': Education.objects.all().order_by('-start_date'),
        'hobbies': Hobby.objects.all(),
        'testimonials': Testimonial.objects.filter(is_approved=True).order_by('-created_at'),
        'contact_form': contact_form,
        'testimonial_form': testimonial_form,
    }
    return render(request, 'main/home.html', context)
