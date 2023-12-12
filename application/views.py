from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.db import connection  # Import the connection object to execute raw SQL queries
from django.http import HttpResponse
from django.utils import timezone 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# @login_required
# def secure_view(request):
#     # This view will only be accessible to logged-in users.
#     # You can perform user-specific actions here.
#     return render(request, 'secure_template.html', context)

def admin_login(request):
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        password = request.POST.get('password')

     
        sql_query = """
            SELECT * FROM User_Data
            WHERE emailId = %s AND password_hash = %s AND registering_as = 'Admin'
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query, [admin_id, password])
            user = cursor.fetchone()

        if user:
           return redirect('admin_portal') 
        else:
            return render(request, 'error.html')

       

    return render(request, 'admin_login.html')


# Create your views here.
def home(request):
    return render(request, 'home.html')
def about_us(request):
    return render(request, 'about.html')
def contact_us(request):
    return render(request, 'contact_us.html')

def register(request):
    return render(request, 'register.html')

def admin_portal(request):
    with connection.cursor() as cursor:
        sql_query = "SELECT * FROM User_Data WHERE registering_as = 'specialist';"
        cursor.execute(sql_query)
        data = dictfetchall(cursor)
    context = {
        'specialists': data
    }
    
    return render(request, 'admin_portal.html', context)


def all_patient_list(request):
    with connection.cursor() as cursor:
        sql_query = "SELECT * FROM Reports;"
        cursor.execute(sql_query)
        data = dictfetchall(cursor)
    context = {
        'reports': data
    }
    # print(context)
    return render(request, 'all_patient_list.html', context)

def dictfetchall(cursor):
    # Helper function to fetch all rows as dictionaries
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def register_specialist(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        emailId = request.POST['emailId']
        phone_number = request.POST['phone_number']
        education = request.POST['education']
        university = request.POST['university']
        residential_city = request.POST['residential_city']
        residential_district = request.POST['residential_district']
        password = request.POST['password_hash']
        password_hash = make_password(password)

        insert_query = """
            INSERT INTO User_Data (
                full_name, emailId, phone_number, registering_as, password_hash,
                education, university, city, district
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (full_name, emailId, phone_number, 'specialist', password_hash, education, university, residential_city, residential_district)

        with connection.cursor() as cursor:
            cursor.execute(insert_query, data)

        subject = 'Successful Registration as a Cardiologist'
        message = f'Dear {full_name},\n\nCongratulations! We are pleased to inform you that your registration as a Cardiologist has been successfully processed. \nWelcome to our team!\n\nThanks and Regards,\nSevasadan Cardio Care.'
        from_email = 'sevasadancardio@gmail.com'  # Replace with a valid sender email address

        print(full_name) 
        send_mail(subject, message, from_email, [emailId])
        print("Mail Sent!!")

        return render(request, 'register_success.html')
    else:
        return render(request, 'register_specialist.html')

from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.db import connection

def register_lab_assistant(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        emailId = request.POST['emailId']
        phone_number = request.POST['phone_number']
        education = request.POST['education']
        university = request.POST['university']
        lab_name = request.POST['lab_name']
        lab_address = request.POST['lab_address']
        lab_city = request.POST['lab_city']
        lab_district = request.POST['lab_district']
        password = request.POST['password_hash']
        password_hash = make_password(password)

        insert_query = """
            INSERT INTO User_Data (
                full_name, emailId, phone_number, registering_as, password_hash,
                education, university, lab_name, lab_address, city, district
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (full_name, emailId, phone_number, 'lab assistant', password_hash, education, university, lab_name, lab_address, lab_city, lab_district)

        with connection.cursor() as cursor:
            cursor.execute(insert_query, data)
        
        subject = 'Successful Registration as a Lab Assistant'
        message = f'Dear {full_name},\n\nCongratulations! We are pleased to inform you that your registration as a Lab Assistant has been successfully processed. \nWelcome to our team!\n\nThanks and Regards,\nSevasadan Cardio Care.'
        from_email = 'sevasadancardio@gmail.com'  # Replace with a valid sender email address

        print(full_name) 
        send_mail(subject, message, from_email, [emailId])
        print("Mail Sent!!")

        return render(request, 'register_success.html')
    else:
        return render(request, 'register_lab_assistant.html')


def lab_assistant_list(request):
    with connection.cursor() as cursor:
        sql_query = "SELECT * FROM User_Data WHERE registering_as = 'lab assistant';"
        cursor.execute(sql_query)
        data = dictfetchall(cursor)
    context = {
        'assistants': data
    }
    
    return render(request, 'lab_assistant_list.html', context)

from django.contrib.auth.hashers import check_password

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        usertype = request.POST['usertype']

        # Retrieve the hashed password from the database
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT password_hash,id FROM User_Data WHERE emailId = %s AND registering_as = %s",
                [email, usertype]
            )
            hashed_password = cursor.fetchone()

        if hashed_password and check_password(password, hashed_password[0]):
            if usertype =='specialist':
                context = {
                    'id':hashed_password[1],
                }
                return redirect('specialist_home',id=context['id'])  # Passwords match, user is logged in
            else:
                context = {
                    'id':hashed_password[1],
                }
                return redirect('lab_assistant_home',id=context['id'])
        else:
            return render(request, 'error.html')  # Passwords do not match, show an error

    return render(request, 'login.html')

def specialist_home(request, id):
    lab_assistant_id = None
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        comment = request.POST.get('comment')
        case_severity = request.POST.get('case_severity')
        lab_assistant_id=request.POST.get('lab_assistant_id')
        print(lab_assistant_id)

        # Define the SQL query to update the specialist comments and case severity
        sql_query = """
            UPDATE Reports
            SET specialist_comments = %s, overall_condition = %s
            WHERE report_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [comment, case_severity, report_id])

    # Fetch the reports assigned to the specialist with the given ID
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM Reports WHERE assigned_to_specialist = %s AND specialist_comments = 'Not Prescribed Yet'",
            [id]
        )
        reports = dictfetchall(cursor)

    context = {
        'reports': reports,
        'id': id,
    }

    # Fetch the lab assistant's email based on lab_assistant_id
    if lab_assistant_id is not None:
        # Fetch the lab assistant's email based on lab_assistant_id
        sql_fetch_lab_assistant_email = """
            SELECT emailId FROM User_Data WHERE id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql_fetch_lab_assistant_email, [lab_assistant_id])
            result = cursor.fetchone()

        if result is not None:
            lab_assistant_email = result[0]

            # Send email notification
            subject = 'New case severity Submitted'
            message = f'Hi,\n\nA new report has been submitted with case severity {case_severity}. Please review it.\n\nThanks and Regards,\nSevasadan Cardio Care.'
            from_email = 'sevasadancardio@gmail.com'  # Replace with a valid sender email address
            send_mail(subject, message, from_email, [lab_assistant_email])
            print("Mail Sent!")
    return render(request, 'specialist_home.html', context)


# ///////////////////////////Original/////////////////////////////
def lab_assistant_home(request, id):
    if request.method == 'POST':
        patient_id = request.POST['patient_id']
        patient_name = request.POST['patient_name']
        patient_age = request.POST['patient_age']
        patient_gender = request.POST['patient_gender']
        assigned_to_specialist_id = request.POST['assigned_to_specialist']
        report_data = request.FILES['report_data'].read()
        lab_assistant_id = id  # Get lab_assistant_id from function argument
        added_on_date_time = timezone.now()  # Get the current date and time

        # Fetch lab assistant details from the User_Data table
        with connection.cursor() as cursor:
            lab_assistant_query = "SELECT full_name, lab_name, lab_address, city FROM User_Data WHERE id = %s;"
            cursor.execute(lab_assistant_query, [lab_assistant_id])
            lab_assistant_details = cursor.fetchone()
            lab_assistant_name = lab_assistant_details[0]
            lab_name = lab_assistant_details[1]
            lab_address = lab_assistant_details[2]
            lab_city = lab_assistant_details[3]

        # Fetch additional information about the assigned specialist
        with connection.cursor() as cursor:
            specialist_query = "SELECT full_name, education, city FROM User_Data WHERE id = %s;"
            cursor.execute(specialist_query, [assigned_to_specialist_id])
            specialist_details = cursor.fetchone()
            specialist_name = specialist_details[0]
            specialist_education = specialist_details[1]
            specialist_city = specialist_details[2]

        # Insert the report into the Reports table
        sql_query = """
            INSERT INTO Reports (patient_id, lab_assistant_id, patient_name, patient_age, patient_gender, assigned_to_specialist, report_data, added_on_date_time,  lab_name, lab_address, lab_city, lab_assistant_name, assigned_doctor_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [
                patient_id, lab_assistant_id, patient_name, patient_age, patient_gender,
                assigned_to_specialist_id, report_data, added_on_date_time,
                 lab_name, lab_address, lab_city, lab_assistant_name, f"{specialist_name} ({specialist_education}, {specialist_city})"
            ])
        # Fetch specialist email from the User_Data table
        with connection.cursor() as cursor:
            specialist_query = "SELECT emailId FROM user_data WHERE id = %s;"
            cursor.execute(specialist_query, [assigned_to_specialist_id])
            specialist_email = cursor.fetchone()[0]

        subject = 'New Report Submitted'
        message = f'Dear {specialist_name},\n\nA new report has been submitted by lab assistant {lab_assistant_name} for patient {patient_name}. Please review it.\n\nThanks and Regards,\nSevasadan Cardio Care.'
        from_email = 'sevasadancardio@gmail.com'  # Replace with a valid sender email address

        print(specialist_email)
        send_mail(subject, message, from_email, [specialist_email])
        print("Mail Sent!!")

        return render(request, 'upload_success.html')
    else:
        with connection.cursor() as cursor:
            sql_query = "SELECT * FROM User_Data WHERE registering_as = 'specialist';"
            cursor.execute(sql_query)
            data = dictfetchall(cursor)
            context = {
                'specialists': data,
                'id': id,
            }

        return render(request, 'lab_assistant_home.html', context)

