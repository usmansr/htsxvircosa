const express = require('express');
const app = express();
require('dotenv').config();
const nodemailer = require('nodemailer');

// Middleware
app.use(express.static('.'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// View engine
app.set('view engine', 'ejs');

// Email transporter configuration
const transporter = nodemailer.createTransport(
    process.env.SMTP_HOST 
        ? {
            host: process.env.SMTP_HOST,
            port: parseInt(process.env.SMTP_PORT || 587),
            secure: process.env.SMTP_SECURE === 'true',
            auth: {
                user: process.env.SMTP_USER || process.env.MAIL_USER,
                pass: process.env.SMTP_PASSWORD || process.env.MAIL_PASS
            }
        }
        : {
            service: process.env.MAIL_SERVICE || 'gmail',
            auth: {
                user: process.env.MAIL_USER,
                pass: process.env.MAIL_PASS
            }
        }
);

// Routes
app.get('/', (req, res) => {
    res.render('index');
});

app.get('/contact-us', (req, res) => {
    res.render('contact-us');
});

// Contact form submission
app.post('/contact-us', async (req, res) => {
    try {
        const { firstName, lastName, email, phone, topic, message } = req.body;

        if (!firstName || !email || !message) {
            return res.status(400).json({ message: "Required fields missing" });
        }

        // Email 1: Send notification to admin
        await transporter.sendMail({
            from: `"Vircosa" <${process.env.MAIL_USER}>`,
            to: process.env.ADMIN_EMAIL || "support@vircosa.com",
            bcc: process.env.ADMIN_BCC_EMAIL || "ceo@vircosa.com",
            replyTo: email,
            subject: `New Contact Inquiry | ${topic || "General"}`,
            html: `
                <div style="font-family: 'Montserrat', Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                  <h2 style="color: #8B5A2B;">New Contact Message</h2>
                  <div style="background-color: #F8F5F2; padding: 20px; border-radius: 10px;">
                    <p><strong>Name:</strong> ${firstName} ${lastName || ''}</p>
                    <p><strong>Email:</strong> ${email}</p>
                    <p><strong>Phone:</strong> ${phone || "Not provided"}</p>
                    <p><strong>Topic:</strong> ${topic || "Not specified"}</p>
                    <p><strong>Message:</strong><br>${message}</p>
                  </div>
                </div>
            `
        });

        // Email 2: Send confirmation to user
        await transporter.sendMail({
            from: `"Vircosa Customer Care" <${process.env.MAIL_USER}>`,
            to: email,
            subject: `We've Received Your Message - Vircosa`,
            html: `
                <!DOCTYPE html>
                <html>
                <head>
                  <style>
                    body { font-family: 'Montserrat', Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: linear-gradient(135deg, #8B5A2B 0%, #6B4423 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                    .content { background-color: #ffffff; padding: 30px; border: 1px solid #e0e0e0; }
                    .footer { background-color: #F8F5F2; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; color: #666; }
                    .highlight { background-color: #FFF8F0; padding: 15px; border-left: 4px solid #8B5A2B; margin: 20px 0; }
                    .button { display: inline-block; padding: 12px 30px; background-color: #8B5A2B; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                  </style>
                </head>
                <body>
                  <div class="container">
                    <div class="header">
                      <h1 style="margin: 0;">Thank You for Contacting Vircosa</h1>
                    </div>
                    <div class="content">
                      <p>Dear ${firstName},</p>
                      
                      <p>We've successfully received your message and wanted to confirm that it's now in our queue. Our team will review your inquiry and respond within <strong>2 hours or less</strong> during business hours.</p>
                      
                      <div class="highlight">
                        <h3 style="margin-top: 0; color: #8B5A2B;">Your Inquiry Details:</h3>
                        <p><strong>Topic:</strong> ${topic || "General Inquiry"}</p>
                        <p><strong>Your Message:</strong><br>${message}</p>
                      </div>
                      
                      <h3 style="color: #8B5A2B;">What Happens Next?</h3>
                      <ul>
                        <li>Our specialist will review your inquiry carefully</li>
                        <li>You'll receive a personalized response via email</li>
                        <li>If urgent, we may contact you via phone</li>
                      </ul>
                      
                      <p><strong>Need immediate assistance?</strong><br>
                      Call us at <a href="tel:+923124910474" style="color: #8B5A2B;">+92 312 4910474</a><br>
                      Mon-Fri: 9:00 AM - 5:00 PM PST</p>
                    </div>
                    <div class="footer">
                      <p><strong>Vircosa</strong><br>
                      Phase 1, Johar Town, Lahore<br>
                      Email: info@vircosa.com | Phone: +92 312 4910474</p>
                    </div>
                  </div>
                </body>
                </html>
            `
        });

        res.redirect('/contact-us?' + new URLSearchParams({
            success: 'true',
            firstName: firstName || 'There',
            topic: topic || 'General Inquiry',
            message: message ? message.substring(0, 200) : ''
        }).toString());
    } catch (error) {
        console.error('Contact form error:', error);
        res.redirect('/contact-us?error=true');
    }
});

app.listen(process.env.PORT || 3000, () => {
    console.log(`Server is running on port ${process.env.PORT || 3000}`);
});