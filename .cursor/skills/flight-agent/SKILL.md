---
name: flight-agent
description: This is a new rule
---

# Overview

# Project Tech Stack
- Use **Next.js 15 (App Router)** and **Tailwind CSS**.
- Use **Lucide-React** for all icons.
- Prefer **Functional Components** and **Arrow Functions**.
- Always use **TypeScript** with strict type checking.

# Development Rules
- When adding new files, place components in `/components` and logic in `/lib`.
- Follow a mobile-first responsive design approach.
- Ensure all interactive elements have proper hover and focus states.

# Project Context
Building a Travel Agent for a family trip from San Diego (SAN) to the East Coast (DC and NYC) in April 2026.

# Coding Standards
- Use Python for all backend logic.
- **Flexible Routing:** Logic must evaluate two itinerary paths:
    1. Inbound: SAN -> DC | Outbound: NYC -> SAN.
    2. Inbound: SAN -> NYC | Outbound: DC -> SAN.
- Ensure all flight search functions strictly filter for **nonStop=true**.
- **No Red-Eye Rule:** Filter out any flight departing SAN before 07:00 or arriving after 22:00.
- Use SQLite to persist price history and avoid duplicate alerts.

# Tone & Style
- Be concise.
- Focus on functional, modular code.