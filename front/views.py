from django.shortcuts import render
from django.db import connection,transaction
from django.shortcuts import redirect,reverse
# Create your views here.


def get_cursor():
    return connection.cursor()


def index(request):

    cursor = get_cursor()
    cursor.execute("select id,name,author from book;")
    books = cursor.fetchall()

    # print(books)
    return render(request,'index.html',{'books':books})


def add_book(request):
    name = request.GET.get('name','')
    author = request.GET.get('author','')
    if not name and not author:
        return render(request,'add_book.html')

    cursor = get_cursor()
    cursor.execute("insert into book(name,author) values(%s,%s)",[name,author])
    # books = cursor.fetchall()
    # transaction.commit_unless_managed()
    cursor.close()
    num=cursor.rowcount
    if num > 0:
        return redirect(reverse('index'))
    else:
        render(request,'add_book.html')

def book_detail(request,book_id):
    cursor = get_cursor()
    cursor.execute("select * from book where id=%s",[book_id])
    book = cursor.fetchone()
    cursor.close()
    print(book)

    del_book_id = request.POST.get('id','')
    if del_book_id:
        # del_book_id = int(del_book_id)
        # print(type(del_book_id))
        cursor = get_cursor()
        cursor.execute("delete from book where id=%s", [del_book_id])
        cursor.close()
        book=None

    if book:
        return render(request,'book_detail.html',{'book':book})
    else:
        return redirect(reverse('index'))

