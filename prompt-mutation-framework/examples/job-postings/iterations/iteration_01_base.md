# ITERATION 1: Base Job Posting Template
## Foundation for AI-Powered Job Descriptions

**Domain**: Job postings for LinkedIn, Indeed, AngelList, Glassdoor
**Purpose**: Generate compelling, inclusive, and effective job descriptions that attract qualified candidates

---

## CORE PROMPT TEMPLATE

```
You are an expert talent acquisition specialist with deep knowledge of recruitment marketing, inclusive language, and job board optimization.

TASK: Generate a compelling job description based on provided inputs.

INPUT REQUIREMENTS:
1. job_title (e.g., "Senior Software Engineer", "Product Manager")
2. company_name and brief description
3. location (remote, hybrid, office, city)
4. employment_type (full-time, part-time, contract)
5. salary_range (if transparent)
6. required_skills (list)
7. nice_to_have_skills (list)
8. benefits (list)
9. team_size and reporting_structure
10. target_platform (LinkedIn, Indeed, etc.)

OUTPUT STRUCTURE:

1. **JOB TITLE** (60-80 characters)
   - Clear, searchable, no inflated titles
   - Format: [Level] [Role] - [Key Specialization]
   - Example: "Senior Backend Engineer - Python & Cloud Infrastructure"

2. **ATTENTION-GRABBING OPENER** (2-3 sentences, 150-200 words)
   - Lead with company mission or exciting challenge
   - Answer "Why would someone want this job?"
   - Avoid generic corporate speak

3. **ABOUT THE COMPANY** (2-3 sentences, 100-150 words)
   - What does the company do?
   - Stage (startup, scale-up, enterprise)
   - Notable achievements or customers
   - Culture snapshot

4. **THE ROLE** (3-4 sentences, 150-200 words)
   - What will the person actually do day-to-day?
   - Impact they'll have
   - Team they'll work with
   - Projects they'll own

5. **KEY RESPONSIBILITIES** (5-7 bullet points)
   - Action-oriented (start with verbs)
   - Specific, not generic
   - Mix of technical and collaborative tasks
   - Prioritized by importance

6. **REQUIRED QUALIFICATIONS** (5-7 bullet points)
   - Must-haves only
   - Avoid years of experience for skills younger than that
   - Focus on skills, not credentials
   - Inclusive language (avoid "rockstar", "ninja")

7. **NICE TO HAVE** (3-5 bullet points)
   - Optional skills that help but aren't required
   - Clearly separated from requirements

8. **BENEFITS & PERKS** (5-8 bullet points)
   - Compensation range (if transparent)
   - Health/wellness benefits
   - Professional development
   - Work-life balance offerings
   - Equity/bonuses (if applicable)

9. **APPLICATION CALL-TO-ACTION**
   - Clear next steps
   - Timeline expectations
   - What to include in application

CRITICAL RULES:
✓ Use gender-neutral language ("they/them", not "he/she")
✓ Avoid age bias ("recent grad" OR "10+ years" = contradictory)
✓ Be honest about requirements (don't call nice-to-haves required)
✓ Include salary range if legally required (EU transparency laws)
✓ Avoid jargon that excludes candidates
✓ Make responsibilities concrete, not abstract
✓ Focus on skills, not degrees (unless legally required)

INCLUSIVE LANGUAGE GUIDELINES:
❌ Avoid: rockstar, ninja, guru, recent grad, digital native
✓ Use: skilled, experienced, proficient, expert
❌ Avoid: aggressive, competitive, dominant
✓ Use: results-driven, collaborative, impactful
❌ Avoid: culture fit
✓ Use: culture add

PLATFORM OPTIMIZATION:
- **LinkedIn**: Professional tone, keyword-rich for search
- **Indeed**: Clear job title, salary transparency helps
- **AngelList**: Startup culture, equity details, fast growth
- **Glassdoor**: Honest about culture, benefits emphasis
```

---

## EXAMPLE OUTPUT

**Input:**
```json
{
  "job_title": "Senior Software Engineer",
  "company_name": "CloudTech GmbH",
  "company_description": "B2B SaaS platform for cloud infrastructure management",
  "location": "Berlin, Germany (Hybrid 2 days/week)",
  "employment_type": "Full-time",
  "salary_range": "€80,000 - €120,000",
  "required_skills": ["Python", "AWS", "PostgreSQL", "REST APIs"],
  "nice_to_have": ["Kubernetes", "Go", "React"],
  "benefits": ["equity", "30 vacation days", "learning budget €2000/year"],
  "team_size": "8 engineers",
  "target_platform": "LinkedIn"
}
```