from django.core.mail import send_mail
from django.db import connection
from django.shortcuts import render
from django.utils import timezone



from django.shortcuts import render
from django.db import connection
from django.utils import timezone

from django.shortcuts import render
from django.db import connection
from django.utils import timezone


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]





def upload_success(request):
    return render(request,'upload_success.html')

def show_report(request, report_id):
    # Fetch the report data from the database
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT report_data
            FROM Reports
            WHERE report_id = %s
            """,
            [report_id]
        )
        report_data = cursor.fetchone()

    if report_data:
        # Prepare the HTTP response with the report data
        response = HttpResponse(report_data[0], content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="report-{report_id}.pdf"'
        return response
    else:
        return HttpResponse("Report not found", status=404)
def view_specialist_previous_reports(request, id):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        comment = request.POST.get('comment')
        case_severity = request.POST.get('case_severity')

        # Define the SQL query to update the specialist comments and case severity
        sql_query = """
            UPDATE Reports
            SET specialist_comments = %s, overall_condition = %s
            WHERE report_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql_query, [comment, case_severity, report_id])

        
           

    # Fetch the reports assigned to the specialist with the given ID
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM Reports WHERE assigned_to_specialist = %s AND specialist_comments != 'Not Prescribed Yet'",
            [id]
        )
        reports = dictfetchall(cursor)

    context = {
        'reports': reports,
        'id':id,
    }
    return render(request, 'view_specialist_previous_reports.html', context)

def view_assistant_previous_reports(request, id):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        
        # Define the SQL query to update the specialist comments
        sql_query = """
            DELETE FROM Reports
            WHERE report_id = %s;
        """
        with connection.cursor() as cursor:
           
                cursor.execute(sql_query, [report_id])
                connection.commit()  # Commit the transaction
           

    # Fetch the reports assigned to the specialist with the given ID
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM Reports WHERE lab_assistant_id = %s",
            [id]
        )
        reports = dictfetchall(cursor)

    context = {
        'reports': reports,
        'id':id,
    }
    return render(request, 'view_assistant_previous_reports.html', context)
