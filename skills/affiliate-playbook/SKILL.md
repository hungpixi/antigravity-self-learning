---
name: affiliate-master-playbook
description: The ultimate, unified playbook for all Affiliate Marketing tasks. Automatically triggers when the user asks anything about affiliate marketing, writing affiliate blogs, tracking conversions, A/B testing, email sequences, landing pages, SEO, social media content (TikTok, Reels, Threads, Reddit), or discovering niches.
---

# Affiliate Marketing Master Playbook

This master skill contains strategies, templates, and workflows for all Affiliate Marketing operations. 
By using this master playbook, we keep the global token budget low while maintaining 100% of capabilities via dynamic file loading.

> [!IMPORTANT]
> To perform specific affiliate tasks, you **MUST** read the corresponding module file using `view_file`.
> All modules are located in the `C:\Users\ppnh1\.gemini\antigravity\skills\affiliate-playbook\modules\` directory.

## 📚 Menu of Available Modules

### 1. Content & Copywriting (Writing Content)
- `aff-affiliate-blog-builder/SKILL.md`: Write SEO-optimized affiliate blog articles, reviews.
- `aff-comparison-post-writer/SKILL.md`: Write "X vs Y" comparison blog posts.
- `aff-how-to-tutorial-writer/SKILL.md`: Write how-to guides and tutorials.
- `aff-listicle-generator/SKILL.md`: Write "Top N best..." listicle articles.
- `aff-paid-ad-copy-writer/SKILL.md`: Write paid ad copy (Facebook, Google, TikTok).
- `aff-reddit-post-writer/SKILL.md`: Write natural, value-driven Reddit posts/comments.
- `aff-tiktok-script-writer/SKILL.md`: Write short-form video scripts (TikTok, IG Reels, YT Shorts).
- `aff-twitter-thread-writer/SKILL.md`: Write viral Twitter/X threads.
- `aff-viral-post-writer/SKILL.md`: Write viral social media posts.

### 2. Strategy, Research & Management
- `aff-affiliate-program-search/SKILL.md`: Research and evaluate affiliate programs.
- `aff-competitor-spy/SKILL.md`: Reverse-engineer successful competitor strategies.
- `aff-funnel-planner/SKILL.md`: Plan a full-scale affiliate funnel.
- `aff-multi-program-manager/SKILL.md`: Manage and compare multiple programs simultaneously.
- `aff-niche-opportunity-finder/SKILL.md`: Find untapped affiliate niches to enter.
- `aff-skill-finder/SKILL.md`: Detailed tool index for finding niche capabilities.

### 3. Funnels, Web & Landing Pages
- `aff-bio-link-deployer/SKILL.md`: Create Linktree-style bio links.
- `aff-github-pages-deployer/SKILL.md`: Deploy affiliate static sites via GitHub Pages.
- `aff-landing-page-creator/SKILL.md`: Build high-converting affiliate landing pages.
- `aff-product-showcase-page/SKILL.md`: Build single-product showcase layouts.
- `aff-squeeze-page-builder/SKILL.md`: Build email capture / squeeze pages.
- `aff-webinar-registration-page/SKILL.md`: Build webinar registration flows.

### 4. Email Marketing & Automations
- `aff-email-automation-builder/SKILL.md`: Architecture multi-sequence email automation flows.
- `aff-email-drip-sequence/SKILL.md`: Write email drip sequences for prospects.

### 5. Analytics, SEO & Operations
- `aff-ab-test-generator/SKILL.md`: Generate A/B test variants.
- `aff-commission-calculator/SKILL.md`: Calculate affiliate earnings projections and ROI.
- `aff-compliance-checker/SKILL.md`: Check content for FTC & Legal compliance.
- `aff-content-repurposer/SKILL.md`: Repurpose core content into multiple formats.
- `aff-conversion-tracker/SKILL.md`: Set up UTMs and conversion tracking methodologies.
- `aff-performance-report/SKILL.md`: Generate affiliate performance analytical reports.
- `aff-self-improver/SKILL.md`: Review results and automatically improve the strategy.
- `aff-seo-audit/SKILL.md`: Audit posts/pages for SEO opportunities.
- `aff-social-media-scheduler/SKILL.md`: Create 30-day social media launch calendars.
- `aff-shared-references/SKILL.md`: Shared configuration and global variables for affiliate tools.

## How to use:
If the user's request requires writing a TikTok script, you will run:
`view_file("C:\Users\ppnh1\.gemini\antigravity\skills\affiliate-playbook\modules\aff-tiktok-script-writer\SKILL.md")`
Then, follow the instructions located within that module.
