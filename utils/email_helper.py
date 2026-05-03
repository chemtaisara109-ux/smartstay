"""
Email utilities for SmartStay
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import get_config

config = get_config()

def send_email(to_email, subject, body):
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = config.MAIL_DEFAULT_SENDER
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(config.MAIL_SERVER, config.MAIL_PORT)
        server.starttls()
        server.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(config.MAIL_DEFAULT_SENDER, to_email, text)
        server.quit()

        print(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Email send failed: {e}")
        return False

def send_booking_confirmation(guest_email, booking_details):
    """Send booking confirmation email to guest"""
    subject = f"Booking Confirmation - SmartStay #{booking_details['id']}"

    body = f"""
    <html>
    <body>
        <h2>🎉 Booking Confirmed!</h2>
        <p>Dear Guest,</p>
        <p>Your booking has been successfully confirmed. Here are the details:</p>

        <h3>Booking Details</h3>
        <ul>
            <li><strong>Booking ID:</strong> {booking_details['id']}</li>
            <li><strong>Property:</strong> {booking_details['property_title']}</li>
            <li><strong>Location:</strong> {booking_details['location']}</li>
            <li><strong>Check-in:</strong> {booking_details['check_in']}</li>
            <li><strong>Check-out:</strong> {booking_details['check_out']}</li>
            <li><strong>Guests:</strong> {booking_details['guests']}</li>
            <li><strong>Total Price:</strong> KES {booking_details['total_price']}</li>
        </ul>

        <h3>Host Contact</h3>
        <p><strong>Name:</strong> {booking_details['host_name']}</p>
        <p><strong>Email:</strong> {booking_details['host_email']}</p>

        <p>If you have any questions, please contact your host directly.</p>

        <p>Thank you for choosing SmartStay!</p>
        <p>Best regards,<br>SmartStay Team</p>
    </body>
    </html>
    """

    return send_email(guest_email, subject, body)

def notify_host_of_booking(host_email, booking_details):
    """Notify host of new booking"""
    subject = f"New Booking Request - SmartStay #{booking_details['id']}"

    body = f"""
    <html>
    <body>
        <h2>🔔 New Booking Request</h2>
        <p>You have received a new booking request for your property.</p>

        <h3>Booking Details</h3>
        <ul>
            <li><strong>Booking ID:</strong> {booking_details['id']}</li>
            <li><strong>Property:</strong> {booking_details['property_title']}</li>
            <li><strong>Guest:</strong> {booking_details['guest_name']}</li>
            <li><strong>Email:</strong> {booking_details['guest_email']}</li>
            <li><strong>Check-in:</strong> {booking_details['check_in']}</li>
            <li><strong>Check-out:</strong> {booking_details['check_out']}</li>
            <li><strong>Guests:</strong> {booking_details['guests']}</li>
            <li><strong>Total Price:</strong> KES {booking_details['total_price']}</li>
        </ul>

        <p>Please log in to your SmartStay dashboard to manage this booking.</p>

        <p>Best regards,<br>SmartStay Team</p>
    </body>
    </html>
    """

    return send_email(host_email, subject, body)