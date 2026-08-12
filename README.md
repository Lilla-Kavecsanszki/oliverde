# Oliverde — Property Management Website

A bespoke Django website designed and developed for Oliverde Property Management Services, a boutique property management company caring for private homes across Tuscany, Umbria and Lazio.

The website is designed primarily for international homeowners who need a trusted local presence in Italy. It presents Oliverde's property management, estate and guest services through an understated, editorial visual identity, while showcasing a curated portfolio of homes under the company's care.

## Live Preview

The project is currently deployed to Heroku as a staging/live preview while final photography, content review and pre-launch testing are completed.

**Staging site:**  
https://oliverde-property-management-2affa78894a3.herokuapp.com/

**Production domain:**  
To be connected at final launch.

---

# Contents

- [Project Overview](#project-overview)
- [User Experience](#user-experience)
- [Planning](#planning)
- [Design](#design)
- [Information Architecture](#information-architecture)
- [App Architecture](#app-architecture)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Data Models](#data-models)
- [Django Admin](#django-admin)
- [SEO and Metadata](#seo-and-metadata)
- [Accessibility and Responsive Design](#accessibility-and-responsive-design)
- [Deployment](#deployment)
- [Testing](#testing)
- [Remaining Pre-Launch Work](#remaining-pre-launch-work)
- [Roadmap](#roadmap)
- [Credits](#credits)


# Project Overview

Oliverde Property Management Services provides ongoing care, maintenance, administration, project oversight and guest support for privately owned homes in central Italy.

The website needed to communicate something more specific than a conventional property-services business.

For an overseas homeowner, choosing a property manager means entrusting someone with access to their home, contractors, utilities, maintenance decisions, guest preparation and potentially significant expenditure while they are hundreds or thousands of kilometres away.

The website therefore focuses on:

- trust and discretion;
- visible evidence of real properties under management;
- clear communication;
- local knowledge;
- continuity of care;
- personal service rather than corporate scale;
- and an easy route to start a conversation with Oliverde.

The result is a content-led Django website combining a luxury editorial aesthetic with a database-driven portfolio and practical administration through Django Admin.

[Back to top](#contents)

# User Experience

## Ideal Client

The primary user is an international homeowner who:

- owns or is purchasing a property in Tuscany, Umbria or Lazio;
- lives abroad or spends significant periods away from the property;
- wants one trusted local point of contact;
- values discretion, reliability and long-term relationships;
- does not want to coordinate gardeners, cleaners, tradespeople, utilities and repairs remotely;
- expects clear communication and photographic reporting;
- may occasionally require guest or rental support;
- and values quality of service over finding the lowest-cost provider.

A detailed design-thinking client persona was developed during the planning stage to help guide content, hierarchy and UX decisions.

## User Goals

Visitors should quickly be able to answer:

1. What does Oliverde do?
2. Can I trust this company with my home?
3. Do they understand overseas owners?
4. Where do they operate?
5. What kinds of properties do they already manage?
6. What services can they coordinate?
7. Can they support a property that is occasionally rented?
8. How do I contact them?

The site deliberately avoids aggressive lead-generation patterns. Calls to action are positioned as invitations to discuss a property rather than hard sales funnels.

[Back to top](#contents)

# Planning

Development has been iterative and content-led.

The site was built page by page around the real operational structure of Oliverde rather than forcing the business into a generic property-management template.

The process included:

- business and audience analysis;
- client persona development;
- information architecture;
- content collection;
- property and destination structure;
- service taxonomy;
- database modelling;
- brand development;
- UI design;
- Django development;
- admin/CMS configuration;
- responsive design;
- SEO implementation;
- staging deployment;
- and ongoing browser/device QA.

The structure and visual system were repeatedly refined in response to client feedback.

Examples include:

- replacing generic iconography with a bespoke botanical sprig motif;
- developing a dedicated Oliverde monogram;
- removing an early client-login concept;
- replacing a founder portrait section with a more discreet testimonial presentation;
- introducing separate Portfolio pathways for the complete managed collection and properties available for private rental;
- and developing stronger privacy conventions for publicly identifying private residences.

[Back to top](#contents)

# Design

## Brand Identity

The project includes a wider Oliverde digital identity rather than only the website UI.

Brand work includes:

- Oliverde wordmark;
- bespoke "O" monogram;
- subtle keyhole motif;
- favicon suite;
- email signature branding;
- LinkedIn assets;
- colour system;
- typography;
- iconography;
- and reusable website components.

The visual direction is deliberately restrained and editorial, taking cues from Italian country estates, architectural publications and high-end hospitality without making the company appear to be a hotel or holiday-rental agency.

## Colour Palette

| Token | Hex |
|---|---|
| Cream | `#F7F4EC` |
| Stone | `#EDE7D9` |
| Olive 900 | `#232A17` |
| Olive 700 | `#47542C` |
| Olive 400 | `#8B9468` |
| Charcoal | `#23221E` |
| Taupe | `#6E6759` |
| Rust | `#A8592E` |

Olive, cream and stone form the core palette.

Rust is intentionally used sparingly for selected accents, interactive states and details rather than throughout the interface.


## Typography

### Cormorant Garamond

Used for:

- display headings;
- editorial statements;
- property names;
- quotations;
- and selected italic emphasis.

### Inter

Used for:

- body copy;
- navigation;
- labels;
- buttons;
- metadata;
- and interface elements.

The serif/sans-serif pairing helps balance an editorial, heritage-influenced identity with a modern and readable interface.

[Back to top](#contents)

# Information Architecture

The principal public structure is:

```
Home
│
├── Portfolio
│   ├── Our Collection
│   ├── Holiday Rentals
│   ├── Destination
│   └── Property Detail
│
├── Services
│   └── Service Detail
│
├── About
│
├── Journal
│   └── Article Detail
│
└── Contact 
```

The Portfolio deliberately distinguishes between:

**Our Collection**  
The broader collection of private residences managed by Oliverde.

**Holiday Rentals**  
Selected properties under Oliverde's care that are also available for private stays.

This prevents Oliverde from being positioned primarily as a holiday-rental business while still allowing appropriate properties to be marketed for stays.

[Back to top](#contents)

# App Architecture

The Django project is separated according to ownership of data and application responsibility.

### `accounts`

Contains the custom `User` model and role structure.

Current roles include:

- Admin;
- Property Manager;
- Client.

Client-facing accounts are not currently exposed publicly.

### `portfolio`

Owns the principal property-management data, including:

- destinations;
- properties;
- property imagery;
- property amenities;
- services;
- service features;
- service imagery;
- and testimonials.

### `services`

Provides the public service index and individual service views while reading service data from the central `portfolio` models.

### `journal`

Owns the Journal and its publishing functionality, including:

- articles;
- publication controls;
- cover imagery;
- excerpts;
- rich-text content;
- related properties;
- pagination;
- and sitemap integration.

### `core`

Handles site-wide pages and functionality including:

- homepage;
- About;
- Contact and enquiry handling;
- privacy policy;
- cookie policy;
- legal notice;
- custom error views;
- `robots.txt`;
- shared navigation/context;
- and site-wide context processors.

### `config`

Contains project-level configuration including:

- Django settings;
- root URL routing;
- WSGI and ASGI configuration;
- sitemap configuration;
- and production database configuration.

The project intentionally uses Django Admin as the content-management interface rather than introducing a separate page-builder CMS such as Wagtail.


[Back to top](#contents)

# Technology Stack

## Languages

- Python
- HTML
- CSS
- JavaScript
- SQL
- Django Template Language

## Application

- Django 6
- PostgreSQL
- Django Admin
- Django Sitemaps Framework
- django-ckeditor-5

## Production and Infrastructure

- Heroku
- Heroku-26 stack
- Heroku Postgres
- Gunicorn
- dj-database-url
- WhiteNoise
- Compressed Manifest Static Files Storage
- release-phase database migrations

## Media

- Cloudinary
- django-cloudinary-storage
- Pillow

## Front End

- Django Templates
- custom CSS
- vanilla JavaScript
- responsive CSS Grid and Flexbox layouts
- self-hosted Cormorant Garamond and Inter typography

No front-end framework is required.

## Development

- Git
- GitHub
- Visual Studio Code
- python-dotenv
- local PostgreSQL development database

## Email and Security

- Gmail SMTP
- Google App Password authentication
- Cloudflare Turnstile
- Django CSRF protection
- honeypot spam protection
- database-backed cache rate limiting


[Back to top](#contents)

# Features

## Homepage

The homepage acts as the primary introduction to the Oliverde brand and service proposition.

Current features include:

- full-screen photographic hero;
- animated scroll indicator;
- primary consultation CTA;
- portfolio and experience statistics;
- service/value introduction;
- dynamically populated featured properties;
- rental-status indicators where applicable;
- services preview;
- rotating testimonial carousel;
- clickable testimonial navigation;
- automatic testimonial rotation;
- mouse and touch/swipe testimonial interaction;
- "Why international owners choose Oliverde" value proposition;
- photographic consultation CTA;
- and responsive navigation.

Featured properties and testimonials are controlled through Django Admin.

[Back to top](#contents)

## Portfolio

The Portfolio is database-driven rather than being a collection of manually coded pages.

### Portfolio Landing Page

Provides two principal pathways:

- Our Collection
- Holiday Rentals

It also allows users to browse properties geographically through destination records.

The broader Portfolio browsing experience also supports:

- destination filtering;
- property sorting;
- pagination;
- reset-filter controls;
- empty-results states;
- featured-property presentation;
- and published-property filtering.

### Our Collection

Displays published properties currently under Oliverde's care.

### Holiday Rentals

Displays only properties explicitly marked as available for rental.

Rental status is controlled at property level in Django Admin.

A rental banner is rendered only where the property's rental availability is enabled.

### Destination Pages

Destination records can contain:

- name;
- slug;
- region;
- descriptive content;
- cover image;
- and associated properties.

The destination structure also supports Oliverde's discretion strategy. Public-facing locations can remain appropriately broad where identifying the exact town of a private residence would reveal too much information.

### Property Detail Pages

Property pages support:

- privacy-safe editorial property titles;
- property type;
- destination;
- cover imagery;
- descriptive copy;
- bedrooms;
- bathrooms;
- sleeping capacity where relevant;
- land size where appropriate;
- air-conditioning information;
- pool and heated-pool information;
- reusable property amenities;
- associated management services;
- rental status;
- property-specific enquiry CTA;
- and related property discovery.

Property galleries support:

- ordered image administration;
- internal editorial image categories;
- continuous public gallery presentation;
- full-screen lightbox viewing;
- previous and next controls;
- keyboard navigation;
- Escape-to-close behaviour;
- image captions;
- image counters;
- reduced-motion support;
- and responsive presentation.

Public property pages use a stable random UUID as part of the property's public identity. This allows editorial titles and slugs to change without breaking the underlying property reference, while canonical redirects ensure outdated editorial URLs resolve to the current public URL.

Not every property is presented as a rental.

For private residences, identifying details can be intentionally limited.

[Back to top](#contents)

# Services

Services are managed dynamically rather than hard-coded into individual templates.

The service architecture currently covers areas such as:

- post-purchase set-up;
- ongoing property maintenance;
- restoration/project oversight;
- property administration;
- guest and rental support.

Individual service pages can include:

- introduction;
- detailed service features;
- explanatory content;
- CTA;
- and relevant properties.

The navigation reads service records dynamically, allowing services to be updated without rewriting the navigation templates.

[Back to top](#contents)

# About

The About page communicates the human and operational structure behind Oliverde.

It includes:

- company history;
- local expertise;
- long-standing supplier relationships;
- Oliverde's own small operational/support team;
- administrative coordination;
- on-the-ground property and grounds support;
- and a wider vetted network of specialist tradespeople and suppliers.

The intention is to communicate that Oliverde is neither a one-person referral service nor an impersonal large agency.

Owners have a consistent point of contact backed by reliable administrative and on-site support, with specialist contractors brought in where appropriate.

Final photography for this page is still being selected.

[Back to top](#contents)

# Journal

A database-driven Journal has been added to support useful editorial content around property ownership and management in Italy.

Journal articles support:

- title;
- publication metadata;
- cover imagery;
- structured article content;
- headings;
- lists;
- images;
- blockquotes;
- and responsive long-form typography.

The Journal is intended to provide useful owner-focused content while also strengthening the site's organic search footprint over time.

[Back to top](#contents)

# Contact

The Contact page provides a low-friction route for prospective owners to start a conversation with Oliverde.

Features include:

- photographic hero;
- enquiry form;
- name;
- email;
- international telephone validation;
- enquiry type;
- message;
- property-specific rental enquiries;
- server-side validation;
- property UUID validation;
- rental-only property validation;
- Cloudflare Turnstile protection;
- honeypot spam protection;
- cache-backed rate limiting;
- Gmail SMTP notifications;
- database persistence;
- Django Admin integration;
- accessible validation and error states;
- loading state during submission;
- Privacy Policy notice;
- success state;
- and direct company contact information.

The tone is deliberately consultative rather than transactional.

[Back to top](#contents)

# Site-Wide Features

The site includes:

- fixed responsive navigation;
- desktop dropdown navigation;
- full-screen mobile navigation;
- dynamically populated Portfolio destinations;
- dynamically populated Services navigation;
- responsive layouts;
- touch-friendly controls;
- reusable CTA components;
- shared footer;
- legal links;
- favicon suite;
- animated reveal effects;
- reduced-motion handling;
- image fallbacks;
- active navigation states;
- keyboard-accessible controls;
- custom 404 and 500 pages;
- canonical URLs;
- XML sitemap;
- `robots.txt`;
- deferred JavaScript;
- and reusable design tokens.

[Back to top](#contents)

# Data Models

The site is driven by relational Django models rather than static property pages.

Core relationships include:

```
Destination
    │
    ├── Property
    └── Testimonial

Property
    │
    ├── PropertyImage
    ├── PropertyAmenity (many-to-many)
    ├── Service (many-to-many)
    ├── Testimonial
    ├── JournalPost (related properties)
    └── optional rental configuration

Service
    │
    ├── ServiceFeature
    └── ServiceImage

JournalPost
    │
    └── related Property records

User
    │
    └── role-based administration structure
```

Property records include publishing and presentation controls so the public site can remain selective even when more information exists internally.

Important property controls include separate internal and public identities, publication approval, rental availability, featured-property ordering and privacy-safe public URLs.

[Back to top](#contents)

# Django Admin

Django Admin acts as the project's CMS.

The admin interface allows Oliverde to manage content without editing templates.

Administrative functionality includes:

- destinations;
- properties;
- internal and public property identities;
- property publishing status;
- featured-property ordering;
- property types;
- rental availability;
- rental banner text;
- readonly public UUIDs;
- property image galleries and ordering;
- image sections;
- alternative-text fields;
- reusable property amenities;
- property-service assignments;
- property-amenity assignments;
- services;
- service features;
- service image galleries;
- testimonials;
- homepage testimonial selection;
- Journal publishing;
- custom user roles;
- contact enquiry management;
- and linked rental property enquiries.

Inline administration is used where appropriate, including property image galleries, service features and service imagery.

The admin separates private operational information from public editorial information, reducing the risk of sensitive property details being exposed accidentally.

This approach keeps the project lightweight while still providing a practical content-management system for the business.

[Back to top](#contents)

# Privacy and Discretion

Privacy is a deliberate part of the site's information architecture.

Many homes managed by Oliverde are private family residences rather than commercial accommodation.

The website therefore supports an editorial presentation strategy in which:

- property names may be replaced with editorial titles;
- exact locations do not need to be published;
- destination descriptions can remain intentionally broad;
- identifying details can be omitted;
- and only properties explicitly marked for rental are presented as available for stays.

This allows the portfolio to demonstrate the quality and range of Oliverde's work without unnecessarily exposing clients' homes.

## Technical Privacy Implementation

The property architecture separates private operational identity from public editorial identity.

A property may therefore have:

- a private internal title used by Oliverde;
- a public editorial title;
- a privacy-safe public slug;
- a random public UUID;
- and explicit approval controls governing publication.

Public property pages are resolved using the UUID rather than relying solely on an editable title or sequential database ID.

The UUID remains stable if an editorial title or slug changes. Where a visitor uses an outdated slug, the application redirects to the property's current canonical URL.

This approach:

- reduces the risk of internal property names appearing publicly;
- makes property URLs more difficult to enumerate;
- supports discreet editorial naming;
- allows public titles to evolve without breaking permanent references;
- and provides stronger separation between Oliverde's internal records and the public portfolio.

The UUID is not treated as a substitute for authentication. Any future owner dashboards, private documents or confidential reporting would require dedicated access controls.

[Back to top](#contents)

# SEO and Metadata

The site includes a technical SEO foundation rather than relying only on visible page copy.

Implemented elements include:

- page-specific `<title>` support;
- meta descriptions;
- canonical URLs;
- Open Graph metadata;
- Open Graph imagery;
- Twitter/X large-image metadata;
- semantic heading structure;
- descriptive image alternative text where appropriate;
- crawlable Django URLs;
- and structured data.

The site also provides:

- XML sitemap generation;
- static-page sitemap entries;
- property sitemap entries;
- destination sitemap entries;
- service sitemap entries;
- Journal sitemap entries;
- `robots.txt`;
- privacy-safe public property URLs;
- and property-level structured data where applicable.

The homepage includes Schema.org structured data for the Oliverde business, including:

- business name;
- legal name;
- telephone;
- email;
- VAT ID;
- service regions;
- address;
- and website URL.

A default social-sharing image is also supported.

Further search optimisation can continue once the production domain and final photography are in place.

[Back to top](#contents)

# Accessibility and Responsive Design

The website has been designed responsively rather than as a desktop-only layout with a single mobile breakpoint.

Current responsive QA covers key layouts across:

- large desktop;
- small desktop/laptop;
- tablet;
- mobile;
- and small mobile widths.

Responsive work includes:

- fluid page gutters;
- collapsing grids;
- responsive typography;
- mobile navigation;
- touch targets;
- mobile footer restructuring;
- property-gallery behaviour;
- long-form Journal typography;
- responsive CTAs;
- mobile-safe hero layouts;
- and viewport/safe-area considerations.

Accessibility considerations include:

- semantic HTML;
- keyboard-accessible links and controls;
- focus states;
- `aria` attributes where appropriate;
- decorative-image handling;
- reduced-motion support;
- and readable text contrast.

Responsive and accessibility QA is still being completed before final launch.

[Back to top](#contents)

# Deployment

## Production Infrastructure

The application is deployed to Heroku using:

- EU region;
- Heroku-26 stack;
- Eco web dyno;
- Gunicorn;
- Heroku Postgres Essential-0;
- Cloudinary media storage;
- WhiteNoise static-file serving;
- compressed manifest static files;
- private GitHub deployment integration;
- Release-phase database migrations.

The production `Procfile` contains:

```text
release: python manage.py migrate && python manage.py createcachetable
web: gunicorn config.wsgi
```

Heroku:

1. detects the Python application;
2. installs `requirements.txt`;
3. runs `collectstatic`;
4. builds the application slug;
5. runs database migrations during the release phase;
6. starts Gunicorn as the web process.

## Environment Variables

Production secrets and deployment-specific values are stored as Heroku Config Vars.

Required variables include:

```text
DJANGO_SECRET_KEY
DEBUG
ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS
SITE_URL
DATABASE_URL
CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET
SECURE_HSTS_SECONDS

EMAIL_BACKEND
EMAIL_HOST
EMAIL_PORT
EMAIL_USE_TLS
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
EMAIL_TIMEOUT
DEFAULT_FROM_EMAIL
CONTACT_RECIPIENT_EMAIL

TURNSTILE_SITE_KEY
TURNSTILE_SECRET_KEY
TURNSTILE_EXPECTED_HOSTNAME
TURNSTILE_EXPECTED_ACTION
TURNSTILE_TIMEOUT

CONTACT_RATE_LIMIT
CONTACT_RATE_LIMIT_WINDOW
```

`DATABASE_URL` is managed automatically by Heroku Postgres.

Local development uses an untracked `.env` file. The repository includes only a safe `.env.example`.

Secrets must never be committed to Git.

## Local Installation

Clone the repository:

```bash
git clone https://github.com/Lilla-Kavecsanszki/oliverde.git
cd oliverde
```

The repository is private, so authorised GitHub access is required.

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local PostgreSQL database.

Create `.env` using `.env.example` as the guide:

```env
DJANGO_SECRET_KEY=
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=

DATABASE_NAME=oliverde
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=localhost
DATABASE_PORT=5432

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

SITE_URL=http://127.0.0.1:8000
```

Apply migrations:

```bash
python manage.py migrate
```

```bash
python manage.py createcachetable
```

Create an administrator:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Run production checks locally:

```bash
DEBUG=False python manage.py check --deploy
```

Collect static files:

```bash
python manage.py collectstatic --noinput
```

[Back to top](#contents)

# Testing

Completed testing includes:

- Django system checks
- Database migrations
- Property routing
- Canonical URL redirects
- Contact form validation
- International phone validation
- Email validation
- Property UUID validation
- Rental-only enquiry validation
- Gmail SMTP notifications
- Cloudflare Turnstile verification
- Honeypot spam protection
- Cache-backed rate limiting
- Database persistence
- Django Admin integration
- Responsive manual testing

Further work before launch:

- cross-browser testing;
- Lighthouse performance and accessibility audit;
- W3C HTML/CSS validation;
- automated Django tests;
- full manual click-through testing of pages and links;
- full Contact form regression testing, including validation, Turnstile, honeypot and rate-limiting behaviour;
- final in-browser responsive testing at key breakpoints;
- and final Django system checks / `flake8`.

[Back to top](#contents)

# Remaining Pre-Launch Work

## Current Limitations

- No client-facing login or owner portal currently exists.
- Video content is not currently supported.
- Journal categories are not yet implemented.
- Contact notifications currently use Gmail SMTP; a dedicated transactional email service may be adopted if future email volumes require it.
- The platform intentionally uses Django Admin rather than a page-builder CMS.

## Before Public Launch

- complete production content population;
- connect the Oliverde custom domain and `www` domain;
- enable Automated Certificate Management;
- enable the final HSTS configuration once HTTPS is confirmed;
- connect Google Search Console and Bing Webmaster Tools;
- complete automated test coverage;
- complete final legal review;
- and complete cross-browser, responsive, accessibility and Lighthouse QA.

[Back to top](#contents)

# Roadmap

The full development and launch roadmap is maintained in:

[`TODO.md`](TODO.md)

Immediate priorities are:

1. Create and verify the production superuser.
2. Test Cloudinary uploads in production.
3. Populate the five core services.
4. Add destinations, amenities, testimonials, and initial properties.
5. Monitor contact-form delivery in production.
6. Complete the final production legal review.
7. Connect the custom domain and enable SSL.
8. Perform full production QA.
9. Submit the sitemap to Google Search Console and Bing Webmaster Tools.
10. Officially launch the website.

[Back to top](#contents)

# Credits

## Content

Business, property, destination, service, and testimonial content is provided or approved by **Oliverde Property Management Services**.

Property names, identifying details, photographs, and other sensitive information are published only with the appropriate owner's permission.

## Design and Development

Designed and developed by **Lilla Kavecsanszki** using **Django**.

## Photography and Assets

Property photography, branding assets, logos, and illustrations are owned by **Oliverde Property Management Services**, created specifically for the project, or used with the appropriate permission.

Where applicable, selected stock photography is sourced from **Pexels** in accordance with the Pexels Licence.

Third-party photography, illustrations, icons, or other creative assets must not be used without the appropriate licence or explicit permission.

[Back to top](#contents)