# Email HTML Technical Standards

This reference provides technical standards for HTML email development, including rendering quirks, responsive design, dark mode, image optimization, and Gmail clipping rules.

---

## Email Client Market Share (2025)

| Email Client | Market Share | Engine | Key Quirks |
|--------------|--------------|--------|------------|
| Apple Mail (iOS/macOS) | 49-58% | WebKit | Dark mode aggressive, media queries supported |
| Gmail (web/app) | 26-31% | Proprietary | Strips <style>, clips >102KB, caches images |
| Outlook (Windows) | 6-8% | Microsoft Word (!) | No CSS3, table-only layouts, VML for images |
| Yahoo Mail | 3-5% | Proprietary | Inconsistent media query support |
| Outlook.com | 2-4% | Proprietary | Better than desktop Outlook |
| Other (Samsung, AOL, etc.) | 5-10% | Varies | Test individually if >2% of audience |

**Critical takeaway**: Design for Apple Mail (majority), test in Gmail (quirky), assume Outlook is broken (it is).

---

## HTML Rendering Rules

### Layout Architecture

**Use table-based layouts only.** No Grid, no Flexbox, no modern CSS positioning.

```html
<!-- CORRECT: Table-based layout -->
<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
  <tr>
    <td align="center" style="padding: 20px;">
      <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600">
        <tr>
          <td style="padding: 20px; background-color: #ffffff;">
            Email content here
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>

<!-- WRONG: Flexbox (breaks in Outlook, Gmail) -->
<div style="display: flex; justify-content: center;">
  <div style="width: 600px;">
    Email content here
  </div>
</div>
```

**Required table attributes:**
- `role="presentation"` (accessibility, tells screen readers this is layout, not data)
- `cellspacing="0"` (removes default spacing)
- `cellpadding="0"` (removes default padding)
- `border="0"` (removes default border)
- `width` attribute (not just CSS) for Outlook

### Maximum Width

| Device | Max Width | Notes |
|--------|-----------|-------|
| Desktop optimal | 600px | Fits all preview panes |
| Desktop absolute max | 640px | Gmail preview pane limit |
| Mobile | 100% | Fluid width, min 320px |

**Implementation:**
```html
<table role="presentation" width="600" style="max-width: 600px; width: 100%;">
  <!-- Outlook reads width attribute, modern clients read max-width CSS -->
</table>
```

### Inline CSS (Critical)

**All critical CSS must be inline.** Gmail strips `<style>` tags. Use `<style>` only for media queries (progressive enhancement).

```html
<!-- CORRECT: Inline styles -->
<td style="font-family: Arial, sans-serif; font-size: 16px; line-height: 24px; color: #333333;">

<!-- WRONG: External styles (Gmail strips) -->
<style>
  .body-text { font-family: Arial, sans-serif; }
</style>
<td class="body-text">
```

**Exception:** Media queries must be in `<style>` tags (Outlook ignores, Gmail on mobile reads).

### Web-Safe Fonts

Gmail and Outlook have limited font support. Use web-safe fonts or specify fallbacks.

| Font Family | Safe? | Fallback |
|-------------|-------|----------|
| Arial | ✅ | Helvetica, sans-serif |
| Helvetica | ✅ | Arial, sans-serif |
| Georgia | ✅ | Times New Roman, serif |
| Times New Roman | ✅ | Times, serif |
| Courier New | ✅ | Courier, monospace |
| Verdana | ✅ | Geneva, sans-serif |
| Trebuchet MS | ⚠️ | Arial, sans-serif (not on all systems) |
| Custom fonts (web fonts) | ❌ | Fallback to web-safe required |

**Implementation:**
```css
font-family: 'Custom Font', Arial, Helvetica, sans-serif;
```

**Custom fonts via @import or `<link>`:** Supported in Apple Mail and some modern clients. Always include web-safe fallback. Not worth the risk for most campaigns.

### Color Codes

