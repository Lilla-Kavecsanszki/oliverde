# Oliverde Website Roadmap

---

# ✅ Phase 1 – Project Setup

- [x] Django project setup
- [x] PostgreSQL
- [x] Private GitHub repository
- [x] Project structure
- [x] Models
- [x] Django Admin
- [x] Database migrations
- [x] Custom user model
- [x] Role-based user types
- [x] Production dependency configuration

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
- [x] Organised and consistently formatted CSS

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
- [x] Privacy-safe editorial property titles
- [x] UUID-based public property URLs
- [x] Canonical redirects for changed property slugs

---

# ✅ Phase 5 – Destination Pages

- [x] Destination hero
- [x] Destination introduction
- [x] Property listings
- [x] Internal navigation
- [x] Published-property filtering
- [x] Destination testimonial support
- [x] Privacy notice for editorial property names

---

# ✅ Phase 6 – Property Pages ⭐

- [x] Property hero
- [x] Cover image
- [x] Continuous editorial gallery
- [x] Internal image categories and ordering
- [x] Full-screen image lightbox
- [x] Previous and next image navigation
- [x] Keyboard gallery navigation
- [x] Gallery captions and image counter
- [x] Property gallery JavaScript
- [x] Description
- [x] Property facts
- [x] Property amenities
- [x] Air-conditioning details
- [x] Swimming-pool details
- [x] Rental availability information
- [x] Services
- [x] Related properties
- [x] Contact enquiry link
- [x] Published-property protection
- [x] Property structured data
- [x] Privacy-safe public identity controls

---

# ✅ Phase 7 – Services

- [x] Services overview
- [x] Individual service pages
- [x] Service features
- [x] Ordered service image galleries
- [x] Editorial service-gallery layout
- [x] Shared full-screen lightbox behaviour
- [x] Related properties
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
- [x] Success and error message styling
- [x] Privacy Policy notice
- [ ] MailerSend integration
- [ ] Production email testing
- [ ] Test failed-delivery handling
- [ ] Confirm final enquiry recipient addresses

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
- [x] Admin excluded from robots.txt
- [x] Canonical URLs
- [x] Structured Data (JSON-LD)
- [x] Metadata
- [x] Open Graph structure
- [x] Default Open Graph image
- [ ] Property-specific social-sharing images
- [ ] Service-specific social-sharing images
- [ ] Destination-specific social-sharing images
- [ ] Google Search Console
- [ ] Bing Webmaster Tools
- [ ] Submit production sitemap after custom-domain setup

## Legal

- [x] Privacy Policy
- [x] Cookie Policy
- [x] Legal Notice
- [ ] Final legal-content review
- [ ] Confirm legal business name and Partita IVA
- [ ] Confirm registered/business address
- [ ] Confirm data-controller wording
- [ ] Confirm data-retention periods
- [ ] Confirm Heroku and Cloudinary disclosures
- [ ] Review cookie requirements before adding analytics

## Error Pages

- [x] Custom 404 page
- [x] Custom 404 handler
- [x] Custom 500 page
- [x] Production 500-page test
- [ ] Production 404-page test
- [ ] Confirm error logging for unexpected production exceptions

## Static Files and Media

- [x] Static files structure
- [x] Static root configuration
- [x] Cloudinary media storage configuration
- [x] WhiteNoise middleware
- [x] Compressed manifest static-file storage
- [x] Favicon package
- [x] Default Open Graph image
- [x] Final production `collectstatic`
- [x] Static manifest tested in production
- [ ] Verify Cloudinary uploads in production
- [ ] Verify large gallery-image uploads
- [ ] Confirm image deletion and replacement behaviour

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
- [x] Production environment variables
- [x] Production database credentials managed by Heroku
- [x] Final production deployment check
- [x] Private GitHub repository
- [x] `.env` excluded from Git
- [x] `.env.example` included safely
- [ ] Confirm custom-domain HTTPS before enabling HSTS
- [ ] Enable an initial HSTS period
- [ ] Increase HSTS duration after verification
- [ ] Review production admin permissions

## Performance

- [x] Self-hosted fonts
- [x] Responsive optimisation
- [x] Accessibility improvements
- [x] Deferred JavaScript
- [x] Optimised database queries
- [x] `select_related` and `prefetch_related`
- [x] Static-file compression
- [x] Manifest-based static-file caching
- [ ] Image-size optimisation
- [ ] Cloudinary image transformations
- [ ] Hero-image preloading review
- [ ] Lighthouse audit
- [ ] Production performance testing
- [ ] Core Web Vitals review

## Animation and Interaction

