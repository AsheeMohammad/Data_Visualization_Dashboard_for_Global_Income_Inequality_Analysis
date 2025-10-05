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