**Generated Job Posting:**

---

**Senior Backend Engineer - Python & Cloud Infrastructure**

Are you excited about building scalable infrastructure that powers thousands of businesses? Join CloudTech as we revolutionize how companies manage their cloud resources.

**About CloudTech**

We're a fast-growing B2B SaaS company helping enterprises optimize their cloud spend and performance. Our platform manages over €100M in cloud infrastructure annually for customers like Mercedes-Benz, Zalando, and Deutsche Telekom. We're a team of 45, backed by €10M Series A funding, and growing rapidly.

**The Role**

As a Senior Backend Engineer, you'll architect and build the core systems that process millions of infrastructure events daily. You'll work closely with our 8-person engineering team to design scalable APIs, optimize database performance, and ensure 99.99% uptime for critical infrastructure. This role offers high autonomy and direct impact on product direction.

**What You'll Do**
- Design and implement scalable backend services using Python and AWS
- Build and maintain REST APIs serving 1M+ requests/day
- Optimize PostgreSQL queries and database architecture for performance
- Collaborate with frontend team on API design and integration
- Participate in on-call rotation (1 week every 2 months)
- Mentor junior engineers through code reviews and pair programming
- Contribute to technical strategy and architecture decisions

**Required Qualifications**
- Strong experience building production Python applications
- Deep knowledge of AWS services (EC2, Lambda, RDS, S3)
- Proficiency with PostgreSQL and database optimization
- Experience designing and documenting REST APIs
- Understanding of system design and scalability patterns
- Excellent communication skills in English (German not required)

**Nice to Have**
- Experience with Kubernetes and container orchestration
- Familiarity with Go or willingness to learn
- Frontend experience with React
- Previous experience at B2B SaaS companies
- Open-source contributions

**Benefits & Perks**
- Salary: €80,000 - €120,000 based on experience
- Equity: 0.1% - 0.3% stock options
- 30 vacation days per year (German standard)
- Learning budget: €2,000/year for courses, conferences, books
- Hybrid work: 2 days/week in Berlin office, 3 days remote
- Health insurance: Premium plan including dental
- Modern tech stack: Latest MacBook Pro or Linux workstation
- Regular team events and quarterly off-sites

**How to Apply**

Send your CV and a brief note about a challenging technical problem you've solved to jobs@cloudtech.de. We review applications within 5 business days and conduct interviews on a rolling basis. Our process: recruiter call (30 min) → technical interview (90 min) → system design interview (60 min) → team fit conversation (45 min).

We're committed to building a diverse team and encourage applications from candidates of all backgrounds. If you need accommodations during the interview process, please let us know.

---

## SCORING DIMENSIONS (Self-Assessment):

- **Clarity**: 82/100 - Role and responsibilities clear, some genericness remains
- **Inclusivity**: 75/100 - Avoids obvious bias but could be more proactive
- **Honesty**: 85/100 - Realistic requirements, transparent about salary and process
- **SEO**: 70/100 - Keywords present but not optimized for job board algorithms
- **Conversion**: 78/100 - Compelling but lacks emotional hooks for passive candidates
- **Compliance**: 80/100 - Meets basic EU requirements, could be stronger
- **Maintenance**: 75/100 - Some hardcoded details (team size, customers)

**Average: 77.9/100** (C+ grade - functional but needs optimization)

## IDENTIFIED LIMITATIONS:

1. **Generic Language**: Phrases like "fast-growing" and "exciting challenge" are overused
2. **Passive Voice**: Some bullets use passive constructions
3. **Length Variations**: No adaptation for platform character limits
4. **Salary Transparency**: Doesn't enforce EU transparency laws automatically
5. **Accessibility**: No mention of accommodations or inclusive hiring practices
6. **Bias Detection**: Doesn't automatically flag problematic language
7. **SEO Weakness**: Missing keyword optimization for job boards

## NEXT ITERATION OPPORTUNITIES:

- Add character-constrained variants for LinkedIn (2000 chars), Twitter (280 chars)
- Build inclusive language checker (adversarial testing)
- Create platform-specific SEO optimization
- Develop salary transparency enforcer
- Add accessibility statement generator
- Implement bias detection patterns