Use 6-character hex codes: `#FF5733` (not `#F53` or `rgb()`). Set `bgcolor` attribute on `<td>` as Outlook fallback alongside `style="background-color: ...".

### Spacing and Padding

**Use padding on `<td>`, not margin on elements.** Outlook ignores margins on many elements. Always reset with `margin: 0; padding: 0;` on headings and paragraphs, then apply padding to the parent `<td>`.

---

## Responsive Design

### Mobile-First Statistics

- **70%+ of emails opened on mobile** (2025 average)
- **15-second attention span** on mobile vs 8 seconds on desktop
- **Thumb zone**: Bottom 50% of screen is easiest to reach

### Breakpoints

| Breakpoint | Width | Target Device |
|------------|-------|---------------|
| Desktop | 600-640px | Default (no media query) |
| Tablet | 480-600px | `@media (max-width: 600px)` |
| Mobile | 320-480px | `@media (max-width: 480px)` |

**Approach:** Design for desktop (600px), use media queries to adapt for mobile (single column, larger text, stacked elements).

### Media Query Classes

Use `@media only screen and (max-width: 600px)` with `!important` overrides:
- `.mobile-full-width` → `width: 100% !important; max-width: 100% !important;`
- `.mobile-padding` → `padding: 10px !important;`
- `.mobile-font-size` → `font-size: 16px !important; line-height: 24px !important;`
- `.mobile-hide` → `display: none !important;`
- `.mobile-stack` → `display: block !important; width: 100% !important;`

### Touch Targets (Critical)

**Minimum button size: 44x44px** (Apple Human Interface Guidelines). Use `<table role="presentation">` with `<td>` containing an `<a>` with `padding: 14px 28px`. Minimum 10px padding around all tappable links.

### Font Sizes

| Element | Desktop | Mobile | Notes |
|---------|---------|--------|-------|
| Body text | 14-16px | 16px | 16px prevents iOS zoom |
| Headings (H1) | 28-32px | 24-28px | Scale down on mobile |
| Headings (H2) | 22-26px | 20-24px | |
| Buttons | 16px | 16-18px | Always readable |
| Fine print | 12px | 14px | Legal, footer |

**Mobile font rule:** Minimum 14px for any text, 16px for body (prevents auto-zoom on iOS).

### Single-Column Stacking

Desktop two-column layouts must stack on mobile. Use `class="mobile-stack"` on `<td>` elements and `@media (max-width: 600px) { .mobile-stack { display: block !important; width: 100% !important; } }` to make columns stack vertically.

---

## Dark Mode Compatibility

### Prevalence

- **Apple Mail**: Automatic dark mode on iOS 13+ and macOS Mojave+
- **Gmail**: Supports dark mode on Android/iOS
- **Outlook**: Partial support (converts colors unpredictably)

**Estimated usage:** 30-40% of emails opened in dark mode (2025).

### Three Approaches

#### 1. Media Query Approach (Best)

```html
<style>
  @media (prefers-color-scheme: dark) {
    body {
      background-color: #000000 !important;
      color: #FFFFFF !important;
    }
    .dark-bg {
      background-color: #1C1C1C !important;
    }
    .dark-text {
      color: #E0E0E0 !important;
    }
  }
</style>
```

**Support:** Apple Mail, Gmail (iOS/Android), some web clients.

#### 2. Data Attributes (Outlook-Specific)

```html
<div style="background-color: #FFFFFF;" data-ogsc="#1C1C1C" data-ogsb="#FFFFFF">
  <!-- Outlook uses data-ogsc (original background) for dark mode -->
</div>
```

**Attributes:**
- `data-ogsc`: Original background color (dark mode uses this)
- `data-ogsb`: Original text color

#### 3. Meta Tag (Gmail)

```html
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
```

**Effect:** Tells Gmail to adapt UI chrome (not content) to dark mode.

### Design Rules for Dark Mode

| Rule | Why |
|------|-----|
| Avoid pure white backgrounds (`#FFFFFF`) | Becomes blinding in dark mode; use `#FAFAFA` or `#F5F5F5` |
| Avoid pure black text (`#000000`) | Reduced contrast in dark mode; use `#333333` |
| Add borders to images | White-background PNGs disappear in dark mode |
| Test logos | White logos disappear; provide dark-mode variant |
| Use transparent PNGs cautiously | May blend into background |

### Logo Dark Mode Fix

**Option 1:** Add `border: 1px solid #CCCCCC` to prevent disappearing on dark backgrounds.
**Option 2:** Use two image tags (`.light-logo` and `.dark-logo`) with `@media (prefers-color-scheme: dark)` to swap between them.

