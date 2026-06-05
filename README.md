# HTS Axon × Vircosa

Corporate landing website for a Pakistan-based software development and cloud solutions partnership. Showcases services, portfolio, and a contact form with email automation.

## Tech Stack

| Layer | Technology |
|---|---|
| **Runtime** | Node.js |
| **Framework** | Express.js 5 |
| **Templating** | EJS |
| **CSS / UI** | Tailwind CSS (CDN), custom CSS, Font Awesome 6, Google Fonts |
| **Email** | Nodemailer (Zoho SMTP) |
| **CI/CD** | GitHub Actions → Oracle Cloud VM |
| **Production** | PM2 + Nginx (Ubuntu) |
| **Frontend** | Vanilla JS (particle system, custom cursor, carousel, modal, pie menu, scroll animations, tilt effect) |

## Features

- **Landing page** – Hero with animated particle network, stats counters, services cards (5), bento-grid portfolio with modal details, project carousel, process section, CTA
- **Contact page** – CEO-styled hero, contact form (6 fields) with error handling, info cards, Google Maps embed, success modal
- **Email automation** – Dual-email system: admin notification + branded user confirmation via Zoho SMTP
- **Interactive UI** – Custom cursor, particle network, scroll-reveal animations, 3D card tilt, pie menu navigation, tooltips, mobile hamburger menu, navbar shrink on scroll

## Getting Started

```bash
npm install
npm start
```

Server starts on `http://localhost:3000` by default.

### Environment Variables

Create a `.env` file in the project root with your SMTP credentials (see `.env` for reference):

```
SMTP_HOST=smtp.zoho.com
SMTP_PORT=587
SMTP_USER=ceo@vircosa.com
SMTP_PASS=your_password
PORT=3000
```

## Project Structure

```
├── app.js              Express server + email logic
├── views/
│   ├── index.ejs       Landing page
│   └── contact-us.ejs  Contact page
├── pictures/           Portfolio project screenshots
├── .github/workflows/  CI/CD pipeline
└── .env                Environment variables
```

## Deployment

Automated via GitHub Actions to an Oracle Cloud VM (Ubuntu) at `/var/www/vircosa`, managed by PM2 behind Nginx.

Push to the `main` branch to trigger deployment.