- [x] Scroll reveal
- [x] Hover interactions
- [x] Page transitions
- [x] Accessible mobile menu
- [x] Accessible accordion behaviour
- [x] Testimonial carousel controls
- [x] Property-gallery lightbox controls
- [x] Service-gallery lightbox controls
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
- [ ] Test rich-text image uploads in production
- [ ] Final article typography review
- [ ] Review article image sizing
- [ ] Add initial destination and property-management articles

---

# 🚧 Phase 12 – Deployment

## Heroku

- [x] Create Heroku application
- [x] Configure EU region
- [x] Configure Heroku-26 stack
- [x] Add production PostgreSQL
- [x] Configure `DATABASE_URL`
- [x] Configure production environment variables
- [x] Configure build process
- [x] Add Gunicorn
- [x] Add Procfile
- [x] Add release-phase migrations
- [x] Configure `.python-version`
- [x] Run production migrations
- [x] Run production `collectstatic`
- [x] Connect private GitHub repository
- [x] Complete first production deployment
- [x] Confirm web dyno is running
- [x] Test production logs
- [x] Resolve first production static-manifest error
- [x] Confirm live Heroku application
- [ ] Create production superuser
- [ ] Verify production admin login
- [ ] Configure custom domain
- [ ] Configure `www` domain
- [ ] Configure custom-domain DNS
- [ ] Enable Automated Certificate Management
- [ ] Verify custom-domain HTTPS
- [ ] Update `SITE_URL` to the custom domain
- [ ] Update `ALLOWED_HOSTS` after domain setup
- [ ] Update `CSRF_TRUSTED_ORIGINS` after domain setup
- [ ] Verify final production security settings

## Cloudinary

- [x] Application configuration
- [x] Add production credentials
- [ ] Verify production property-image uploads
- [ ] Verify production service-image uploads
- [ ] Verify existing property images
- [ ] Verify Journal image uploads
- [ ] Test image replacement
- [ ] Test image deletion

## MailerSend

- [ ] Verify sending domain
- [ ] Configure DNS records
- [ ] Add production API credentials
- [ ] Email integration
- [ ] Contact-form emails
- [ ] Test successful delivery
- [ ] Test failed-delivery handling
- [ ] Confirm production sender and reply-to addresses

## Production Content

- [ ] Add destinations
- [ ] Add five core services
- [ ] Add property amenities
- [ ] Add initial properties
- [ ] Add testimonials
- [ ] Add service gallery images
- [ ] Add property gallery images
- [ ] Add initial Journal articles
- [ ] Review all public titles and privacy-safe slugs
- [ ] Confirm owner approval for publicly displayed properties

## Launch

- [ ] Final content review
- [ ] Final legal review
- [ ] Final QA
- [ ] Test all navigation links
- [ ] Test destination pages
- [ ] Test filtering and sorting
- [ ] Test property galleries
- [ ] Test service galleries
- [ ] Test contact form
- [ ] Test Journal publishing
- [ ] Test production 404 page
- [x] Test production 500 page
- [ ] Mobile testing
- [ ] Tablet testing
- [ ] Safari testing
- [ ] Chrome testing
- [ ] Firefox testing
- [ ] Accessibility review
- [ ] Lighthouse review
- [ ] Connect custom domain
- [ ] Enable custom-domain SSL
- [ ] Submit sitemap
- [ ] Connect Google Search Console
- [ ] Connect Bing Webmaster Tools
- [ ] Enable initial HSTS period
- [ ] Confirm backups and recovery process
- [ ] Official launch

---

# 🚧 Phase 13 – Testing and Maintenance

## Automated Tests

- [ ] Add model tests
- [ ] Add URL tests
- [ ] Add public-view tests
- [ ] Add unpublished-property protection tests
- [ ] Add UUID property URL tests
- [ ] Add contact-form validation tests
- [ ] Add sitemap tests
- [ ] Add robots.txt test
- [ ] Add custom error-page tests
- [ ] Add admin configuration tests where appropriate

## Database and Backups

- [ ] Confirm Heroku Postgres backup schedule
- [ ] Test a manual database backup
- [ ] Document database-restore procedure
- [ ] Document production-content recovery procedure

## Monitoring

- [ ] Add production error monitoring
- [ ] Review Heroku logs after launch
- [ ] Monitor failed contact-form deliveries
- [ ] Monitor Cloudinary usage
- [ ] Monitor Heroku Postgres usage
- [ ] Monitor Eco dyno-hour allowance

## Documentation

- [ ] Update README deployment instructions
- [ ] Document production environment variables
- [ ] Document content-entry workflow
- [ ] Document property privacy rules
- [ ] Document backup and restore process
- [ ] Document custom-domain configuration