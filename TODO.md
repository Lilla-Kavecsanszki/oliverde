# Oliverde Website Roadmap

---

# ✅ Phase 1 – Project Setup

- [x] Django project setup
- [x] PostgreSQL
- [x] GitHub repository
- [x] Project structure
- [x] Models
- [x] Django Admin
- [x] Database migrations
- [x] Custom user model

---

# ✅ Phase 2 – Design System

- [x] Colour palette
- [x] Typography
- [x] Components
- [x] Base template
- [x] Navigation
- [x] Dropdown navigation
- [x] Mobile navigation
- [x] Active navigation states
- [x] Footer
- [x] Responsive design system
- [x] Self-hosted fonts
- [x] Reduced-motion support
- [x] Keyboard accessibility improvements

---

# ✅ Phase 3 – Homepage ⭐

- [x] Hero
- [x] Introduction
- [x] Services preview
- [x] Featured properties
- [x] Statistics
- [x] Testimonials
- [x] Testimonial carousel
- [x] CTA
- [x] Homepage structured data

---

# ✅ Phase 4 – Portfolio

- [x] Portfolio overview
- [x] Destination cards
- [x] Featured properties
- [x] All-properties page
- [x] Pagination
- [x] Destination filtering
- [x] Property sorting
- [x] Filter reset
- [x] Empty-results state
- [x] Related navigation
- [x] Portfolio URL structure

---

# ✅ Phase 5 – Destination Pages

- [x] Destination hero
- [x] Destination introduction
- [x] Property listings
- [x] Internal navigation
- [x] Published-property filtering
- [x] Destination testimonial support

---

# ✅ Phase 6 – Property Pages ⭐

- [x] Property hero
- [x] Cover image
- [x] Editorial gallery
- [x] Gallery sections
- [x] Property gallery JavaScript
- [x] Description
- [x] Property facts
- [x] Services
- [x] Related properties
- [x] Contact enquiry link
- [x] Published-property protection
- [x] Property structured data

---

# ✅ Phase 7 – Services

- [x] Services overview
- [x] Individual service sections
- [x] Service features
- [x] CTA
- [x] Services sitemap integration

---

# ✅ Phase 8 – About

- [x] Company story
- [x] Founder section
- [x] Values
- [x] CTA
- [x] About-page metadata

---

# 🚧 Phase 9 – Contact ⭐

- [x] Contact page
- [x] Property-specific enquiry parameters
- [x] Contact form
- [x] Form validation
- [x] Django Messages
- [x] Success / error message styling
- [x] Privacy Policy notice
- [ ] MailerSend integration
- [ ] Production email testing

---

# 🚧 Phase 10 – Production Polish

## SEO

- [x] Sitemap.xml
- [x] Static-page sitemap
- [x] Property sitemap
- [x] Destination sitemap
- [x] Services sitemap
- [x] Journal sitemap
- [x] robots.txt
- [x] Canonical URLs
- [x] Structured Data (JSON-LD)
- [x] Metadata
- [x] Open Graph structure
- [ ] Final social-sharing images
- [ ] Google Search Console
- [ ] Bing Webmaster Tools

## Legal

- [x] Privacy Policy
- [x] Cookie Policy
- [x] Legal Notice

## Error Pages

- [x] Custom 404 page
- [x] Custom 404 handler
- [x] Custom 500 page
- [ ] Test error pages with `DEBUG=False`

## Static Files and Media

- [x] Static files structure
- [x] Static root configuration
- [x] Cloudinary media storage configuration
- [x] WhiteNoise middleware
- [x] Compressed manifest static-file storage
- [ ] Add missing favicon files
- [ ] Run final production `collectstatic`
- [ ] Verify Cloudinary uploads in production

## Security

- [x] Environment-based secret key
- [x] Environment-based debug setting
- [x] Environment-based allowed hosts
- [x] CSRF trusted origins
- [x] Secure-cookie configuration
- [x] HTTPS redirect configuration
- [x] Proxy SSL header configuration
- [x] HSTS configuration structure
- [x] Frame protection
- [x] Referrer policy
- [ ] Configure production environment variables
- [ ] Confirm HTTPS before enabling HSTS
- [ ] Run final production deployment check

## Performance

- [x] Self-hosted fonts
- [x] Responsive optimisation
- [x] Accessibility improvements
- [x] Deferred JavaScript
- [x] Optimised database queries
- [x] `select_related` and `prefetch_related`
- [x] Static-file compression configuration
- [ ] Image-size optimisation
- [ ] Lighthouse audit
- [ ] Production performance testing

## Animation and Interaction

- [x] Scroll reveal
- [x] Hover interactions
- [x] Page transitions
- [x] Accessible mobile menu
- [x] Accessible accordion behaviour
- [x] Testimonial carousel controls
- [x] Reduced-motion handling

---

# 🚧 Phase 11 – Journal

- [x] Journal model
- [x] Django Admin integration
- [x] Journal homepage
- [x] Article detail template
- [x] Published-post filtering
- [x] Cover images
- [x] Excerpts
- [x] Related properties
- [x] More-articles section
- [x] Rich text with CKEditor 5
- [x] CKEditor image-upload URL
- [x] Migration from CKEditor 4
- [x] Journal sitemap
- [x] SEO structure
- [x] Pagination
- [ ] Categories
- [ ] Add initial Journal content
- [ ] Test rich-text image uploads
- [ ] Final article typography review

---

# 🚀 Phase 12 – Deployment

## Heroku

- [ ] Create Heroku application
- [ ] Add production PostgreSQL
- [ ] Configure environment variables
- [ ] Configure build process
- [ ] Add Gunicorn
- [ ] Add Procfile
- [ ] Run migrations
- [ ] Run `collectstatic`
- [ ] Create production superuser
- [ ] Configure custom domain
- [ ] Configure `www` domain
- [ ] Enable HTTPS
- [ ] Verify production security settings
- [ ] Test production logs

## Cloudinary

- [x] Application configuration
- [ ] Add production credentials
- [ ] Verify production image uploads
- [ ] Verify existing property images
- [ ] Verify Journal image uploads

## MailerSend

- [ ] Verify sending domain
- [ ] Configure DNS records
- [ ] Add production API credentials
- [ ] Email integration
- [ ] Contact-form emails
- [ ] Test successful delivery
- [ ] Test error handling

## Launch

- [ ] Final content review
- [ ] Final QA
- [ ] Test all navigation links
- [ ] Test filtering and sorting
- [ ] Test forms
- [ ] Test Journal publishing
- [ ] Test custom error pages
- [ ] Mobile testing
- [ ] Tablet testing
- [ ] Browser testing
- [ ] Accessibility review
- [ ] Lighthouse review
- [ ] Submit sitemap
- [ ] Connect Google Search Console
- [ ] Connect Bing Webmaster Tools
- [ ] Enable initial HSTS period
- [ ] Launch