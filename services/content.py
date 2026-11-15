"""
Extra editorial content for the public service pages.

This text lives in code, not the database, so changing it needs no
migration: edit the wording below, commit and deploy.

Each entry is keyed by the service's slug. A service without an entry
simply shows the existing page without the extra sections.

All copy is written in British English.
"""

# Which "This enquiry is about" option the contact form should preselect
# when someone arrives from a service page. Values must match
# core.models.ContactEnquiry.EnquiryType.
ENQUIRY_TYPES = {
    "post-purchase-set-up": "post_purchase",
    "property-maintenance": "management",
    "restoration-management": "restoration",
    "property-administration": "management",
    "property-rental": "management",
}


# Questions that apply to every service.
COMMON_FAQS = [
    {
        "question": "Do I have to take everything you offer?",
        "answer": (
            "No. Every plan is tailored to your home and to how you use "
            "it. We arrange only the services you ask for, and you can add "
            "more whenever you wish."
        ),
    },
    {
        "question": "Do I need to be in Italy while you look after my home?",
        "answer": (
            "No. Many of our owners live abroad. We act on your behalf "
            "locally and keep you informed with regular updates, so you can "
            "be as involved as you wish."
        ),
    },
    {
        "question": "Which areas do you cover?",
        "answer": (
            "We look after homes across Tuscany, Umbria and Lazio."
        ),
    },
    {
        "question": "Who will I deal with?",
        "answer": (
            "You will have a single point of contact at Oliverde, who "
            "coordinates the specialists and local teams on your behalf."
        ),
    },
    {
        "question": "How do we get started?",
        "answer": (
            "Schedule a consultation through our contact page. Tell us about "
            "your property and what you need, and we will take it from there."
        ),
    },
]