---

## Image Optimization

### Email Size Limits

| Metric | Ideal | Absolute Max | Consequence |
|--------|-------|--------------|-------------|
| Total email HTML size | <60KB | 102KB | Gmail clips emails >102KB |
| Individual image size | <200KB | 1MB | Slow load, blocked images |
| Image count | 5-10 | 20 | More images = more blocking risk |

**Gmail clipping:** If HTML exceeds 102KB, Gmail truncates the email and shows "[Message clipped] View entire message" link. This breaks CTAs and harms conversion.

### Text-to-Image Ratio

**Minimum 60% text, maximum 40% images** (by email height, not file size).

**Why:**
- Spam filters flag image-heavy emails
- Users block images by default (30-40% of recipients)
- Accessibility (screen readers can't read images without alt text)

**Image-only emails:** Deliverability drops 50%+.

### Retina Display Optimization

Save images at 2x resolution, display at 1x via `width`/`height` attributes. 2x images are ~3-4x larger — use TinyPNG or ImageOptim to compensate.

### Alt Text (Required)

**Every image needs alt text.**

```html
<img src="product.jpg" alt="Blue running shoes - $79.99" width="300" height="200" style="display: block;" />
```

**Alt text best practices:**
- Describe the image for screen readers
- Include key info (price, CTA) if image contains text
- For decorative images, use `alt=""` (empty, not missing)
- Max 125 characters (screen readers truncate)

### Image Blocking

**30-40% of recipients block images by default** (Gmail, Outlook). Fallback strategies: always include alt text, set `bgcolor` on image `<td>`, never put CTA text inside images (use HTML text buttons).

### Image Formats

| Format | Use Case | Compression | Transparency |
|--------|----------|-------------|--------------|
| JPEG | Photos, gradients | Lossy (60-80% quality) | No |
| PNG | Logos, text, icons | Lossless | Yes |
| GIF | Animations, simple graphics | Lossless (256 colors max) | Yes |
| WebP | Modern alternative (not safe) | Lossy/lossless | Yes |
| SVG | Vectors (not safe for email) | Lossless | Yes |

**Email-safe formats:** JPEG, PNG, GIF. Avoid WebP and SVG (limited support).

### Compression

Use TinyPNG, ImageOptim, or Squoosh. Target: <100KB per image, <50KB for logos/icons.

---

## Gmail-Specific Rules

### Clipping Threshold

**Gmail clips emails exceeding 102KB total HTML size.** This includes:
- HTML markup
- Inline CSS
- Inline SVG (don't use)
- Base64-encoded images (don't use)

**Does NOT include:**
- External images (loaded via `<img src>`)
- External stylesheets (which Gmail strips anyway)

**How to check email size:**
1. Save final HTML file
2. Check file size in bytes: `ls -lh email.html`
3. Aim for <60KB, absolute max 90KB (buffer for email client wrapping)

**If email exceeds 102KB:**
- Remove inline SVG (use PNG instead)
- Minify HTML (remove whitespace, comments)
- Reduce inline CSS (Gmail strips `<style>` anyway, so move media queries to conditional comments)
- Split into multi-part email (not recommended)

### Gmail Style Block Limit

Gmail enforces an **8,192 character limit on `<style>` blocks**. If your embedded CSS exceeds this, Gmail strips the entire `<style>` tag rather than partially rendering it. This is separate from the 102KB clipping threshold.

**Mitigation:**
- Inline critical CSS on elements (required anyway since Gmail strips `<style>`)
- Keep `<style>` blocks under 8,192 characters (for media queries and progressive enhancement)
- Minify CSS (remove comments, whitespace) before sending

### Gmail Caching and CSS

Gmail caches images indefinitely — add cache-busting query params (`?v=2`) for updated images. Gmail strips all `<style>` and `<link>` tags (except media queries on mobile apps), so inline all critical CSS.

---

## Preheader Text

**Preheader text** is the snippet shown after the subject line in inbox previews.

**Character limits:**
- Mobile (Apple Mail): 30-40 characters
- Desktop (Gmail): 80-100 characters
- Outlook: 50-70 characters

**Implementation:** Use hidden `<div>` with `display: none; max-height: 0px; overflow: hidden; mso-hide: all;` immediately after `<body>`.

**Rules:** 30-80 characters, expand subject line (don't repeat), include CTA or value prop. +3% open rate vs no preheader.

---

## Accessibility Standards

### Semantic HTML

Use semantic tags where supported:
- `<h1>`, `<h2>` for headings (not `<font size="5">`)
- `<p>` for paragraphs
- `<a>` for links (not `<span onclick>`)

**Note:** Outlook renders `<h1>` as Times New Roman by default. Override:
```html
<h1 style="margin: 0; font-family: Arial, sans-serif; font-size: 28px; font-weight: bold; color: #333333;">
  Heading
</h1>
```

### Role Attribute for Tables

```html
<table role="presentation" cellspacing="0" cellpadding="0" border="0">
```

**Why:** Tells screen readers this table is for layout, not data. Without it, screen readers announce "table with 3 columns, 5 rows" (confusing).

### Link Descriptiveness

**Avoid "click here."** Use descriptive link text.

```html
<!-- CORRECT -->
<a href="https://example.com/pricing">View our pricing plans</a>

<!-- WRONG -->
<a href="https://example.com/pricing">Click here</a>
```

### Color Contrast

WCAG AA standard: **4.5:1 contrast ratio** for normal text, **3:1 for large text** (18px+ or 14px+ bold).

**Tools:** WebAIM Contrast Checker, Coolors Contrast Checker.

---

## Outlook-Specific Hacks

Outlook desktop (Windows) uses **Microsoft Word rendering engine** (yes, really). This breaks most modern CSS.

### Conditional Comments

Use `<!--[if mso]>...<![endif]-->` to target Outlook-only styles, font overrides, spacing fixes, and content visibility.

### VML for Background Images

Outlook doesn't support CSS `background-image`. Use VML (Vector Markup Language) with `v:rect` and `v:fill type="frame"` wrapped in `<!--[if mso]>` conditional comments. **Modern approach:** Avoid background images in Outlook entirely. Use solid colors or table `bgcolor` instead.

---

## Testing Checklist

Before sending, test in:

| Client | Priority | Why |
|--------|----------|-----|
| Apple Mail (iOS) | Critical | 50%+ market share |
| Gmail (web) | Critical | 30% market share, clips >102KB |
| Outlook (Windows) | High | Breaks everything, 8% share |
| Gmail (Android/iOS app) | High | Dark mode, mobile |
| Yahoo Mail | Medium | 5% share, quirky |
| Outlook.com | Low | <4% share, better than desktop |

**Testing tools:**
- Litmus (paid): Tests 90+ clients, screenshots
- Email on Acid (paid): Similar to Litmus
- Testi@ (free): Limited clients, slower
- Manual testing: Send to yourself on 3-5 clients

---

## Performance Checklist

- [ ] Total HTML size <60KB (Gmail clipping)
- [ ] Individual images <200KB
- [ ] Text-to-image ratio 60/40 minimum
- [ ] All images have alt text
- [ ] All critical CSS inlined
- [ ] Web-safe fonts used
- [ ] 44x44px minimum touch targets
- [ ] Mobile font size 14px+ (16px for body)
- [ ] Responsive breakpoints at 600px and 480px
- [ ] Dark mode styles defined
- [ ] Preheader text 30-80 characters
- [ ] Tested in Apple Mail, Gmail, Outlook
- [ ] No Grid/Flexbox layouts (tables only)

---

## Anti-Patterns (Never Do This)

| Anti-Pattern | Why | Fix |
|--------------|-----|-----|
| All-image email | Spam filters, accessibility | 60/40 text-to-image |
| Flexbox/Grid layouts | Breaks in Outlook, Gmail | Table-based layouts |
| External CSS | Gmail strips `<style>` and `<link>` | Inline all critical CSS |
| Base64-encoded images | Bloats HTML size, Gmail clips | External image URLs |
| Forms/JavaScript | Stripped by all clients | Link to landing page |
| Custom fonts without fallback | Renders as Times New Roman | Web-safe fallback |
| Single image as CTA | Blocked images = no CTA | HTML button with text |

See the `email-write` sub-skill for a complete HTML email boilerplate with responsive design, dark mode, and Outlook conditional comments.

<!-- Updated: 2026-02-16 -->
