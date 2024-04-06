from flask import Flask, render_template, request
import requests
import smtplib

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods = ['get', 'post'])
def contact():
    if request.method == 'POST':
        return recieve_data()
    else:
        return render_template("contact.html", msg_send = False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


# @app.route('/form_entry', methods = ['post'])
def recieve_data ():
    name = request.form['name']
    email = request.form['email']
    cel = request.form['phone']
    message = request.form['message']
    my_email = 'jaimevillalbaoyola@gmail.com'
    password = 'sjgwizpxcgmesaps'
    info = f'Name: {name}\nEmail: {email}\nCel: {cel}\nMessage: {message}'
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls() #make the conection secure
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, 
                            to_addrs='cryptobluewolf@gmail.com', 
                            msg=f"Subject:Data\n\n{info}"
                            )
    return render_template("contact.html", msg_send = True)

if __name__ == "__main__":
    app.run(debug=True, port=5001)


