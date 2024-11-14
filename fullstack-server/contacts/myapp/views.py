from django.shortcuts import render,redirect
from django.http import HttpResponse
from pymongo import MongoClient
from django.contrib import messages
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import smtplib
import gridfs
from bson import ObjectId

client=MongoClient('mongodb+srv://es:es7666@cluster0.jjxan.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
database=client['sample_db']
collection=database['contacts']
fs=gridfs.GridFS(database)
def index(request):
    fotp=request.POST.get('fotp','')
    otp=request.POST.get('otp','')
    print(fotp,otp)
    if(str(fotp)==str(otp)):
        l=list(list(i.values()) for i in collection.find({}, {'_id': 0}))
        res={
            'rr':l
        }
        #messages.success(request,"Welcome to Mentor connect")
        return render(request,'index.html',res)
    else:
        messages.error(request,"Invalid Otp")
        return redirect('login')
def search(request):
    k=request.POST.get('name0')
    a=list(k.split())
    l=list(list(i.values()) for i in collection.find({}, {'_id': 0}))
    l1=[]
    for i in l:
        for j in a:
            if(j.lower() in i[2].lower()) or(j.lower() in i[1].lower()):
                l1.append(i)
                break
    if(l1!=[]):
        return render(request,'developer.html',{'name':f"{k.capitalize()}",'l1':l1})
    messages.success(request,"No searches has been Found!!")
    return redirect('index')
def login(request):
    return render(request,'login.html')
random_number=None
def email(request):
    random_number = random.randint(100000, 999999)
    if(request.method=='GET'):
        return render(request,'login.html')
    if(request.method=='POST'):
        email=request.POST.get('email')
        def send_email(sender_email, receiver_email, subject, body, password):
            # Set up the MIME
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject

            # Attach the body to the email
            message.attach(MIMEText(body, 'plain'))

            try:
                # Create an SMTP session for sending the email
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()  # Secure the connection
                    server.login(sender_email, password)  # Log in to your account
                    text = message.as_string()  # Convert the message to a string
                    server.sendmail(sender_email, receiver_email, text)  # Send the email

                print("Email sent successfully!")

            except Exception as e:
                print(f"Failed to send email. Error: {str(e)}")

        # Example usage
        sender = 'sekartmrelangovan@gmail.com'
        receiver = email
        subject = 'Test Email'
        body = f'Your OTP is: {random_number}\nPlease use this code to complete your verification.For security, don’t share it with anyone.'
        password = 'tvpq iysg qdqy agjx'  # Use a secure method to store passwords

        send_email(sender, receiver, subject, body, password)
        return render(request,'email.html',{'fotp':random_number})
def view_pdf(request,file_id):
    try:
        file = fs.get(ObjectId(file_id))
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{file.filename}"'
        return response
    except gridfs.errors.NoFile:
        messages.success("File not found.")
        return redirect('index')
    except Exception as e:
        messages.success(f"An error occurred: {str(e)}")
        return redirect('index')
    
def view_image(request, file_id):
    try:
        file = fs.get(ObjectId(file_id))
        response = HttpResponse(file.read(), content_type=file.content_type)  # Ensure content_type is correct
        response['Content-Disposition'] = f'inline; filename="{file.filename}"'
        return response
    except gridfs.errors.NoFile:
        return HttpResponse("Image not found.", status=404)
