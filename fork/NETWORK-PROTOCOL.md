# Network Protocol: The AI for Main Street Collective

How the distributed SEO hivemind works.

---

## The Idea

Every town that creates an "AI for [Town]" site is an independent node.
Each node is valuable on its own -- it serves local business owners with
honest AI education. But connected, the nodes become a network that
outranks every AI hype site on the internet.

Here's why: Google rewards topical authority, backlink diversity, and
content quality. A network of 50 sites, each with 10+ pages of genuine
local content, all cross-linked and all focused on "AI for small business,"
creates a topical cluster that no single site can match.

One site is a blog. Fifty sites is a movement. Google notices movements.

---

## How It Works

### 1. Each Node is Independent

You own your site. You own your domain. You own your content.
Nobody can take it away from you. The network is opt-in.

### 2. Cross-Linking

Every node links to:
- The mothership (aiforlancaster.com) for universal content
- At least 3 other nodes in the network
- The network directory page

The mothership links back to every node from the /network/ directory.

This creates a web of relevant, high-quality backlinks. Not link spam --
genuine cross-references between sites that cover the same topic for
different audiences.

### 3. Monthly Traffic Reports

Each node submits a simple monthly report. Format:

```yaml
# Monthly Report: AI for [Town]
month: 2025-07
domain: aifor[town].com
total_sessions: 342
top_pages:
  - url: /guides/what-is-ai-small-business/
    sessions: 89
    avg_time: 3:42
  - url: /guides/ai-voice-agents/
    sessions: 67
    avg_time: 2:58
  - url: /book/chapter-1/
    sessions: 45
    avg_time: 4:11
top_search_terms:
  - term: "ai for small business [town]"
    impressions: 230
    clicks: 34
  - term: "ai voice agent [town]"
    impressions: 120
    clicks: 18
new_backlinks: 2
email_signups: 14
notes: "Chapter on voice agents driving most traffic. Local restaurant
  owner shared the link on Facebook -- 40 sessions in one day."
```

Submit by opening a PR to the mothership repo under /network/reports/[town]/

### 4. Collective Intelligence

Every month, we aggregate all reports and publish:
- Which pillar content pages drive the most traffic across all nodes
- Which search terms are working (and which aren't)
- Which local strategies are converting (Facebook shares? Chamber events?)
- Content gaps: what are people searching for that we don't have?
- Keyword opportunities: terms with high impressions but low clicks

This goes to /data/ on the mothership, visible to everyone.

### 5. Collective Keyword Research

The network shares keyword data openly:
- Google Search Console data (anonymized to page-level, no personal info)
- What terms each node ranks for
- Where the gaps are

When we discover a high-value keyword cluster that nobody's targeting,
we can coordinate: multiple nodes create content around it simultaneously.
A coordinated content push across 20+ domains targeting the same keyword
cluster is extremely effective and completely white-hat (because each
piece is genuinely localized and independently valuable).

---

## Privacy Rules

What we share:
- Page-level traffic numbers (which URLs get visits)
- Search terms and rankings (what people search for)
- Aggregate engagement metrics (time on page, bounce rate)
- Backlink counts and sources
- Email signup counts

What we NEVER share:
- Individual visitor data
- Email addresses or personal information
- Revenue or financial data (unless you choose to)
- Anything that identifies a specific person

---

## How to Join

### Requirements:
1. A live site with at least the book content and 3 pillar guides
2. Real local content (not just find-and-replace on Lancaster)
3. A commitment to monthly traffic reports
4. Cross-links to at least 3 other network nodes

### Process:
1. Fork the repo and build your site
2. Deploy it to your domain
3. Open a PR to the mothership adding your town to /network/directory.yaml:
   ```yaml
   - town: Topeka
     state: Kansas
     domain: aifortopeka.com
     author: Jane Smith
     joined: 2025-08-15
     status: active
   ```
4. We review (is the content real? is it localized? is it live?) and merge
5. You get added to the network directory
6. Start submitting monthly reports

### Review criteria:
- Content must be genuinely localized (not just Lancaster with the name swapped)
- Chapter 12 must have REAL local resources (verified phone numbers, addresses)
- Site must be live and accessible
- Author must be a real person (pseudonyms OK, but a real human behind it)

---

## Governance

This is not a company. There's no board. There's no fee.

Leo Guinan maintains the mothership repo and aggregates reports.
Decisions about the network are made in the open via GitHub issues.

If the network grows past 20 nodes, we'll elect 3 coordinators to
help with reviews and report aggregation. Until then, it's just Leo
and whoever shows up.

The CC BY-SA license means nobody can lock this down. If Leo gets
hit by a bus, the network continues. Every node is independent.
The protocol is the product, not the person.

---

## The Math

Why this works, in numbers:

- 1 site with 20 pages = a blog
- 10 sites with 20 pages each = 200 pages of topical content
- 50 sites = 1,000 pages, all cross-linked, all on-topic
- Each site has unique local content (not duplicate)
- Each site has a real author with local credibility
- Each cross-link is a genuine editorial backlink

Google's algorithm rewards exactly this: a network of authoritative,
non-duplicate, topically-related content with natural backlinks.

The difference between this and a link farm: every single page is
genuinely useful to a real person in a real town. That's why it works
and why it's sustainable.

---

## Contact

Questions: leo@metaspn.com
GitHub: github.com/leoguinan/ai-for-lancaster
Mothership: aiforlancaster.com
