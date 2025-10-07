# auth.py
from tinydb import TinyDB, Query
import smtplib
from email.mime.text import MIMEText
import random

# Initialize DB (file created automatically)
db = TinyDB("users.json")
users_table = db.table("users")


def signup(email: str, password: str):
    """Register a new user. Returns (success: bool, message: str)."""
    User = Query()
    if users_table.search(User.email == email):
        return False, "User already exists!"
    users_table.insert({"email": email, "password": password})
    return True, "Account created successfully!"


def login(email: str, password: str):
    """Check login credentials. Returns (success: bool, message: str)."""
    User = Query()
    user = users_table.search((User.email == email) & (User.password == password))
    if user:
        return True, "Login successful!"
    return False, "Invalid email or password"


def send_otp(email: str):
    """Send OTP to the given email and return the OTP."""
    otp = str(random.randint(100000, 999999))  # generate 6-digit OTP
    try:
        sender = "asheemohammad123@gmail.com"   # <-- replace with your Gmail
        password = "jxeaeuilwswpfyro"   # <-- replace with Gmail App Password

        msg = MIMEText(f"Your OTP for password reset is: {otp}")
        msg["Subject"] = "Password Reset OTP"
        msg["From"] = sender
        msg["To"] = email

        # Gmail SMTP setup
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, [email], msg.as_string())
        server.quit()

        print("✅ OTP email sent to", email)
        return otp
    except Exception as e:
        print("❌ Error sending email:", e)
        return None

# -------------------------
# Reset password
# -------------------------
def update_password(email: str, new_password: str):
    """Update password in TinyDB."""
    User = Query()
    user = users_table.search(User.email == email)
    if user:
        users_table.update({"password": new_password}, User.email == email)
        return True
    return False

#Edit Profile
def update_profile(old_email: str, new_name: str, new_email: str, new_password: str):
    """Update user profile details in DB"""
    User = Query()
    user = users_table.search(User.email == old_email)

    if not user:
        return False, "User not found!"

    # Update fields
    update_data = {}
    if new_name:
        update_data["name"] = new_name
    if new_email:
        update_data["email"] = new_email
    if new_password:
        update_data["password"] = new_password

    users_table.update(update_data, User.email == old_email)
    return True, "Profile updated successfully!"

