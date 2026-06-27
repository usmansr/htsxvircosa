const express = require('express');
const app = express();
require('dotenv').config();
const nodemailer = require('nodemailer');
const { spawn } = require('child_process');
const path = require('path');
const multer = require('multer');
const fs     = require('fs');

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const dir = './uploads';
        if (!fs.existsSync(dir)) fs.mkdirSync(dir);
        cb(null, dir);
    },
    filename: (req, file, cb) => {
        // unique name to avoid collisions under concurrent requests
        cb(null, `${Date.now()}-${Math.random().toString(36).slice(2)}.csv`);
    }
});

const upload = multer({
    storage,
    limits: { fileSize: 5 * 1024 * 1024 },          // 5 MB hard limit on server too
    fileFilter: (req, file, cb) => {
        if (!file.originalname.toLowerCase().endsWith('.csv')) {
            return cb(new Error('Only CSV files are allowed'));
        }
        cb(null, true);
    }
});

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

app.get('/bakerdays', (req, res) => {
    res.render('bakerdays');
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

app.get('/visualdsa', (req, res) => {
    res.render('visualdsa');
});

app.post('/visualdsa/predict', (req, res) => {
    const { code } = req.body;
    if (!code || !code.trim()) {
        return res.status(400).json({ error: 'No code provided' });
    }

    const scriptPath = path.join(__dirname, 'python', 'milestone2_visualize.py');
    const modelPath  = path.join(__dirname, 'python', 'visualdsa_nb_model.pkl');

    // Pass code via stdin to avoid shell-escaping issues
    const py = spawn('python', [scriptPath, '--model', modelPath], {
        cwd: path.join(__dirname, 'python')
    });

    let stdout = '', stderr = '';
    py.stdin.write(code);
    py.stdin.end();

    py.stdout.on('data', d => stdout += d.toString());
    py.stderr.on('data', d => stderr += d.toString());

    py.on('close', code => {
        if (code !== 0) {
            console.error('Python error:', stderr);
            return res.status(500).json({ error: 'Prediction failed', detail: stderr });
        }
        try {
            const result = JSON.parse(stdout);
            res.json(result);
        } catch (e) {
            console.error('Parse error. stdout:', stdout);
            res.status(500).json({ error: 'Bad response from Python' });
        }
    });
});

app.get('/ml', (req, res) => {
    res.render('ml');
});

app.post('/api/ml/analyze', upload.single('file'), (req, res) => {
    const csvPath   = req.file?.path;
    const target    = req.body?.target;
    const task      = req.body?.task;

    // Guard: missing fields
    if (!csvPath || !target || !task) {
        if (csvPath) fs.unlinkSync(csvPath);
        return res.status(400).json({ error: 'Missing file, target column, or task type.' });
    }

    const scriptPath = path.join(__dirname, 'python', 'ml_engine.py');  

    // Spawn Python — pass csv path, target column, task type as argv
    const pyCmd = process.platform === 'win32' ? 'python' : 'python3';
    const py = spawn(pyCmd, [scriptPath, csvPath, target, task]);

    let stdout = '';
    let stderr = '';

    py.stdout.on('data', d => stdout += d.toString());
    py.stderr.on('data', d => stderr += d.toString());

    py.on('close', (code) => {
        // Always delete the temp CSV regardless of outcome
        try { fs.unlinkSync(csvPath); } catch (_) {}

        if (code !== 0) {
            console.error('[ml_engine] stderr:', stderr);
            return res.status(500).json({ error: 'ML engine failed', detail: stderr });
        }

        try {
            const result = JSON.parse(stdout);
            if (result.error) {
                return res.status(422).json({ error: result.error });
            }
            res.json(result);
        } catch (e) {
            console.error('[ml_engine] bad stdout:', stdout);
            res.status(500).json({ error: 'Invalid response from ML engine' });
        }
    });

    // Handle spawn errors (e.g. python3 not found)
    py.on('error', (err) => {
        try { fs.unlinkSync(csvPath); } catch (_) {}
        console.error('[ml_engine] spawn error:', err);
        res.status(500).json({ error: 'Could not start ML engine', detail: err.message });
    });
});

// Multer error handler — catches file size / type rejections
app.use((err, req, res, next) => {
    if (err.code === 'LIMIT_FILE_SIZE') {
        return res.status(413).json({ error: 'File too large. Maximum size is 5MB.' });
    }
    if (err.message === 'Only CSV files are allowed') {
        return res.status(400).json({ error: err.message });
    }
    next(err);
});


app.listen(process.env.PORT || 3000, () => {
    console.log(`Server is running on port ${process.env.PORT || 3000}`);
});