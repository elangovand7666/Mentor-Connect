from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs

client=MongoClient('mongodb+srv://es:es7666@cluster0.jjxan.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
database=client['sample_db']
collection=database['contacts']
fs = gridfs.GridFS(database)
def index(request):
    l = list(list(i.values()) for i in collection.find({}, {'_id': 0}))
    res={
        'rr':l,
    }
    return render(request,'index.html',res)
def crt(request):
    if(request.method=='GET'):
        return render(request,'crt.html')
    if(request.method=='POST'):
        profile=request.FILES.get('profile')
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        address=request.POST.get('address')
        speciality=request.POST.get('speciality')
        bio=request.POST.get('bio')
        file=request.FILES.get('file')
        profile_id = fs.put(profile.read(), filename=profile.name, content_type=profile.content_type)
        file_id = fs.put(file.read(), filename=file.name, content_type=file.content_type)
        data={'profile':profile_id,'name':name,'specialition':speciality,'desgination':bio,'address':address,'email':email,'phone':phone,'file':file_id}
        collection.insert_one(data)
        messages.success(request, 'Contact created Successfully!')
    return redirect('index')
def search(request):
    name=request.POST.get('name0')
    l=[]
    l1=list(list(i.values()) for i in collection.find({}, {'_id': 0}))
    for i in l1:
        if(name.lower() in i[1].lower()):
            l.append(i)
    print(l)
    if(l!=[]):
            res={
                'rr':l,
            }
            return render(request,'search.html',res)
    if(l==[]):
            messages.success(request, 'No searches Found!')
    return redirect('index')
def delete(request, file_id, image_id):
    phone = request.POST.get('phone')
    print(phone)
    file_id = ObjectId(file_id)
    image_id = ObjectId(image_id)
    fs.delete(file_id)
    fs.delete(image_id)
    collection.delete_one({'phone': phone})
    messages.success(request, 'deleted Successfully!')
    return redirect('index')
def update(request,file_id,image_id):
    if(request.method=='POST'):
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        address=request.POST.get('address')
        speciality=request.POST.get('speciality')
        bio=request.POST.get('bio')
        fs.delete(ObjectId(image_id))
        fs.delete(ObjectId(file_id))
        collection.delete_one({'phone':phone})
        return render(request,'upd.html',{'name': name,'phone': phone,'email': email,'address': address,'speciality':speciality,'bio': bio,'file':file_id})
def update1(request):
    if(request.method=='POST'):
        file=request.FILES.get('file')
        file_id = fs.put(file.read(), filename=file.name, content_type=file.content_type)
        profile=request.FILES.get('profile')
        profile_id = fs.put(profile.read(), filename=profile.name, content_type=profile.content_type)
        data = {
            'profile':profile_id,
            'name':request.POST.get('name'),
            'specialition':request.POST.get('speciality'),
            'designation':request.POST.get('bio'),
            'address':request.POST.get('address'),
            'email':request.POST.get('email'),
            'phone':request.POST.get('phone'),
            'file':file_id,
        }
        collection.insert_one(data)
        messages.success(request, 'updated Successfully!')
        return redirect('index')
def view_pdf(request,file_id):
    try:
        file = fs.get(ObjectId(file_id))
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{file.filename}"'
        return response
    except gridfs.errors.NoFile:
        return HttpResponse("File not found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def view_image(request, file_id):
    try:
        file = fs.get(ObjectId(file_id))
        response = HttpResponse(file.read(), content_type=file.content_type)  # Ensure content_type is correct
        response['Content-Disposition'] = f'inline; filename="{file.filename}"'
        return response
    except gridfs.errors.NoFile:
        return HttpResponse("Image not found.", status=404)
        