SERVICE_CONTENT = {

    # ------------------------------------------------------------------
    "post-purchase-set-up": {
        "overview": [
            "Buying a home in Italy is the beginning of a long list of "
            "practical tasks, many of them in a language and an "
            "administrative system you may not know. We take you through "
            "the first weeks and months, arranging whatever you would like "
            "help with, so that the house is registered, connected, "
            "staffed and secure, and ready for you to enjoy.",

            "Our team works alongside the local council and utility "
            "providers, and can suggest and introduce an Italian "
            "accountant and other trusted specialists wherever you need "
            "them, so you deal with one point of contact rather than "
            "many.",
        ],
        "who_for": (
            "New owners, and anyone who has bought in Italy from abroad."
        ),
        "steps": [
            {
                "title": "Review your purchase",
                "text": (
                    "We go through what you have bought and which tasks you "
                    "would like help with, so that we arrange what you "
                    "need and nothing is missed."
                ),
            },
            {
                "title": "Registrations and tax",
                "text": (
                    "Council (IMU) and waste (TARI) registrations are "
                    "arranged, and we can suggest and introduce an "
                    "Italian accountant for your annual filing."
                ),
            },
            {
                "title": "Bank, utilities and security",
                "text": (
                    "We help you open an Italian bank account and set up "
                    "your gas, electricity, water and internet, and can "
                    "arrange security and surveillance if you would like "
                    "it."
                ),
            },
            {
                "title": "Your team in place",
                "text": (
                    "If you wish, we introduce trusted housekeeping and "
                    "grounds staff, so the house is looked after from the "
                    "first day."
                ),
            },
        ],
        "articles": [],
    },

    # ------------------------------------------------------------------
    "property-maintenance": {
        "overview": [
            "An Italian country house is not a home you can leave alone "
            "for months. Regular care stops small issues from becoming "
            "expensive ones, and keeps the house, garden and pool looking "
            "just as you left them.",

            "Together we agree what the house needs, and then we organise "
            "regular inspections, coordinate the people who look after "
            "the house, grounds and swimming pool, and send you "
            "photographic updates, so you always know how things stand.",
        ],
        "who_for": (
            "Owners who spend part of the year away, or who would simply "
            "rather not manage the upkeep themselves."
        ),
        "steps": [
            {
                "title": "A plan for your property",
                "text": (
                    "We agree what the house, gardens and pool need "
                    "through the seasons."
                ),
            },
            {
                "title": "Regular inspections",
                "text": (
                    "We visit the property at a frequency agreed with you "
                    "and check security, utilities, housekeeping and the "
                    "grounds."
                ),
            },
            {
                "title": "Specialists when needed",
                "text": (
                    "We coordinate local tradespeople and contractors for "
                    "repairs and seasonal work."
                ),
            },
            {
                "title": "Updates you can rely on",
                "text": (
                    "You receive photographic updates and have a single "
                    "point of contact for anything you need."
                ),
            },
        ],
        # Journal slugs. Only articles that exist and are published are shown.
        "articles": [
            "preparing-tuscan-home-for-winter",
            "care-tuscan-home-garden-summer",
            "caring-for-umbrian-stone-farmhouse",
        ],
    },

    # ------------------------------------------------------------------
    "restoration-management": {
        "overview": [
            "Restoring or renovating a property in Italy involves "
            "architects, builders, craftspeople and permissions, often "
            "while you are in another country. We oversee the project on "
            "your behalf, so that the work is carried out to plan and to a "
            "high standard, and respects the character of the building.",

            "We act as your representative on site, coordinating the "
            "specialists involved and keeping you informed at every stage.",
        ],
        "who_for": (
            "Owners planning a restoration or renovation who want a "
            "trusted person overseeing the work on the ground."
        ),
        "steps": [
            {
                "title": "Understand the project",
                "text": (
                    "We review your plans, priorities and budget, and "
                    "what the building needs."
                ),
            },
            {
                "title": "Assemble the team",
                "text": (
                    "We coordinate trusted architects, builders and "
                    "craftspeople for the work."
                ),
            },
            {
                "title": "Oversee the works",
                "text": (
                    "We visit regularly, check progress against the plan "
                    "and keep you informed with updates and photographs."
                ),
            },
            {
                "title": "Hand over and look after",
                "text": (
                    "When the work is complete, we check the finished "
                    "result and move the house into regular care."
                ),
            },
        ],
        "articles": [],
    },

    # ------------------------------------------------------------------
    "property-administration": {
        "overview": [
            "Owning a home in Italy brings a steady stream of paperwork: "
            "taxes, utility bills, insurance, local registrations and "
            "correspondence. We take care of it for you, so nothing is "
            "overlooked and nothing arrives unexpectedly.",

            "Our in-house team provides consistent administrative support, "
            "working with your accountant and local providers where "
            "needed.",
        ],
        "who_for": (
            "Owners who live abroad or have limited time, and would rather "
            "not manage the paperwork themselves."
        ),
        "steps": [
            {
                "title": "We take stock",
                "text": (
                    "We gather the documents, accounts and deadlines "
                    "that relate to your property."
                ),
            },
            {
                "title": "Bills, taxes and renewals",
                "text": (
                    "We keep track of utility bills, local taxes and "
                    "renewals, so that nothing is missed."
                ),
            },
            {
                "title": "Correspondence handled",
                "text": (
                    "We deal with letters, providers and professionals "
                    "on your behalf."
                ),
            },
            {
                "title": "Clear communication",
                "text": (
                    "You hear from us when something needs your decision, "
                    "and can otherwise leave the details with us."
                ),
            },
        ],
        "articles": [],
    },

    # ------------------------------------------------------------------
    "property-rental": {
        "overview": [
            "Letting your home can help towards its running costs, but it "
            "brings work of its own: welcoming guests, preparing the house "
            "and dealing with anything that goes wrong. We look after the "
            "guest experience, so that your home is cared for and your "
            "guests are welcomed properly.",

            "Rentals are planned around your own use of the house, so "
            "your time there always comes first.",
        ],
        "who_for": (
            "Owners who would like to let their home to guests without "
            "managing the arrivals, the housekeeping or the day-to-day "
            "details themselves."
        ),
        "steps": [
            {
                "title": "Agree how you want to let",
                "text": (
                    "We discuss when the house is available, who it is "
                    "for and the standard you expect."
                ),
            },
            {
                "title": "Prepare the house",
                "text": (
                    "The house is cleaned, prepared and checked before "
                    "every arrival."
                ),
            },
            {
                "title": "Look after your guests",
                "text": (
                    "We welcome guests and are on hand to help during "
                    "their stay."
                ),
            },
            {
                "title": "Check and reset",
                "text": (
                    "After each departure, everything is checked and "
                    "returned to its usual routine, and you are kept "
                    "informed."
                ),
            },
        ],
        "articles": [],
    },
}