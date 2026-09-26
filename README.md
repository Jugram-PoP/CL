# CyberLearn

A Django-based cybersecurity awareness platform built for Ghanaian university students. CyberLearn teaches core security concepts — password hygiene, phishing awareness, safe browsing, and social engineering — through short, interactive, section-by-section lessons, an in-app phishing simulation, and a live password-strength tool, with progress tracked per user.

This project began as a 3-week internship build and grew significantly beyond its original scope during development — most notably the lesson experience, which evolved from single static pages into a fully interactive, section-based format with inline quizzes, reflection prompts, and a custom password-strength simulator.

---

## Features

### Accounts
- Custom email-based user model (sign up, log in, log out)
- Project-wide login requirement (`LoginRequiredMiddleware`) — every page except the login/signup flow requires authentication by default

### Lessons
- Four core lessons: Password Hygiene, Phishing Awareness, Safe Browsing, Social Engineering
- Lesson content is split automatically into short, single-screen pages by heading (`<h2>`/`<h3>`), with a sidebar table of contents that visually distinguishes top-level sections from subsections
- Inline multiple-choice "quick check" questions appear directly within the relevant section, graded instantly via AJAX, with answers locked in permanently once submitted
- Open-ended reflection questions appear as their own dedicated page, with a "type your own answer, then reveal the model answer" format (ungraded by design)
- A custom `<!--pagebreak-->` marker lets specific content (like the password simulator) force its own page regardless of word count
- A live, client-side **password strength simulator** embedded in the Password Hygiene lesson, checking:
  - Minimum length
  - Character-type variety
  - Exact matches against a common-password list (including generated name+number combinations, e.g. `kofi123`)
  - Dictionary-word and recognizable-name detection (with leetspeak normalization, e.g. `p@ssw0rd`)
  - Keyboard-walk and sequential-character patterns (`qwerty`, `123456789`)
  - Repeated-character runs
  - A rough, entirely client-side crack-time estimate
  - A weighted verdict where certain properties (known password, digits-only, sequential pattern, under minimum length) override the score entirely rather than being one vote among many

### Phishing Simulation
- Four fixed mock phishing/safe scenarios rendered as email previews
- User marks each as "safe" or "phishing" and receives immediate feedback plus structured red-flags/safety-reasons explanations (stored as JSON)

### Progress Tracking
- Per-user dashboard showing lesson completion and quiz accuracy per lesson

### Admin
- Custom `list_display`, `search_fields`, and `list_filter` configured for Lessons, Questions, Completions, and Scenarios
- Inline editing of Questions/Choices within their parent Lesson/Question in the admin

### Automated Tests
- `accounts/tests.py` covers signup, successful login, failed login, and anonymous-user access control

---

## Tech Stack
- **Backend:** Python, Django, SQLite
- **Frontend:** Django Template Language (server-rendered), hand-written CSS (no framework), vanilla JavaScript for interactive widgets
- **Fonts:** Fraunces (headings), Plus Jakarta Sans (body)

---

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to sign up, or `/admin/` to manage content.

---

## Known Shortcomings

This project has real, intentional limitations — noted here rather than hidden, since being upfront about scope tradeoffs is more useful than pretending they don't exist.

- **Password dictionary is small and hand-curated.** The word/name lists used by the password simulator are a few hundred entries, not a real breach database. A production-grade tool would use something like the [Have I Been Pwned API](https://haveibeenpwned.com/API/v3) (via k-anonymity hashing, so no real password is ever transmitted) rather than a static client-side list.
- **Rule-based password checking has inherent blind spots.** No fixed set of pattern checks can catch every weak password or avoid ever flagging an unusual-but-strong one. This is a limitation of rule-based checkers generally, not specific to this implementation.
- **Open-ended reflection questions are ungraded by design** — there's no backend validation of free-text answers, and they don't factor into the progress dashboard at all.
- **Lesson and quiz content is managed entirely through the Django admin**, as raw HTML/JS pasted into a text field. There's no WYSIWYG editor, and a malformed paste (an unclosed tag, a script cut in half by the page-splitting logic) can silently break a page with no validation at the point of entry.
- **No automated tests beyond the auth flow.** Lessons, the quiz system, the phishing simulation, and the password simulator were verified through manual click-through testing, not automated test coverage.
- **No production deployment.** This has only been run and tested locally (`runserver`); it has not been configured for a real server, HTTPS, or a production-grade database.
- **Limited mobile/responsive testing.** The interactive lesson layout (sidebar + content) was primarily built and tested at desktop widths.
- **No real email-based phishing simulation** — scenarios are shown as in-app mock previews only, per the original project scope.
- **An AI-assisted tutor feature was considered but ultimately not implemented**, once the lesson format itself became sufficiently interactive to address the original feedback that prompted the idea.

---

## Ways It Could Be Improved

### UI / UX
- Replace the current hand-written, page-by-page CSS with a single shared design system/component library, so visual changes (colors, spacing, button styles) don't need to be repeated across every template
- A consistent, polished mobile layout — the current design assumes a reasonably wide viewport
- Richer lesson-authoring tools in the admin (a real rich-text editor, live preview) instead of raw HTML in a text field
- Visual loading/transition states between lesson section pages
- Accessibility pass: proper ARIA labeling on the password simulator and quiz widgets, keyboard-navigation testing, screen-reader testing

### Features
- Real breach-database password checking (Have I Been Pwned or similar), replacing the static wordlist
- Optional lightweight grading/feedback for open-ended questions (even simple keyword matching) so they can contribute to progress tracking
- A structured content model for lessons (rather than free-form HTML) so content can be edited safely without risking broken markup
- Expanded automated test coverage across lessons, quizzes, the phishing simulator, and progress calculations
- Deployment configuration for a real hosting environment (PostgreSQL, static file serving, HTTPS, environment-based secrets)

### Content
- More phishing scenarios and lesson topics beyond the original four
- Localization/translation support beyond the current Ghana-focused English content

---

## Project Structure

```
config/         — project settings, root URL routing
accounts/       — custom user model, signup/login/logout
learning/       — home page, progress dashboard
lessons/        — lesson content, quiz questions, open questions, password simulator
phishing_sim/   — phishing scenarios and attempts
```
