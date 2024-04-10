# Internal Modules
from models import app, db, User, Group, Post, Membership
from forms import loginUser, RegisterUser, addToDo, createGroup, createMember
# Flask Modules
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
# Security
from werkzeug.security import generate_password_hash, check_password_hash

##  Routes ##

## Login/register/Logout routes
 # Login
@app.route('/', methods=["GET", "POST"])
def index():
    form = loginUser()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(
            db.select(User)
            .where(User.email == form.email.data))
        # Email is unqiue, so will only find single result
        user = result.scalar()
        
        if not user:
            flash("That email does not exist, plase try again")
        elif not check_password_hash(user.password, password):
            flash("Password or email incorrect, please try again")
        else:
            login_user(user)
            return redirect(url_for("get_list")) 
    return render_template("login.html", form=form, loggedIn=current_user.is_authenticated)

 # Register
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        result = db.session.execute(
            db.select(User)
            .where(User.email == form.email.data))
        user = result.scalar()
        #If user exists
        if user:
            flash("You've already signed up, please log in!")
        
        hash_saltedPassword = generate_password_hash(
            form.password.data,
            method='scrypt',
            salt_length=8
        )

        new_user = User(
            email = form.email.data,
            firstName = form.firstName.data,
            lastName = form.lastName.data,
            role = form.role.data,
            password = hash_saltedPassword
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("register.html", form=form, current_user=current_user)

 # Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


## POST CRUD Operations
 # CREATE Post
@app.route("/add", methods=["GET", "POST"])
@login_required
def add_item():
    form = addToDo()
    if form.validate_on_submit():
        new_item = Post(
            title = form.title.data,
            subheading = form.subheading.data,
            content = form.content.data,
            dueDate = form.dueDate.data,
            priority = form.priority.data,
            author = current_user
        )
        db.session.add(new_item)
        db.session.commit()
        print(form.dueDate.data)
        return redirect(url_for("get_list"))
    return render_template("add_item.html", form=form)

 # READ Posts
@app.route("/list", methods=["GET", "POST"])
@login_required
def get_list():
    result = db.session.execute(
        db.select(Post)
        .where(Post.author_id == current_user.id)
        .order_by(Post.priority))
    posts = result.scalars().all()
    return render_template("to_do_list.html", all_posts=posts, current_user=current_user)

 # UPDATE Post
@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_item(id):
    form = addToDo()
    item_to_update = Post.query.get_or_404(id)
    
    if request.method == "POST":
        item_to_update.title = request.form["title"]
        item_to_update.subheading = request.form["subheading"]
        item_to_update.content = request.form["content"]
        item_to_update.dueDate = request.form["dueDate"]
        item_to_update.priority = request.form["priority"]
        item_to_update.author = current_user
        
        try:
            db.session.commit()
            return redirect(url_for("get_list"))
        except:
            flash("Something went wrong!")
            return redirect(url_for("update_item"))
    else:
        return render_template('edit.html', form=form, item_to_update=item_to_update, id=id)

 # DELETE Post
@app.route("/delete/<post_id>", methods=["POST"])
@login_required
def remove_item(post_id):
    item = Post.query.get_or_404(post_id)
    db.session.delete(item)
    db.session.commit()
    flash("Item was deleted")
    return redirect(url_for("get_list"))


## Group CRUD Operations
 # CREATE Group
@app.route("/new-group", methods=["GET", "POST"])
@login_required
def add_group():
    form = createGroup()
    if form.validate_on_submit():
        new_group = Group(
            name = form.name.data,
        )
        db.session.add(new_group)
        db.session.commit()
        return redirect(url_for("read_group"))
    else:
        return render_template('add_group.html', form=form, current_user=current_user)

 # READ Group
@app.route("/group-list", methods=["GET", "POST"])
@login_required
def read_group():
    result = db.session.execute(db.select(Group))
    groups = result.scalars().all()
    return render_template("read_group.html", all_groups=groups)

 # UPDATE Group
@app.route("/update-group/<int:id>", methods=["GET", "POST"])
@login_required
def update_group(id):
    form = createGroup()
    group_to_update = Group.query.get_or_404(id)

    if request.method == "POST":
        group_to_update.name = request.form["name"]

        try:
            db.session.commit()
            return redirect(url_for("read_group"))
        except:
            flash("Something went wrong")
            return redirect(url_for("update_group"))
        
    else:
        return render_template('edit_group.html', form=form, group_to_update=group_to_update, id=id)

 # DELETE Group
@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_group(id):
    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    flash("Item was deleted")
    return redirect(url_for("read_group"))

## Membership CRUD Operations
 # CREATE Memberships
@app.route("/group/<int:id>/new-member", methods=["GET","POST"])
@login_required
def create_membership(id):
    form = createMember()
    groupId = Group.query.get_or_404(id)

    if request.method == "POST":
        result = db.session.execute(
            db.select(User)
            .where(User.email == form.userMember.data)
        )
        user = result.scalar()

        if not user:
            print("That email does not exist, please try again")
        else:
            new_member = Membership(
                userId = user.id,
                groupId = groupId.id,
                role = form.role.data
            )
            db.session.add(new_member)
            db.session.commit()
            return redirect(url_for("read_group"))
    else:
        return render_template("add_member.html", form=form, groupId=groupId)

 # READ Memberships
@app.route("/group/<int:id>/current-members", methods=["GET", "POST"])
@login_required
def read_memberships(id):
    ## Couple of lines below completes a Left outer join for User/Membership tables
   
    members = db.session.query(
        User, Membership).outerjoin(
            Membership, User.id == Membership.userId).where(
                Membership.groupId == id
            )

    print(members)

    userInfoResult = db.session.execute(
        db.select(User)
        .where(User.id == Membership.userId)
    )
    userInfo = userInfoResult.scalars().all()
    return render_template("read_members.html", members=members, userInfo=userInfo)

 # UPDATE Memberships

 # DELETE Memberships


if __name__ == "__main__":
    app.run(debug=True)