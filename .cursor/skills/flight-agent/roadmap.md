# 🗽 East Coast Spring Break: Travel Agent Roadmap
**Goal:** Track flights/hotels for a 6-day family trip from **SAN** to DC & NYC (April 2026).
**Constraints:** Nonstop only, no red-eyes, daily price drop alerts.

---

## 🏗️ Phase 1: Environment & API Foundation
- [ ] Initialize Python environment and project structure.
- [ ] Install `amadeus-python`, `pandas`, `python-dotenv`, and `requests`.
- [ ] Create `.env` for Amadeus API Key and Secret.
- [ ] Setup `config.json` with Origin: **SAN** and Destinations: **DCA, IAD, JFK, LGA, EWR**.

## ✈️ Phase 2: Flexible Multi-City Search Engine
- [ ] Fetch flight offers for April 1 - April 10, 2026 window.
- [ ] **Flexible Routing:** Search both `SAN -> DC / NYC -> SAN` AND `SAN -> NYC / DC -> SAN` to find the best value.
- [ ] **Filter: No Red-Eye.** Exclude flights departing SAN before 7:00 AM or arriving East Coast after 10:00 PM.
- [ ] **Filter: Nonstop.** Enforce `nonStop=true` for all long-haul segments.

## 💾 Phase 3: Memory & Comparison
- [ ] Initialize SQLite database `travel_tracker.db`.
- [ ] Write logic to compare current multi-city total against the daily "best total".
- [ ] Add hotel price tracking for family-friendly stays in both DC and NYC.

## 📧 Phase 4: Automation & Notification
- [ ] Setup `smtplib` for daily email reports.
- [ ] **Alert Logic:** Notify only if the total trip price drops > $10.
- [ ] Configure **GitHub Actions** for 8:00 AM daily execution.

## 🗓️ Phase 5: Final Itinerary
- [ ] Suggest the optimal 6-day split based on the cheapest flight direction.
- [ ] Add Spring Break events: Check Cherry Blossom peak dates for the report.